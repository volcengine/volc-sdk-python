# coding: utf-8
import base64
import hashlib
import json
import os
import queue
import threading
import time
import uuid

import urllib3

LOWEST_SUPPORTED_VERSION = "v1.7.2.2"
ISP_CT = "ct"
ISP_UN = "un"
ISP_CM = "cm"
SYS_WIN = "nt"
FTRANS_MOUNT_PATH = "/var/mnt"
FTRANS_S10_P2_PATH = "/s10/p2/ftrans"
FTRANS_ORDER_TYPE_ASC = "asc"
FTRANS_ORDER_TYPE_DESC = "desc"
FTRANS_ORDER_FIELD_NAME = "name"
FTRANS_ORDER_FIELD_MTIME = "mtime"
FTRANS_DEFAULT_PAGE_NUM = 1
FTRANS_DEFAULT_PAGE_SIZE = 10
FTRANS_STATUS_WAITING = 0
FTRANS_STATUS_DOING = 1
FTRANS_STATUS_FINISHED = 2
FTRANS_STATUS_FAILED = 3
FTRANS_DEFAULT_PART_SIZE = 4 << 20
FTRANS_DEFAULT_PART_CONCURRENCY = 4
HTTP_METHOD_POST = "POST"
HTTP_STATUS_OK = 200


class FtransFileTask(object):
    def __init__(self, local_file_path, remote_file_path, temp_file_path, file_size, mtime, file, part_size,
                 consistency_check, md5_check, md5=None):
        self.local_file_path = local_file_path
        self.remote_file_path = remote_file_path
        self.temp_file_path = temp_file_path
        self.file_size = file_size
        self.mtime = mtime
        self.file = file
        self.part_size = part_size
        self.consistency_check = consistency_check
        self.md5_check = md5_check
        self.md5 = md5
        self.parts = None
        self.status = FTRANS_STATUS_WAITING
        self.lock = threading.Lock()

    def split_part_task(self):
        self.parts = queue.Queue()
        start = 0
        end = self.file_size

        while start < end:
            size = self.part_size
            if start + size > end:
                size = end - start

            fpt = FtransPartTask(start, size, self)
            self.parts.put(fpt)
            start += size


class FtransPartTask(object):
    def __init__(self, off, size, fft):
        self.off = off
        self.size = size
        self.parent_task = fft
        self.data = None
        self.status = FTRANS_STATUS_WAITING


class FtransWorker(threading.Thread):
    def __init__(self, func, args_list):
        self.func = func
        self.args_list = args_list
        super().__init__()

    def run(self):
        while True:
            try:
                args = self.args_list.get(timeout=1)
                self.func(args)
            except Exception as ex:
                return


