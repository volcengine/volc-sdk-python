# coding:utf-8
import json
import os
import threading
from volcengine.const.Const import *
from volcengine.util.Util import *
from volcengine.Policy import *
from volcengine.imagex.v2.const import *

from retry import retry
from urllib.parse import quote

try:
    import queue
except ImportError:
    import Queue as queue


class Uploader:
    def __init__(
            self, imagex_service, host, store_infos=None, file_paths_or_bytes=None, params=None
    ):
        if store_infos is None:
            store_infos = []
        if file_paths_or_bytes is None:
            file_paths_or_bytes = []
        if params is None:
            params = {}

        self.imagex_service = imagex_service
        self.host = host
        self.store_infos = store_infos
        self.file_paths_or_bytes = file_paths_or_bytes
        self.content_types = params.get("ContentTypes", [])
        self.storage_classes = params.get("StorageClasses", [])
        self.upload_host = params.get("UploadHost", "")
        if self.upload_host != "":
            self.host = self.upload_host

        self.queue = queue.Queue()
        self.queue_lock = threading.Lock()

        self.successOids = []
        self.results = []

        for i in range(len(store_infos)):
            self.queue.put(i)

    def async_upload(self):
        while not self.queue.empty():
            self.queue_lock.acquire()
            if self.queue.empty():
                self.queue_lock.release()
                break
            idx = self.queue.get()
            self.queue_lock.release()

            store_info = self.store_infos[idx]
            file_paths_or_bytes = self.file_paths_or_bytes[idx]
            param = {}
            if len(self.content_types) > idx:
                param["ContentType"] = self.content_types[idx]
            if len(self.storage_classes) > idx:
                param["StorageClass"] = self.storage_classes[idx]

            try:
                if isinstance(file_paths_or_bytes, bytes):
                    self.upload_by_host(store_info, file_paths_or_bytes, param)
                elif isinstance(file_paths_or_bytes, str):
                    file_path = file_paths_or_bytes
                    file_size = os.path.getsize(file_path)
                    data = open(file_path, "rb")
                    if file_size < MinChunkSize:
                        self.upload_by_host(store_info, data.read(), param)
                    elif file_size > LargeFileSize or self.upload_host != "":
                        self.chunk_upload(store_info, data, file_size, True, param)
                    else:
                        self.chunk_upload(store_info, data, file_size, False, param)
                    data.close()
                else:
                    raise Exception("Uploader only accept bytes or path data")
                self.successOids.append(store_info["StoreUri"])
                self.results.append(
                    {
                        "Uri": store_info["StoreUri"],
                        "UriStatus": 2000,
                    }
                )
            except Exception as e:
                self.results.append(
                    {
                        "Uri": store_info["StoreUri"],
                        "UriStatus": 2001,
                        "Error": e,
                    }
                )

    @retry(tries=3, delay=1, backoff=2)
    def upload_by_host(self, store_info, img_data, param=None):
        if param is None:
            param = {}
        url = "https://{}/{}".format(self.host, quote(store_info["StoreUri"]))
        check_sum = crc32(img_data) & 0xFFFFFFFF
        check_sum = "%08x" % check_sum
        headers = {"Content-CRC32": check_sum, "Authorization": store_info["Auth"]}
        if param.get("ContentType", "") != "":
            headers["Specified-Content-Type"] = param["ContentType"]
        if param.get("StorageClass", "") != "":
            headers["X-VeImageX-Storage-Class"] = param["StorageClass"]
        upload_status, resp = self.imagex_service.put_data(url, img_data, headers)
        if not upload_status:
            raise Exception(
                "upload by host: upload url %s status false, resp: %s" % (url, resp)
            )

    def chunk_upload(self, store_info, f, size, is_large_file, param=None):
        if param is None:
            param = {}
        upload_id = self.init_upload_part(store_info, is_large_file, param)
        n = size // MinChunkSize
        last_num = n - 1
        parts = []
        for i in range(0, last_num):
            data = f.read(MinChunkSize)
            part_number = i
            if is_large_file:
                part_number = i + 1
            part = self.upload_part(
                store_info, upload_id, part_number, data, is_large_file
            )
            parts.append(part)
        data = f.read()
        if is_large_file:
            last_num = last_num + 1
        part = self.upload_part(store_info, upload_id, last_num, data, is_large_file)
        parts.append(part)
        return self.upload_merge_part(store_info, upload_id, parts, is_large_file, param)

    @retry(tries=3, delay=1, backoff=2)
    def init_upload_part(self, store_info, is_large_file, param=None):
        if param is None:
            param = {}
        url = "https://{}/{}?uploads".format(self.host, quote(store_info["StoreUri"]))
        headers = {"Authorization": store_info["Auth"]}
        if is_large_file:
            headers["X-Storage-Mode"] = "gateway"
        if param.get("ContentType", "") != "":
            headers["Specified-Content-Type"] = param["ContentType"]
        if param.get("StorageClass", "") != "":
            headers["X-VeImageX-Storage-Class"] = param["StorageClass"]
        upload_status, resp = self.imagex_service.put_data(url, None, headers)
        resp = json.loads(resp)
        if not upload_status:
            raise Exception("init upload error")
        if resp.get("success") is None or resp["success"] != 0:
            raise Exception("init upload error")
        return resp["payload"]["uploadID"]

    @retry(tries=3, delay=1, backoff=2)
    def upload_part(self, store_info, upload_id, part_number, data, is_large_file):
        url = "https://{}/{}?partNumber={}&uploadID={}".format(
            self.host, quote(store_info["StoreUri"]), part_number, upload_id
        )
        check_sum = crc32(data) & 0xFFFFFFFF
        check_sum = "%08x" % check_sum
        headers = {"Content-CRC32": check_sum, "Authorization": store_info["Auth"]}
        if is_large_file:
            headers["X-Storage-Mode"] = "gateway"
        upload_status, resp = self.imagex_service.put_data(url, data, headers)
        if not upload_status:
            raise Exception(url + json.dumps(resp))
        resp = json.loads(resp)
        if resp.get("success") is None or resp["success"] != 0:
            raise Exception("upload part error")
        return check_sum

    # noinspection DuplicatedCode
    @staticmethod
    def generate_merge_body(check_sum_list):
        if len(check_sum_list) == 0:
            raise Exception("crc32 list empty")
        s = []
        for i in range(len(check_sum_list)):
            s.append("{}:{}".format(i, check_sum_list[i]))
        comma = ","
        return comma.join(s)

    @retry(tries=3, delay=1, backoff=2)
    def upload_merge_part(self, store_info, upload_id, check_sum_list, is_large_file, param=None):
        if param is None:
            param = {}
        url = "https://{}/{}?uploadID={}".format(
            self.host, quote(store_info["StoreUri"]), upload_id
        )
        data = self.generate_merge_body(check_sum_list)
        headers = {"Authorization": store_info["Auth"]}
        if is_large_file:
            headers["X-Storage-Mode"] = "gateway"
        if param.get("ContentType", "") != "":
            headers["Specified-Content-Type"] = param["ContentType"]
        if param.get("StorageClass", "") != "":
            headers["X-VeImageX-Storage-Class"] = param["StorageClass"]
        upload_status, resp = self.imagex_service.put_data(url, data, headers)
        resp = json.loads(resp)
        if not upload_status:
            raise Exception("init upload error")
        if resp.get("success") is None or resp["success"] != 0:
            raise Exception("init upload error")
