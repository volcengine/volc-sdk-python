import base64
import hashlib
import json
import os
import queue
import random
import threading
import time
import uuid

import urllib3.poolmanager

ISP_CT = "ct"
ISP_UN = "un"
ISP_CM = "cm"
ISP_DEFAULT="default"
VERSION_DEFAULT="default"
SWITCH_ON = 1
SWITCH_OFF = 0
FTRANS_PROTOCOL_TCP = "tcp"
FTRANS_PROTOCOL_UDP = "udp"
FTRANS_HTTP_STATUS_OK = 200
FTRANS_SIG_EXPIRED_NSEC = 15
FTRANS_HTTP_METHOD_GET = "GET"
FTRANS_HTTP_METHOD_POST = "POST"
FTRANS_MOUNT_PATH = "/var/mnt"
FTRANS_ORDER_TYPE_ASC = "asc"
FTRANS_ORDER_TYPE_DESC = "desc"
FTRANS_ORDER_FIELD_NAME = "name"
FTRANS_ORDER_FIELD_MTIME = "mtime"
FTRANS_DEFAULT_PAGE_NUM = 1
FTRANS_DEFAULT_PAGE_SIZE = 10
FTRANS_DEFAULT_FILTER_IN = ""
FTRANS_PART_SIZE = 4 << 20
FTRANS_STATUS_WAITING = 0
FTRANS_STATUS_DOING = 1
FTRANS_STATUS_FINISHED = 2
FTRANS_STATUS_FAILED = 3
FTRANS_DEFAULT_PART_CONCURRENCY = 4
FTRANS_TRANS_STATUS_COMPLETED = "completed"
FTRANS_TRANS_STATUS_FAILED = "failed"
FTRANS_TRANS_STATUS_CANCELLED = "cancelled"
FTRANS_STATUS_UPLOAD_FILE_NONE = 0x401003
FTRANS_STATUS_DOWNLOAD_FILE_NONE = 0x402003
FTRANS_STATUS_SUCC = 0x000000


class FtransException(Exception):
    pass


class FtransParameterException(FtransException):
    pass


class FtransNetworkException(FtransException):
    pass


class FtransHttpResponseException(FtransException):
    pass


class FtransUploadException(FtransException):
    pass


class FtransDownloadException(FtransException):
    pass


class FtransFileNotFound(FtransException):
    pass


def _split_addr(addr):
    if addr[0] == '[':
        segs = addr.split(":")
        ip = ":".join(segs[0:-1])
        ip = ip[1:-1]
        port = int(segs[-1])
    else:
        segs = addr.split(":")
        ip = segs[0]
        port = int(segs[-1])

    return ip, port


def _set_addr_map(addr_map, version, isp, ip, port):
    if version not in addr_map:
        addr_map[version] = {}

    if isp not in addr_map[version]:
        addr_map[version][isp] = []

    found = False
    for exist_ip, exist_port in addr_map[version][isp]:
        if ip == exist_ip and port == exist_port:
            found = True
            break
    if not found:
        addr_map[version][isp].append((ip, port))


def _get_addr_map(addr_map, version, isp):
    if version not in addr_map:
        if VERSION_DEFAULT not in addr_map:
            raise FtransException("version not found in addr_map")

        version = VERSION_DEFAULT

    if isp not in addr_map[version]:
        if ISP_DEFAULT not in addr_map[version]:
            raise FtransException("isp not found in addr_map")

        isp = ISP_DEFAULT

    if len(addr_map[version][isp]) == 0:
        raise FtransException("empty addr list")

    return addr_map[version][isp][random.randint(1, 100) % len(addr_map[version][isp])]

def _build_addr_map(addr):
    addr_map = {}

    for elem in addr.split(";"):
        idx = elem.find("[")
        if idx == -1:
            # ipv4
            segs = elem.split(":")
            if len(segs) < 2 or len(segs) > 4:
                continue
            if len(segs) == 2:
                # ip4:port
                ip, port = _split_addr(elem)
                _set_addr_map(addr_map, VERSION_DEFAULT, ISP_DEFAULT, ip, port)
            elif len(segs) == 3:
                if segs[0] != ISP_CT and segs[0] != ISP_UN and segs[0] != ISP_CM:
                    # version:ip4:port
                    ip, port = _split_addr(":".join(segs[1:]))
                    _set_addr_map(addr_map, segs[0], ISP_DEFAULT, ip, port)
                else:
                    # isp:ip4:port
                    ip, port = _split_addr(":".join(segs[1:]))
                    _set_addr_map(addr_map, VERSION_DEFAULT, segs[0], ip, port)
            else:
                # version:isp:ip4:port
                ip, port = _split_addr(":".join(segs[2:]))
                _set_addr_map(addr_map, segs[0], segs[1], ip, port)
        else:
            # ipv6
            if idx == 0:
                # [ip6]:port
                ip, port = _split_addr(elem)
                _set_addr_map(addr_map, VERSION_DEFAULT, ISP_DEFAULT, ip, port)
            else:
                segs = elem[:idx-1].split(":")
                if len(segs) > 2:
                    continue

                ip, port = _split_addr(elem[idx:])
                if len(segs) == 1:
                    if segs[0] != ISP_CT and segs[0] != ISP_UN and segs[0] != ISP_CM:
                        # version:[ip6]:port
                        _set_addr_map(addr_map, segs[0], ISP_DEFAULT, ip, port)
                    else:
                        # isp:[ip6]:port
                        _set_addr_map(addr_map, VERSION_DEFAULT, segs[0], ip, port)
                else:
                    # version:isp:[ip6]:port
                    _set_addr_map(addr_map, segs[0], segs[1], ip, port)
    return addr_map