class FtransService(object):
    def __init__(self, bucket, acl_token, server_name, s10_server, cert_pem, key_pem, isp="ct"):
        addr, port = FtransService._parse_s10_server(s10_server, isp)
        if addr == "" or port <= 0:
            raise Exception("invalid s10 server[%s] or isp[%s]" % (s10_server, isp))

        self._addr = addr
        self._port = port
        self._bucket = bucket
        self._ftrans_acl_token = acl_token
        self._ftrans_server_name = server_name
        self._ftrans_cert_file, self._ftrans_key_file = FtransService._save_cert_into_file(bucket, cert_pem, key_pem)
        self._conn = urllib3.HTTPSConnectionPool(
            self._addr,
            self._port,
            cert_file=self._ftrans_cert_file,
            key_file=self._ftrans_key_file,
            assert_hostname=self._ftrans_server_name
        )

    @staticmethod
    def _save_cert_into_file(bucket, cert, key):
        random_str = uuid.uuid4().hex
        cert_file = "%s_%s.cert" % (bucket, random_str)
        with open(cert_file, "w+") as f:
            f.write(cert)

        key_file = "%s_%s.key" % (bucket, random_str)
        with open(key_file, "w+") as f:
            f.write(key)
        return cert_file, key_file

    @staticmethod
    def _parse_s10_server(s10_server, selected_isp):
        addr_isp_map = {}
        cur_version = LOWEST_SUPPORTED_VERSION
        for seg in s10_server.split(";"):
            elems = seg.split(":")
            if len(elems) < 3:
                continue

            if elems[0] < cur_version:
                continue

            port = int(elems[-1])
            isp = elems[1]
            if isp == ISP_CT or isp == ISP_UN or isp == ISP_CM:
                addr = ":".join(elems[2:-1])
                if addr[0] == '[' and addr[-1] == ']':
                    addr = addr[1:-1]
                addr_isp_map[isp] = (addr, port)
            else:
                addr = ":".join(elems[1:-1])
                if addr[0] == '[' and addr[-1] == ']':
                    addr = addr[1:-1]
                addr_isp_map[ISP_CT] = (addr, port)
                addr_isp_map[ISP_UN] = (addr, port)
                addr_isp_map[ISP_CM] = (addr, port)

            cur_version = elems[0]

        return addr_isp_map[selected_isp]

    def _get_full_path(self, file):
        return "%s/%s/%s" % (FTRANS_MOUNT_PATH, self._bucket, file)

    def _do_post(self, uri, params, headers=None, body=None):
        query = []
        for k, v in params.items():
            query.append("%s=%s" % (k, v))
        url = "%s?%s" % (uri, "&".join(query))

        try:
            return self._conn.request(HTTP_METHOD_POST, url, headers=headers, body=body)
        except Exception as ex:
            raise Exception("request %s failed %s" % (url, str(ex)))

    def _upload_file_part(self, fpt):
        uri = FTRANS_S10_P2_PATH
        full_path = self._get_full_path(fpt.parent_task.temp_file_path)
        params = {
            "op": "upload_file",
            "des": base64.b64encode(bytes(full_path, encoding="UTF-8")).decode("UTF-8"),
            "offset": fpt.off,
            "size": fpt.size,
            "mtime": fpt.parent_task.mtime,
            "acltoken": self._ftrans_acl_token
        }
        resp = self._do_post(uri, params, body=fpt.data)
        if resp.status != HTTP_STATUS_OK:
            raise Exception("invalid response status [%d] when upload %s" %
                            (resp.status, fpt.parent_task.local_file_path))
        return resp

    def _download_file_part(self, fpt):
        uri = FTRANS_S10_P2_PATH
        full_path = self._get_full_path(fpt.parent_task.remote_file_path)
        params = {
            "op": "download_file",
            "src": base64.b64encode(bytes(full_path, encoding="UTF-8")).decode("UTF-8"),
            "offset": fpt.off,
            "size": fpt.size,
            "acltoken": self._ftrans_acl_token
        }
        resp = self._do_post(uri, params)
        if resp.status != HTTP_STATUS_OK:
            raise Exception("invalid response status [%d] when download %s" % (resp.status, fpt.remote_file_path))

        file_size = int(resp.headers.get("Fsize"))
        mtime = int(resp.headers.get("Mtime"))

        return file_size, mtime, resp.data

    def get_file_size(self, filename):
        uri = FTRANS_S10_P2_PATH
        full_path = self._get_full_path(filename)
        params = {
            "op": "size_file",
            "src": base64.b64encode(bytes(full_path, encoding="UTF-8")).decode("UTF-8"),
            "acltoken": self._ftrans_acl_token
        }

        resp = self._do_post(uri, params)
        if resp.status != HTTP_STATUS_OK:
            raise Exception("invalid response status [%d] when get size of %s" % (resp.status, filename))

        file_size = int(resp.headers.get("Fsize"))
        mtime = int(resp.headers.get("Mtime"))

        return file_size, mtime

    def _get_file_md5(self, filename):
        uri = FTRANS_S10_P2_PATH
        full_path = self._get_full_path(filename)
        params = {
            "op": "md5_file",
            "src": base64.b64encode(bytes(full_path, encoding="UTF-8")).decode("UTF-8"),
            "acltoken": self._ftrans_acl_token
        }

        resp = self._do_post(uri, params)
        if resp.status != HTTP_STATUS_OK:
            raise Exception("invalid response status [%d] when get md5 of %s" % (resp.status, filename))

        md5_str = resp.headers.get("Md5")

        return md5_str

    def remove_file(self, filename):
        return self._remove_file(filename)

    def _remove_file(self, filename):
        uri = FTRANS_S10_P2_PATH
        full_path = self._get_full_path(filename)
        params = {
            "op": "remove_file",
            "des": base64.b64encode(bytes(full_path, encoding="UTF-8")).decode("UTF-8"),
            "acltoken": self._ftrans_acl_token
        }

        resp = self._do_post(uri, params)
        if resp.status != HTTP_STATUS_OK:
            raise Exception("invalid response status [%d] when remove %s" % (resp.status, filename))
        return

    def _rename_file(self, src, dst):
        uri = FTRANS_S10_P2_PATH
        src_path = self._get_full_path(src)
        dst_path = self._get_full_path(dst)

        params = {
            "op": "rename_file",
            "src": base64.b64encode(bytes(src_path, encoding="UTF-8")).decode("UTF-8"),
            "des": base64.b64encode(bytes(dst_path, encoding="UTF-8")).decode("UTF-8"),
            "acltoken": self._ftrans_acl_token
        }

        resp = self._do_post(uri, params)
        if resp.status != HTTP_STATUS_OK:
            raise Exception("invalid response status [%d] when rename %s into %s" % (resp.status, src, dst))

    def list_file(self, prefix, filter_in=None, order_type=None, order_field=None, page_num=None, page_size=None):
        uri = FTRANS_S10_P2_PATH
        full_path = self._get_full_path(prefix)
        if filter_in is None:
            filter_in = ""
        if order_type is None or order_field != FTRANS_ORDER_TYPE_DESC:
            order_type = FTRANS_ORDER_TYPE_ASC
        if order_field is None or order_field != FTRANS_ORDER_FIELD_MTIME:
            order_field = FTRANS_ORDER_FIELD_NAME
        if page_num is None or page_num <= 0:
            page_num = FTRANS_DEFAULT_PAGE_NUM
        if page_size is None or page_size <= 0:
            page_size = FTRANS_DEFAULT_PAGE_SIZE

        params = {
            "op": "list_dir",
            "src": base64.b64encode(bytes(full_path, encoding="UTF-8")).decode("UTF-8"),
            "filterIn": base64.b64encode(bytes(filter_in, encoding="UTF-8")).decode("UTF-8"),
            "orderBy": order_type,
            "sortBy": order_field,
            "pageNo": page_num,
            "pageSize": page_size,
            "acltoken": self._ftrans_acl_token
        }

        resp = self._do_post(uri, params)
        if resp.status != HTTP_STATUS_OK:
            raise Exception("invalid response status [%d] when list dir %s" % (resp.status, prefix))

        total = int(resp.headers.get("matchedNum"))
        records = json.loads(resp.data)

        return total, records

    def _make_dir(self, dir_name, mtime):
        uri = FTRANS_S10_P2_PATH
        full_path = self._get_full_path(dir_name)
        params = {
            "op": "make_dir",
            "des": base64.b64encode(bytes(full_path, encoding="UTF-8")).decode("UTF-8"),
            "mtime": mtime,
            "acltoken": self._ftrans_acl_token
        }

        resp = self._do_post(uri, params)
        if resp.status != HTTP_STATUS_OK:
            raise Exception("invalid response status [%d] when make dir %s" % (resp.status, dir_name))
        return

    def _file_exist(self, filename):
        uri = FTRANS_S10_P2_PATH
        full_path = self._get_full_path(filename)
        params = {
            "op": "exist_file",
            "src": base64.b64encode(bytes(full_path, encoding="UTF-8")).decode("UTF-8"),
            "acltoken": self._ftrans_acl_token
        }

        resp = self._do_post(uri, params)
        if resp.status != HTTP_STATUS_OK:
            return False
        return True

    @staticmethod
    def _get_local_file_md5(local_file_path):
        m = hashlib.md5()
        with open(local_file_path, 'rb') as f:
            while True:
                data = f.read(FTRANS_DEFAULT_PART_SIZE)
                if not data:
                    break
                m.update(data)

        return m.hexdigest()

    @staticmethod
    def _to_slash(raw):
        return raw.replace(":\\", "/").replace("\\", "/")

    def upload_file(self, local_file_path, remote_file_path, part_size=None, consistency_check=True, md5_check=False):
        if not os.path.exists(local_file_path):
            raise Exception("file %s not found" % local_file_path)

        fi = os.stat(local_file_path)
        file_size = fi.st_size
        mtime = int(fi.st_mtime * 10e5)
        md5 = ""
        if md5_check:
            md5 = self._get_local_file_md5(local_file_path)

        remote_file_path = FtransService._to_slash(remote_file_path)
        if self._file_exist(remote_file_path):
            remote_file_size, remote_file_mtime = self.get_file_size(remote_file_path)
            if file_size == remote_file_size and mtime == remote_file_mtime:
                if not md5_check:
                    return remote_file_path, file_size, mtime, md5
                else:
                    remote_md5 = self._get_file_md5(remote_file_path)
                    if md5 == remote_md5:
                        return remote_file_path, file_size, mtime, md5

        if os.path.isdir(local_file_path):
            self._make_dir(remote_file_path, mtime)
            return remote_file_path, 0, mtime, ""

        f = open(local_file_path, "rb")
        temp_file_path = "%s_%s" % (remote_file_path, uuid.uuid4().hex)
        part_size = FTRANS_DEFAULT_PART_SIZE
        fft = FtransFileTask(local_file_path, remote_file_path, temp_file_path, file_size, mtime, f,
                             part_size, consistency_check, md5_check, md5)
        fft.split_part_task()

        if fft.file_size <= 0:
            fpt = FtransPartTask(0, 0, fft)
            self._upload_file_part(fpt)
            self._rename_file(fft.temp_file_path, fft.remote_file_path)
            return remote_file_path, file_size, mtime * 10e5, md5

        fft.status = FTRANS_STATUS_DOING
        worker_list = []
        i = 0
        while i < FTRANS_DEFAULT_PART_CONCURRENCY:
            worker = FtransWorker(self._upload_part, fft.parts)
            worker.start()
            worker_list.append(worker)
            i += 1

        for worker in worker_list:
            worker.join()

        if fft.status == FTRANS_STATUS_DOING:
            fft.status = FTRANS_STATUS_FINISHED
        else:
            fft.status = FTRANS_STATUS_FAILED
        fft.file.close()

        if fft.status != FTRANS_STATUS_FINISHED:
            raise Exception("upload file %s failed" % local_file_path)

        if fft.md5_check:
            md5 = self._get_file_md5(temp_file_path)
            if fft.md5 != md5:
                raise Exception("md5 check failed(local: %s, remote: %s) when upload %s" %
                                (fft.md5, md5, fft.local_file_path))

        self._rename_file(fft.temp_file_path, fft.remote_file_path)
        return fft.remote_file_path, fft.file_size, fft.mtime, md5

    def download_file(self, local_file_path, remote_file_path, part_size=None, consistency_check=True, md5_check=False):
        md5 = ""

        file_size, mtime = self.get_file_size(remote_file_path)
        if md5_check:
            md5 = self._get_file_md5(remote_file_path)

        if os.path.exists(local_file_path):
            fi = os.stat(local_file_path)
            if fi.st_size == file_size and fi.st_mtime * 10e5 == mtime:
                if md5_check:
                    local_md5 = self._get_local_file_md5(local_file_path)
                    if local_md5 == md5:
                        return remote_file_path, file_size, mtime, md5
                else:
                    return remote_file_path, file_size, mtime, md5
            os.remove(local_file_path)

        temp_file_path = "%s_%s" % (local_file_path, uuid.uuid4().hex)

        save_dir = os.path.dirname(temp_file_path)
        if not os.path.exists(save_dir):
            os.makedirs(save_dir)

        f = open(temp_file_path, "wb+")
        part_size = FTRANS_DEFAULT_PART_SIZE
        fft = FtransFileTask(local_file_path, remote_file_path, temp_file_path, file_size, mtime, f,
                             part_size, consistency_check, md5_check, md5)
        fft.split_part_task()

        if fft.file_size <= 0:
            fft.file.close()
            os.rename(fft.temp_file_path, fft.local_file_path)
            return fft.remote_file_path, fft.file_size, fft.mtime, fft.md5

        try:
            fft.status = FTRANS_STATUS_DOING
            worker_list = []
            i = 0
            while i < FTRANS_DEFAULT_PART_CONCURRENCY:
                worker = FtransWorker(self._download_part, fft.parts)
                worker.start()
                worker_list.append(worker)
                i += 1

            for worker in worker_list:
                worker.join()

            if fft.status == FTRANS_STATUS_DOING:
                fft.status = FTRANS_STATUS_FINISHED
            else:
                fft.status = FTRANS_STATUS_FAILED
            fft.file.close()

            if fft.status != FTRANS_STATUS_FINISHED:
                raise Exception("download file %s failed" % remote_file_path)

            if fft.md5_check:
                md5 = self._get_local_file_md5(temp_file_path)
                if fft.md5 != md5:
                    raise Exception("md5 check failed(local: %s, remote: %s) when upload %s" %
                                    (fft.md5, md5, fft.local_file_path))

            os.rename(fft.temp_file_path, fft.local_file_path)
            os.utime(fft.local_file_path, (time.time(), float(mtime) / 1e6))
            return fft.remote_file_path, fft.file_size, fft.mtime, md5
        except Exception as ex:
            os.remove(fft.temp_file_path)
            raise ex

    def _upload_part(self, fpt):
        with fpt.parent_task.lock:
            if fpt.parent_task.status == FTRANS_STATUS_FAILED:
                raise Exception("some part upload failed for %s" % fpt.parent_task.local_file_path)
            fpt.parent_task.file.seek(fpt.off)
            fpt.data = fpt.parent_task.file.read(fpt.size)
        try:
            self._upload_file_part(fpt)
        except Exception as ex:
            with fpt.parent_task.lock:
                fpt.parent_task.status = FTRANS_STATUS_FAILED
            raise ex

    def _download_part(self, fpt):
        with fpt.parent_task.lock:
            if fpt.parent_task.status == FTRANS_STATUS_FAILED:
                raise Exception("some part download failed for %s" % fpt.parent_task.remote_file_path)
        try:
            file_size, mtime, data = self._download_file_part(fpt)
            if fpt.parent_task.consistency_check:
                if file_size != fpt.parent_task.file_size or mtime != fpt.parent_task.mtime:
                    raise Exception("file %s has been modified during downloading" % fpt.parent_task.remote_file_path)
            with fpt.parent_task.lock:
                fpt.parent_task.file.seek(fpt.off)
                fpt.parent_task.file.write(data)
        except Exception as ex:
            with fpt.parent_task.lock:
                fpt.parent_task.status = FTRANS_STATUS_FAILED
            raise ex

    def clean(self):
        os.remove(self._ftrans_cert_file)
        os.remove(self._ftrans_key_file)