def _save_cert_key(cert_pem, key_pem):
    random_str = uuid.uuid4().hex
    cert_file = "%s.cert" % random_str
    with open(cert_file, "w+") as f:
        f.write(cert_pem)

    key_file = "%s.key" % random_str
    with open(key_file, "w+") as f:
        f.write(key_pem)
    return cert_file, key_file


def _stat_local_file(filename):
    return os.stat(filename)


def _normalize_filter_in(filter_in):
    special_chars = {
        "\\": "\\\\",
        ".": "\\.",
        "*": "\\*",
        "+": "\\+",
        "?": "\\?",
        "[": "\\[",
        "]": "\\]",
        "{": "\\{",
        "}": "\\}",
        "(": "\\(",
        ")": "\\)",
        ",": "\\,"
    }

    for old in special_chars:
        filter_in = filter_in.replace(old, special_chars[old])

    return filter_in


def _to_slash(filename):
    filename = filename.replace(":\\", "/").replace("\\", "/")
    if filename[0] == '/':
        filename = filename[1:]

    return filename


class FtransPartTask(object):
    def __init__(self, off, size, fft):
        self.off = off
        self.size = size
        self.parent_task = fft
        self.data = None
        self.status = FTRANS_STATUS_WAITING


class FtransFileTask(object):
    def __init__(self, local_file_path, remote_file_path, temp_file_path, file_size, mtime, file):
        self.local_file_path = local_file_path
        self.remote_file_path = remote_file_path
        self.temp_file_path = temp_file_path
        self.file_size = file_size
        self.mtime = mtime
        self.file = file
        self.parts = None
        self.status = FTRANS_STATUS_WAITING
        self.lock = threading.Lock()

    def split_part_task(self):
        self.parts = queue.Queue()

        start = 0
        end = self.file_size

        while start < end:
            size = FTRANS_PART_SIZE
            if start + size > end:
                size = end - start

            fpt = FtransPartTask(start, size, self)
            self.parts.put(fpt)
            start += size


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
            except queue.Empty:
                return


class FtransService(object):
    def __init__(self, bucket, acl_token, server_name, s10_server=None, cert_pem=None, key_pem=None, isp="ct",
                 client_addr=None, s2_server=None, proxy_addr=None,
                 client_acl_token=None):
        self._ftrans_bucket = bucket
        self._ftrans_acl_token = acl_token
        self._ftrans_server_name = server_name
        self._ftrans_s10_addr = None
        self._ftrans_s10_port = None
        self._ftrans_s10_cert_file = None
        self._ftrans_s10_key_file = None
        self._ftrans_client_addr = None
        self._ftrans_client_port = None
        self._ftrans_s2_addr = None
        self._ftrans_s2_port = None
        self._ftrans_proxy_addr = None
        self._ftrans_proxy_port = None
        self._ftrans_client_config = None

        if s10_server is not None:
            try:
                addr_map = _build_addr_map(s10_server)
            except Exception:
                raise FtransParameterException("invalid s10 server addr %s" % s10_server)

            try:
                s10_addr, s10_port = _get_addr_map(addr_map, VERSION_DEFAULT, isp)
            except:
                raise FtransParameterException("no s10 server found of isp[%s]" % isp )

            if cert_pem is None or key_pem is None:
                raise FtransParameterException("cert_pem and key_pem must be specified when s10_server is set")

            cert_file, key_file = _save_cert_key(cert_pem, key_pem)

            self._ftrans_s10_addr = s10_addr
            self._ftrans_s10_port = s10_port
            self._ftrans_s10_cert_file = cert_file
            self._ftrans_s10_key_file = key_file
            self._ftrans_s10_conn = urllib3.HTTPSConnectionPool(
                self._ftrans_s10_addr,
                self._ftrans_s10_port,
                cert_file=self._ftrans_s10_cert_file,
                key_file=self._ftrans_s10_key_file,
                assert_hostname=self._ftrans_server_name
            )

        if client_addr is not None:
            if s2_server is None:
                raise FtransParameterException("s2_server must be specified when client_addr is set")

            try:
                client_ip, client_port = _split_addr(client_addr)
            except Exception:
                raise FtransParameterException("invalid client_addr [%s]" % client_addr)

            client_config = FtransService._get_ftrans_client_config(client_ip, client_port, client_acl_token)
            version = client_config["Version"]
            protocol = FTRANS_PROTOCOL_UDP
            if (client_config.get("RuntimeTransTudpSwitch", "") == SWITCH_OFF) and \
                    (client_config.get("RuntimeTransTtcpSwitch", "") == SWITCH_ON):
                protocol = FTRANS_PROTOCOL_TCP

            try:
                addr_map = _build_addr_map(s2_server)
            except Exception:
                raise FtransParameterException("invalid s2_server [%s]" % s2_server)

            try:
                s2_addr, s2_port = _get_addr_map(addr_map, version, isp)
            except:
                raise FtransParameterException("no s2 addr found of version[%s] isp[%s]" % (version, isp))
            proxy_ip = None
            proxy_port = None
            if proxy_addr is not None:
                try:
                    proxy_manager_addr, proxy_manager_port = _split_addr(proxy_addr)
                except Exception:
                    raise FtransParameterException("invalid proxy_addr[%s]" % proxy_addr)

                proxy_list = FtransService._get_ftrans_proxy_list(proxy_manager_addr, proxy_manager_port)
                found = False

                for p in proxy_list:
                    if p["TargetDomain"] == s2_addr and p["TargetPort"] == s2_port and p["Type"] == protocol and \
                            p["State"] == "运行中":
                        found = True
                        proxy_ip = p["IP"]
                        proxy_port = p["Port"]
                        break

                if not found:
                    proxy_list = FtransService._create_ftrans_proxy(proxy_manager_addr, proxy_manager_port,
                                                                    s2_addr, s2_port, protocol)
                    proxy_ip = proxy_list[0]["IP"]
                    proxy_port = proxy_list[0]["Port"]

            self._ftrans_client_addr = client_ip
            self._ftrans_client_port = client_port
            self._ftrans_s2_addr = s2_addr
            self._ftrans_s2_port = s2_port
            self._ftrans_client_config = client_config
            self._ftrans_proxy_addr = proxy_ip
            self._ftrans_proxy_port = proxy_port
            self._ftrans_client_acl_token = client_acl_token

    def __del__(self):
        os.remove(self._ftrans_s10_cert_file)
        os.remove(self._ftrans_s10_key_file)

    @staticmethod
    def _gen_ftrans_sig(op, t, token):
        if token is None:
            token = "4d0c1b2513cb82263814e10bf2f136ed"
        s = "%s@ftrans/%s@%d" % (token.lower(), op.lower(), t)
        return hashlib.md5(s.encode()).hexdigest()

    @staticmethod
    def _get_ftrans_client_config(client_addr, client_port, client_acl_token):
        op = "config"
        t = int(time.time()) + FTRANS_SIG_EXPIRED_NSEC
        sig = FtransService._gen_ftrans_sig(op, t, client_acl_token)
        url = "http://%s:%d/v2/ftrans?op=%s&t=%d&sig=%s" % (client_addr, client_port, op, t, sig)

        resp = FtransService._do_request(FTRANS_HTTP_METHOD_POST, url)

        if resp.status != FTRANS_HTTP_STATUS_OK:
            raise FtransHttpResponseException("invalid http response status %d when get client config" % resp.status)

        return json.loads(resp.data)

    @staticmethod
    def _get_ftrans_proxy_list(proxy_manager_addr, proxy_manager_port):
        url = "http://%s:%d/api/v1/proxy-list" % (proxy_manager_addr, proxy_manager_port)

        resp = FtransService._do_request(FTRANS_HTTP_METHOD_GET, url)

        if resp.status != FTRANS_HTTP_STATUS_OK:
            raise FtransHttpResponseException("invalid http response %d when get proxy list" % resp.status)

        return json.loads(resp.data)

    @staticmethod
    def _create_ftrans_proxy(proxy_manager_addr, proxy_manager_port, s2_addr, s2_port, protocol):
        url = "http://%s:%d/api/v1/proxy" % (proxy_manager_addr, proxy_manager_port)
        data = [
            {
                "TargetDomain": s2_addr,
                "TargetPort": s2_port,
                "Type": protocol
            }
        ]

        resp = FtransService._do_request(FTRANS_HTTP_METHOD_POST, url, body=json.dumps(data))

        if resp.status != FTRANS_HTTP_STATUS_OK:
            raise FtransHttpResponseException("invalid response status [%d] when create proxy" % resp.status)

        return json.loads(resp.data)

    @staticmethod
    def _do_request(method, url, headers=None, body=None, conn=None):
        if conn is None:
            conn = urllib3.PoolManager()
        try:
            resp = conn.request(method, url, headers=headers, body=body)
        except Exception as ex:
            raise FtransNetworkException("do request %s failed %s" % (url, str(ex)))

        return resp

    def _get_full_path(self, filename):
        full_path = "%s/%s/%s" % (FTRANS_MOUNT_PATH, self._ftrans_bucket, filename)
        return full_path

    def _ftrans_client_enable(self):
        return (self._ftrans_client_addr is not None) and (self._ftrans_client_port is not None)

    def _upload_file_s2(self, local_file_path, remote_file_path):
        op = "upload"
        t = int(time.time()) + FTRANS_SIG_EXPIRED_NSEC
        sig = FtransService._gen_ftrans_sig(op, t, self._ftrans_client_acl_token)
        url = "http://%s:%d/v2/ftrans?op=%s&t=%d&sig=%s" % (self._ftrans_client_addr, self._ftrans_client_port,
                                                            op, t, sig)
        des = self._get_full_path(remote_file_path)
        if self._ftrans_proxy_addr is not None and self._ftrans_proxy_port is not None:
            server_address = "%s:%d" % (self._ftrans_proxy_addr, self._ftrans_proxy_port)
        else:
            server_address = "%s:%d" % (self._ftrans_s2_addr, self._ftrans_s2_port)
        body = {
            "serverName": self._ftrans_server_name,
            "serverAddress": server_address,
            "files": [
                {
                    "transId": uuid.uuid4().hex,
                    "aclToken": self._ftrans_acl_token,
                    "src": local_file_path,
                    "des": des
                }
            ]
        }

        resp = FtransService._do_request(FTRANS_HTTP_METHOD_POST, url, body=json.dumps(body))

        if resp.status != FTRANS_HTTP_STATUS_OK:
            raise FtransHttpResponseException("invalid http status %d when submit upload file request" % resp.status)

        upload_info = json.loads(resp.data)
        upload_info["serverName"] = self._ftrans_server_name
        upload_info["serverAddress"] = server_address

        while True:
            resp = self._status_upload_s2(upload_info)

            upload_status = resp["files"][0]

            if upload_status["transId"] != upload_info["files"][0]["transId"]:
                continue

            if upload_status["statusCode"] not in [FTRANS_STATUS_SUCC, FTRANS_STATUS_UPLOAD_FILE_NONE]:
                raise FtransUploadException("upload file %s failed %s" % (local_file_path, upload_status["statusMsg"]))

            if upload_status["statusCode"] == FTRANS_STATUS_SUCC:
                trans_status = upload_status["transStatus"]
                if trans_status == FTRANS_TRANS_STATUS_COMPLETED:
                    break
                elif (trans_status == FTRANS_TRANS_STATUS_FAILED) or (trans_status == FTRANS_TRANS_STATUS_CANCELLED):
                    raise FtransUploadException(
                        "upload file %s failed %s" % (local_file_path, upload_status["statusMsg"])
                    )

            time.sleep(1)

        stat_info = _stat_local_file(local_file_path)
        return remote_file_path, stat_info.st_size, int(stat_info.st_mtime * 1e6), None

    def _download_file_s2(self, local_file_path, remote_file_path):
        op = "download"
        t = int(time.time()) + FTRANS_SIG_EXPIRED_NSEC
        sig = FtransService._gen_ftrans_sig(op, t, self._ftrans_client_acl_token)
        url = "http://%s:%d/v2/ftrans?op=%s&t=%d&sig=%s" % (self._ftrans_client_addr, self._ftrans_client_port,
                                                            op, t, sig)
        src = self._get_full_path(remote_file_path)
        if self._ftrans_proxy_addr is not None and self._ftrans_proxy_port is not None:
            server_address = "%s:%d" % (self._ftrans_proxy_addr, self._ftrans_proxy_port)
        else:
            server_address = "%s:%d" % (self._ftrans_s2_addr, self._ftrans_s2_port)
        body = {
            "serverName": self._ftrans_server_name,
            "serverAddress": server_address,
            "files": [
                {
                    "transId": uuid.uuid4().hex,
                    "aclToken": self._ftrans_acl_token,
                    "src": src,
                    "des": local_file_path
                }
            ]
        }

        resp = FtransService._do_request(FTRANS_HTTP_METHOD_POST, url, body=json.dumps(body))

        if resp.status != FTRANS_HTTP_STATUS_OK:
            raise FtransHttpResponseException("invalid http status %d when submit download file request" % resp.status)

        download_info = json.loads(resp.data)
        download_info["serverName"] = self._ftrans_server_name
        download_info["serverAddress"] = server_address

        while True:
            resp = self._status_download_s2(download_info)

            download_status = resp["files"][0]

            if download_status["transId"] != download_info["files"][0]["transId"]:
                continue

            if download_status["statusCode"] not in [FTRANS_STATUS_SUCC, FTRANS_STATUS_DOWNLOAD_FILE_NONE]:
                raise FtransUploadException(
                    "upload file %s failed %s" % (local_file_path, download_status["statusMsg"]))

            if download_status["statusCode"] == FTRANS_STATUS_SUCC:
                trans_status = download_status["transStatus"]
                if trans_status == FTRANS_TRANS_STATUS_COMPLETED:
                    break
                elif (trans_status == FTRANS_TRANS_STATUS_FAILED) or (trans_status == FTRANS_TRANS_STATUS_CANCELLED):
                    raise FtransUploadException(
                        "upload file %s failed %s" % (local_file_path, download_status["statusMsg"])
                    )

            time.sleep(1)

        stat_info = _stat_local_file(local_file_path)
        return remote_file_path, stat_info.st_size, int(stat_info.st_mtime * 1e6), None

    def _status_upload_s2(self, upload_info):
        op = "status_upload"
        t = int(time.time()) + FTRANS_SIG_EXPIRED_NSEC
        sig = FtransService._gen_ftrans_sig(op, t, self._ftrans_client_acl_token)
        url = "http://%s:%d/v2/ftrans?op=%s&t=%d&sig=%s" % (self._ftrans_client_addr, self._ftrans_client_port,
                                                            op, t, sig)
        resp = FtransService._do_request(FTRANS_HTTP_METHOD_POST, url,
                                         body=json.dumps(upload_info))

        if resp.status != FTRANS_HTTP_STATUS_OK:
            raise FtransHttpResponseException("invalid http status %d when status upload file request" % resp.status)

        return json.loads(resp.data)

    def _status_download_s2(self, download_info):
        op = "status_download"
        t = int(time.time()) + FTRANS_SIG_EXPIRED_NSEC
        sig = FtransService._gen_ftrans_sig(op, t, self._ftrans_client_acl_token)
        url = "http://%s:%d/v2/ftrans?op=%s&t=%d&sig=%s" % (self._ftrans_client_addr, self._ftrans_client_port,
                                                            op, t, sig)
        resp = FtransService._do_request(FTRANS_HTTP_METHOD_POST, url,
                                         body=json.dumps(download_info))

        if resp.status != FTRANS_HTTP_STATUS_OK:
            raise FtransHttpResponseException("invalid http status %d when status download file request" % resp.status)

        return json.loads(resp.data)

    def _list_file_s2(self, prefix, filter_in, order_type, order_field, page_num, page_size):
        op = "list_dir"
        t = int(time.time()) + FTRANS_SIG_EXPIRED_NSEC
        sig = FtransService._gen_ftrans_sig(op, t, self._ftrans_client_acl_token)
        url = "http://%s:%d/v2/ftrans?op=%s&t=%d&sig=%s" % (self._ftrans_client_addr, self._ftrans_client_port,
                                                            op, t, sig)
        des = self._get_full_path(prefix)
        if self._ftrans_proxy_addr is not None and self._ftrans_proxy_port is not None:
            server_address = "%s:%d" % (self._ftrans_proxy_addr, self._ftrans_proxy_port)
        else:
            server_address = "%s:%d" % (self._ftrans_s2_addr, self._ftrans_s2_port)

        body = {
            "serverName": self._ftrans_server_name,
            "serverAddress": server_address,
            "aclToken": self._ftrans_acl_token,
            "des": des,
            "filterIn": filter_in,
            "sortBy": order_field,
            "orderBy": order_type,
            "pageNo": page_num,
            "pageSize": page_size
        }

        resp = FtransService._do_request(FTRANS_HTTP_METHOD_POST, url,
                                         body=json.dumps(body))

        if resp.status != FTRANS_HTTP_STATUS_OK:
            raise FtransHttpResponseException("invalid http status %d when list dir request" % resp.status)

        files = json.loads(resp.data)
        total = files["matchedNum"]
        records = files["fileNodes"]
        for f in records:
            f["mtime"] = mtime = int(time.mktime(time.strptime(f["mtime"], "%Y-%m-%d %H:%M:%S")) * 1e6)

        return total, records

    def _get_file_size_s2(self, filename):
        prefix = os.path.dirname(filename)
        name = os.path.basename(filename)
        filter_in = _normalize_filter_in(name)
        total_num, file_info_list = self._list_file_s2(prefix, filter_in, FTRANS_ORDER_TYPE_ASC, FTRANS_ORDER_FIELD_MTIME,
                                                       FTRANS_DEFAULT_PAGE_NUM, FTRANS_DEFAULT_PAGE_SIZE)
        if total_num == 0:
            raise FtransFileNotFound("file [%s] not found" % filename)
        found = False
        size = 0
        mtime = 0
        for f in file_info_list:
            if f["name"] == name:
                size = f["size"]
                mtime = f["mtime"]
                found = True
                break

        if not found:
            raise FtransFileNotFound("file [%s] not found" % filename)

        return size, mtime

    def _remove_file_s2(self, filename):
        op = "remove_file"
        t = int(time.time()) + FTRANS_SIG_EXPIRED_NSEC
        sig = FtransService._gen_ftrans_sig(op, t, self._ftrans_client_acl_token)
        url = "http://%s:%d/v2/ftrans?op=%s&t=%d&sig=%s" % (self._ftrans_client_addr, self._ftrans_client_port,
                                                            op, t, sig)
        des = self._get_full_path(filename)
        if self._ftrans_proxy_addr is not None and self._ftrans_proxy_port is not None:
            server_address = "%s:%d" % (self._ftrans_proxy_addr, self._ftrans_proxy_port)
        else:
            server_address = "%s:%d" % (self._ftrans_s2_addr, self._ftrans_s2_port)
        body = {
            "serverName": self._ftrans_server_name,
            "serverAddress": server_address,
            "aclToken": self._ftrans_acl_token,
            "des": des,
        }

        resp = FtransService._do_request(FTRANS_HTTP_METHOD_POST, url,
                                         body=json.dumps(body))

        if resp.status != FTRANS_HTTP_STATUS_OK:
            raise FtransHttpResponseException("invalid http status %d when remove file %s" % (resp.status, filename))

        return

    def _upload_part_s10(self, fpt):
        with fpt.parent_task.lock:
            if fpt.parent_task.status == FTRANS_STATUS_FAILED:
                raise FtransUploadException("some part upload failed for %s" % fpt.parent_task.local_file_path)
            fpt.parent_task.file.seek(fpt.off)
            fpt.data = fpt.parent_task.file.read(fpt.size)

        try:
            self._upload_file_part_s10(fpt)
        except Exception as ex:
            with fpt.parent_task.lock:
                fpt.parent_task.status = FTRANS_STATUS_FAILED
            raise ex

    def _download_part_s10(self, fpt):
        with fpt.parent_task.lock:
            if fpt.parent_task.status == FTRANS_STATUS_FAILED:
                raise FtransDownloadException("some part download failed for %s" % fpt.parent_task.remote_file_path)
        try:
            file_size, mtime, data = self._download_file_part_s10(fpt)
            if file_size != fpt.parent_task.file_size or mtime != fpt.parent_task.mtime:
                raise FtransDownloadException(
                    "file %s has been modified during downloading" % fpt.parent_task.remote_file_path)
            with fpt.parent_task.lock:
                fpt.parent_task.file.seek(fpt.off)
                fpt.parent_task.file.write(data)
        except Exception as ex:
            with fpt.parent_task.lock:
                fpt.parent_task.status = FTRANS_STATUS_FAILED
            raise ex

    def _upload_file_s10(self, local_file_path, remote_file_path):
        if not os.path.exists(local_file_path):
            raise FtransFileNotFound("local file %s not found" % local_file_path)

        fi = os.stat(local_file_path)
        file_size = fi.st_size
        mtime = int(fi.st_mtime * 1e6)

        des = _to_slash(remote_file_path)
        remote_file_size, remote_mtime = self._get_file_size_s10(des)
        # local_file and remote_file is same, just return success
        if (file_size == remote_file_size) and (mtime == remote_mtime):
            return des, file_size, mtime, None

        # if local_file_path is dir, just make it
        if os.path.isdir(local_file_path):
            self._make_dir_s10(des, mtime)
            return des, 0, mtime, None

        # empty file, just touch it
        if file_size == 0:
            self._touch_file_s10(des, mtime)
            return des, 0, mtime, None

        f = open(local_file_path, "rb")
        temp_file_path = "%s_%s" % (remote_file_path, uuid.uuid4().hex)
        fft = FtransFileTask(local_file_path, des, temp_file_path, file_size, mtime, f)
        fft.split_part_task()

        fft.status = FTRANS_STATUS_DOING
        worker_list = []

        i = 0
        while i < FTRANS_DEFAULT_PART_CONCURRENCY:
            worker = FtransWorker(self._upload_part_s10, fft.parts)
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
            raise FtransUploadException("upload file %s failed" % local_file_path)

        self._rename_file_s10(fft.temp_file_path, fft.remote_file_path)
        return fft.remote_file_path, fft.file_size, fft.mtime, None

    def _download_file_s10(self, local_file_path, remote_file_path):
        file_size, mtime = self._get_file_size_s10(remote_file_path)

        if (file_size == 0) and (mtime == 0):
            raise FtransFileNotFound("file %s not found" % remote_file_path)

        if os.path.exists(local_file_path):
            fi = os.stat(local_file_path)

            # local_file_path and remote_file is same
            if (fi.st_size == file_size) and (int(fi.st_mtime * 1e6) == mtime):
                return remote_file_path, file_size, mtime, None
            else:
                # local_file_path exists and not same as remote_file_path, just delete it and download
                os.remove(local_file_path)

        temp_file_path = "%s_%s" % (local_file_path, uuid.uuid4().hex)
        save_dir = os.path.dirname(temp_file_path)
        if not os.path.exists(save_dir):
            os.makedirs(save_dir)

        f = open(temp_file_path, "wb+")
        if file_size == 0:
            f.close()
            os.rename(temp_file_path, local_file_path)

        fft = FtransFileTask(local_file_path, remote_file_path, temp_file_path, file_size, mtime, f)
        fft.split_part_task()

        i = 0
        fft.status = FTRANS_STATUS_DOING
        worker_list = []
        i = 0
        while i < FTRANS_DEFAULT_PART_CONCURRENCY:
            worker = FtransWorker(self._download_part_s10, fft.parts)
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
            raise FtransDownloadException("download file %s failed" % remote_file_path)

        os.rename(fft.temp_file_path, fft.local_file_path)
        os.utime(fft.local_file_path, (time.time(), float(mtime) / 1e6))

        return remote_file_path, file_size, mtime, None

    def _upload_file_part_s10(self, fpt):
        op = "upload_file"
        des = base64.b64encode(bytes(self._get_full_path(fpt.parent_task.temp_file_path), encoding="UTF-8")).decode(
            encoding="UTF-8")
        offset = fpt.off
        size = fpt.size
        mtime = fpt.parent_task.mtime
        acl_token = self._ftrans_acl_token

        url = "/s10/p2/ftrans?op=%s&des=%s&offset=%d&size=%d&mtime=%d&acltoken=%s" % (op, des, offset, size, mtime,
                                                                                      acl_token)
        resp = self._do_request(FTRANS_HTTP_METHOD_POST, url, conn=self._ftrans_s10_conn, body=fpt.data)
        if resp.status != FTRANS_HTTP_STATUS_OK:
            raise FtransHttpResponseException("invalid http response status [%d] when upload_file_s10" % resp.status)

        return

    def _download_file_part_s10(self, fpt):
        op = "download_file"
        src = base64.b64encode(bytes(self._get_full_path(fpt.parent_task.remote_file_path), encoding="UTF-8")).decode(
            encoding="UTF-8")
        offset = fpt.off
        size = fpt.size
        acl_token = self._ftrans_acl_token

        url = "/s10/p2/ftrans?op=%s&src=%s&offset=%d&size=%d&acltoken=%s" % (op, src, offset, size, acl_token)
        resp = self._do_request(FTRANS_HTTP_METHOD_POST, url, conn=self._ftrans_s10_conn, body=fpt.data)
        if resp.status != FTRANS_HTTP_STATUS_OK:
            raise FtransHttpResponseException("invalid http response status [%d] when download_file_s10" % resp.status)

        file_size = int(resp.headers.get("Fsize"))
        mtime = int(resp.headers.get("Mtime"))

        return file_size, mtime, resp.data

    def _list_file_s10(self, prefix, filter_in, order_type, order_field, page_num, page_size):
        op = "list_dir"
        src = base64.b64encode(bytes(self._get_full_path(prefix), encoding="UTF-8")).decode(encoding="UTF-8")
        keyword = base64.b64encode(bytes(filter_in, encoding="UTF-8")).decode(encoding="UTF-8")
        url = "/s10/p2/ftrans?op=%s&src=%s&filterIn=%s&orderBy=%s&sortBy=%s&pageNo=%d&pageSize=%d&" \
              "acltoken=%s" % (
                  op, src, keyword, order_type, order_field, page_num, page_size, self._ftrans_acl_token
              )

        resp = self._do_request(FTRANS_HTTP_METHOD_POST, url, conn=self._ftrans_s10_conn)
        if resp.status != FTRANS_HTTP_STATUS_OK:
            raise FtransHttpResponseException("invalid response status [%d] when list_file_s10" % resp.status)

        total = int(resp.headers.get("matchedNum"))
        records = json.loads(resp.data)

        for f in records:
            f["mtime"] = int(time.mktime(time.strptime(f["mtime"], "%Y-%m-%d %H:%M:%S")) * 1e6)

        return total, records

    def _remove_file_s10(self, filename):
        op = "remove_file"
        des = base64.b64encode(bytes(self._get_full_path(filename), encoding="UTF-8")).decode(encoding="UTF-8")
        acl_token = self._ftrans_acl_token

        url = "/s10/p2/ftrans?op=%s&des=%s&acltoken=%s" % (op, des, acl_token)

        resp = self._do_request(FTRANS_HTTP_METHOD_POST, url, conn=self._ftrans_s10_conn)
        if resp.status != FTRANS_HTTP_STATUS_OK:
            raise FtransHttpResponseException("invalid response status [%d] when remove_file_s10" % resp.status)

        return

    def _get_file_size_s10(self, filename):
        op = "size_file"
        src = base64.b64encode(bytes(self._get_full_path(filename), encoding="UTF-8")).decode(encoding="UTF-8")
        acl_token = self._ftrans_acl_token

        url = "/s10/p2/ftrans?op=%s&src=%s&acltoken=%s" % (op, src, acl_token)

        resp = self._do_request(FTRANS_HTTP_METHOD_POST, url, conn=self._ftrans_s10_conn)
        if resp.status != FTRANS_HTTP_STATUS_OK:
            raise FtransHttpResponseException("invalid response status [%d] when get_file_size_s10" % resp.status)

        file_size = int(resp.headers.get("Fsize"))
        mtime = int(resp.headers.get("Mtime"))

        return file_size, mtime

    def _make_dir_s10(self, dir_name, mtime):
        op = "make_dir"
        des = base64.b64encode(bytes(self._get_full_path(dir_name), encoding="UTF-8")).decode(encoding="UTF-8")
        acl_token = self._ftrans_acl_token
        url = "/s10/p2/ftrans?op=%s&des=%s&acltoken=%s&mtime=%d" % (op, des, acl_token, mtime)

        resp = self._do_request(FTRANS_HTTP_METHOD_POST, url, conn=self._ftrans_s10_conn)
        if resp.status != FTRANS_HTTP_STATUS_OK:
            raise FtransHttpResponseException("invalid response status [%d] when make_dir_s10" % resp.status)

        return

    def _rename_file_s10(self, src, des):
        op = "rename_file"
        src = base64.b64encode(bytes(self._get_full_path(src), encoding="UTF-8")).decode(encoding="UTF-8")
        des = base64.b64encode(bytes(self._get_full_path(des), encoding="UTF-8")).decode(encoding="UTF-8")
        acl_token = self._ftrans_acl_token

        url = "/s10/p2/ftrans?op=%s&src=%s&des=%s&acltoken=%s" % (op, src, des, acl_token)

        resp = self._do_request(FTRANS_HTTP_METHOD_POST, url, conn=self._ftrans_s10_conn)
        if resp.status != FTRANS_HTTP_STATUS_OK:
            raise FtransHttpResponseException("invalid response status [%d] when rename_file_s10" % resp.status)

        return

    def _touch_file_s10(self, des, mtime):
        op = "touch_file"
        des = base64.b64encode(bytes(self._get_full_path(des), encoding="UTF-8")).decode(encoding="UTF-8")
        acl_token = self._ftrans_acl_token

        url = "/s10/p2/ftrans?op=%s&des=%s&acltoken=%s&mtime=%d" % (op, des, acl_token, mtime)

        resp = self._do_request(FTRANS_HTTP_METHOD_POST, url, conn=self._ftrans_s10_conn)
        if resp.status != FTRANS_HTTP_STATUS_OK:
            raise FtransHttpResponseException("invalid response status [%s] when touch_file_s10" % resp.status)

        return

    def upload_file(self, local_file_path, remote_file_path):
        if remote_file_path == "":
            raise FtransException("invalid des [%s]" % remote_file_path)
        remote_file_path = _to_slash(remote_file_path)
        if self._ftrans_client_enable():
            return self._upload_file_s2(local_file_path, remote_file_path)
        else:
            return self._upload_file_s10(local_file_path, remote_file_path)

    def download_file(self, local_file_path, remote_file_path):
        if remote_file_path == "":
            raise FtransException("invalid des [%s]" % remote_file_path)
        remote_file_path = _to_slash(remote_file_path)
        if self._ftrans_client_enable():
            return self._download_file_s2(local_file_path, remote_file_path)
        else:
            return self._download_file_s10(local_file_path, remote_file_path)

    def get_file_size(self, filename):
        if filename == "":
            raise FtransException("invalid des [%s]" % filename)
        filename = _to_slash(filename)
        if self._ftrans_client_enable():
            return self._get_file_size_s2(filename)
        else:
            return self._get_file_size_s10(filename)

    def get_file_md5(self, filename):
        # may be supported in future
        return None

    def remove_file(self, filename):
        if filename == "":
            raise FtransException("invalid des [%s]" % filename)
        filename = _to_slash(filename)
        if self._ftrans_client_enable():
            return self._remove_file_s2(filename)
        else:
            return self._remove_file_s10(filename)

    def list_file(self, prefix, filter_in=None, order_type=None, order_field=None, page_num=None, page_size=None):
        if prefix != "":
            prefix = _to_slash(prefix)
        if filter_in is None:
            filter_in = FTRANS_DEFAULT_FILTER_IN

        if order_type is None:
            order_type = FTRANS_ORDER_TYPE_ASC

        if order_field is None:
            order_field = FTRANS_ORDER_FIELD_NAME

        if page_num is None:
            page_num = FTRANS_DEFAULT_PAGE_NUM

        if page_size is None:
            page_size = FTRANS_DEFAULT_PAGE_SIZE

        if self._ftrans_client_enable():
            return self._list_file_s2(prefix, filter_in, order_type, order_field, page_num, page_size)
        else:
            return self._list_file_s10(prefix, filter_in, order_type, order_field, page_num, page_size)
