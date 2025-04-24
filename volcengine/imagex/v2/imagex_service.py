# coding:utf-8
from volcengine.imagex.v2.imagex_trait import ImagexTrait  # Modify it if necessary
from volcengine.imagex.v2.upload import Uploader
from volcengine.const.Const import *
from volcengine.imagex.v2.const import *
from volcengine.imagex.v2.helper.file_section_reader import FileSectionReader

from volcengine.util.Util import *
from volcengine.Policy import *

import threading
import os


class ImagexService(ImagexTrait):
    def __init__(self, region=REGION_CN_NORTH1, ak=None, sk=None):
        super().__init__(
            {
                "region": region,
                "ak": ak,
                "sk": sk,
            }
        )

    # upload
    def apply_upload(self, params):
        return self.imagex_get("ApplyImageUpload", params, doseq=1)

    def commit_upload(self, params, body):
        return self.imagex_post("CommitImageUpload", params, body)

    # upload local image file
    # noinspection DuplicatedCode
    def upload_image(self, params, file_paths):
        for p in file_paths:
            if not os.path.isfile(p):
                raise Exception("no such file on file path %s" % p)

        apply_upload_request = {
            "ServiceId": params["ServiceId"],
            "SessionKey": params.get("SessionKey", ""),
            "UploadNum": len(file_paths),
            "StoreKeys": params.get("StoreKeys", []),
            "Overwrite": str(params.get("Overwrite", False)),
        }
        resp = self.apply_upload(apply_upload_request)
        if "Error" in resp["ResponseMetadata"]:
            raise Exception(resp["ResponseMetadata"])

        result = resp["Result"]
        reqid = result["RequestId"]
        addr = result["UploadAddress"]
        if len(addr["UploadHosts"]) == 0:
            raise Exception("no upload host found, reqid %s" % reqid)
        elif len(addr["StoreInfos"]) != len(file_paths):
            raise Exception(
                "store info len %d != upload num %d, reqid %s"
                % (len(result["StoreInfos"]), len(file_paths), reqid)
            )

        session_key = addr["SessionKey"]
        host = addr["UploadHosts"][0]
        uploader = self.do_upload(file_paths, host, addr["StoreInfos"], params)
        if len(uploader.successOids) == 0:
            raise Exception("no file uploaded")

        if params.get("SkipCommit", False):
            return {"Results": uploader.results}
        commit_upload_request = {
            "ServiceId": params["ServiceId"],
            "SkipMeta": params.get("SkipMeta", False),
        }
        commit_upload_body = {
            "SessionKey": session_key,
            "SuccessOids": uploader.successOids,
            "Functions": params.get("Functions", []),
            "OptionInfos": params.get("OptionInfos", []),
        }
        resp = self.commit_upload(commit_upload_request, json.dumps(commit_upload_body))
        if "Error" in resp["ResponseMetadata"]:
            raise Exception(resp["ResponseMetadata"])
        return resp["Result"]

    # upload image data
    # noinspection DuplicatedCode
    def upload_image_data(self, params, img_datas):
        for data in img_datas:
            if not isinstance(data, bytes):
                raise Exception("upload of non-bytes not supported")

        apply_upload_request = {
            "ServiceId": params["ServiceId"],
            "SessionKey": params.get("SessionKey", ""),
            "UploadNum": len(img_datas),
            "StoreKeys": params.get("StoreKeys", []),
            "Overwrite": str(params.get("Overwrite", False)),
        }
        resp = self.apply_upload(apply_upload_request)
        if "Error" in resp["ResponseMetadata"]:
            raise Exception(resp["ResponseMetadata"])

        result = resp["Result"]
        reqid = result["RequestId"]
        addr = result["UploadAddress"]
        if len(addr["UploadHosts"]) == 0:
            raise Exception("no upload host found, reqid %s" % reqid)
        elif len(addr["StoreInfos"]) != len(img_datas):
            raise Exception(
                "store info len %d != upload num %d, reqid %s"
                % (len(result["StoreInfos"]), len(img_datas), reqid)
            )

        session_key = addr["SessionKey"]
        host = addr["UploadHosts"][0]
        uploader = self.do_upload(img_datas, host, addr["StoreInfos"], params)
        if len(uploader.successOids) == 0:
            raise Exception("no file uploaded")

        if params.get("SkipCommit", False):
            return {"Results": uploader.results}
        commit_upload_request = {
            "ServiceId": params["ServiceId"],
            "SkipMeta": params.get("SkipMeta", False),
        }
        commit_upload_body = {
            "SessionKey": session_key,
            "SuccessOids": uploader.successOids,
            "Functions": params.get("Functions", []),
            "OptionInfos": params.get("OptionInfos", []),
        }
        resp = self.commit_upload(commit_upload_request, json.dumps(commit_upload_body))
        if "Error" in resp["ResponseMetadata"]:
            raise Exception(resp["ResponseMetadata"])
        return resp["Result"]

    def vpc_upload_image(self, upload_request):
        if upload_request.get("FilePath", "") == "" and len(upload_request.get("Data", '')) == 0:
            raise Exception("filePath and data can not be empty at the same time")

        if upload_request.get("FilePath", "") != "" and len(upload_request.get("Data", '')) != 0:
            raise Exception("filePath and data can not be not empty at the same time")

        file_path = upload_request.get("FilePath", "")
        if file_path != "":
            if not os.path.isfile(file_path):
                raise Exception("no such file on file path")
            file_size = os.path.getsize(file_path)
            is_file = True
        else:
            file_size = len(upload_request.get("Data", []))
            is_file = False

        apply_vpc_request = {
            "ContentType": upload_request.get("ContentType", ""),
            "FileExtension": upload_request.get("FileExtension", ""),
            "FileSize": file_size,
            "PartSize": upload_request.get("PartSize", 0),
            "Prefix": upload_request.get("Prefix", ""),
            "ServiceId": upload_request.get("ServiceId"),
            "StorageClass": upload_request.get("StorageClass", ""),
            "StoreKey": upload_request.get("StoreKey", ""),
            "Overwrite": upload_request.get("Overwrite", False),
        }
        resp = self.apply_vpc_upload_info(apply_vpc_request)
        if "Error" in resp["ResponseMetadata"] or resp["Result"] is None or resp["Result"].get("UploadAddr") == "":
            raise Exception(resp["ResponseMetadata"])

        upload_addr = resp["Result"]
        file_info = {
            "FilePath": file_path,
            "Data": upload_request.get("Data"),
            "FileSize": file_size,
            "IsFile": is_file,
        }

        session_key = upload_addr["SessionKey"]

        commit_upload_request = {
            "ServiceId": upload_request["ServiceId"],
            "SkipMeta": upload_request.get("SkipMeta", False),
        }

        commit_upload_body = {
            "SessionKey": session_key,
            "SuccessOids": [],
            "Functions": upload_request.get("Functions", []),
            "OptionInfos": upload_request.get("OptionInfos", []),
        }

        try:
            self.vpc_upload(upload_addr, file_info)
        except Exception as e:
            self.commit_upload(commit_upload_request, json.dumps(commit_upload_body))
            raise Exception(e)

        successOids = [upload_addr.get("Oid")]
        commit_upload_body["SuccessOids"] = successOids
        resp = self.commit_upload(commit_upload_request, json.dumps(commit_upload_body))
        if "Error" in resp["ResponseMetadata"]:
            raise Exception(resp["ResponseMetadata"])
        return resp["Result"]

    def vpc_upload(self, vpc_upload_address, file_info):
        if vpc_upload_address.get("UploadMode") == "direct":
            self.vpc_put(vpc_upload_address, file_info)
        elif vpc_upload_address.get("UploadMode") == "part":
            self.vpc_part_upload(vpc_upload_address.get("PartUploadInfo"), file_info)
        else:
            raise Exception("unknown upload mode")

    def vpc_part_upload(self, part_upload_info, file_info):
        if part_upload_info is None:
            raise Exception("part upload info is empty")
        file_size = file_info.get("FileSize")
        chunk_size = part_upload_info.get("PartSize")
        total_num = file_size // chunk_size
        last_part_size = file_size % chunk_size
        part_put_urls = part_upload_info.get("PartPutURLs", [])
        if (last_part_size == 0 and total_num != len(part_put_urls) or (
                last_part_size != 0 and total_num + 1 != len(part_put_urls))):
            raise Exception("mismatch part upload urls")

        offset = 0
        etag_list = []
        for i in range(len(part_put_urls)):
            part_put_url = part_put_urls[i]
            if i == len(part_put_urls) - 1:
                chunk_size = file_size - offset
            if file_info.get("IsFile"):
                with open(file_info.get("FilePath"), 'rb') as f:
                    sr = FileSectionReader(f, chunk_size, init_offset=offset, can_reset=True)
                    etag = self.vpc_part_put(part_put_url, sr)
            else:
                etag = self.vpc_part_put(part_put_url, file_info.get("Data")[offset:offset + chunk_size])
            offset = offset + chunk_size
            etag_list.append(etag)

        post_data = self.vpc_generate_body(etag_list)
        post_url_headers_list = part_upload_info.get("CompletePartURLHeaders", [])
        post_headers = {}
        for post_url_header in post_url_headers_list:
            post_headers[post_url_header["Key"]] = post_url_header["Value"]
        self.vpc_post(part_upload_info.get("CompletePartURL"), post_data, post_headers)

    def vpc_post(self, post_url, data, headers):
        resp = self.session.post(post_url, data=data, headers=headers)
        if resp.status_code != 200:
            log_id = resp.headers.get("x-tos-request-id", "")
            raise Exception("vpc post error, logId: {}".format(log_id))

    def vpc_generate_body(self, etag_list):
        if len(etag_list) == 0:
            raise Exception('etag list empty')
        s = []
        for i in range(len(etag_list)):
            s.append("{" + '"PartNumber": {}, "ETag": {}'.format(i + 1, etag_list[i]) + "}")
        comma = ','

        return '{"Parts":[' + comma.join(s) + ']}'

    def vpc_part_put(self, part_put_url, content):
        resp = self.session.put(part_put_url, data=content)
        if resp.status_code != 200:
            log_id = resp.headers.get("x-tos-request-id", "")
            raise Exception("put error: code resp.status_code{} logId {}".format(resp.status_code, log_id))

        etag = resp.headers.get("ETag", "")
        return etag

    def vpc_put(self, vpc_upload_address, file_info):
        put_url = vpc_upload_address.get("PutURL")
        put_url_headers_list = vpc_upload_address.get("PutURLHeaders", [])
        put_headers = {}
        for put_url_header in put_url_headers_list:
            put_headers[put_url_header["Key"]] = put_url_header["Value"]

        if file_info.get("IsFile"):
            with open(file_info.get("FilePath"), 'rb') as f:
                resp = self.session.put(put_url, headers=put_headers, data=f)
        else:
            resp = self.session.put(put_url, headers=put_headers, data=file_info.get("Data"))

        if resp.status_code != 200:
            log_id = resp.headers.get("x-tos-request-id", "")
            raise Exception("put error: code resp.status_code{} logId {}".format(resp.status_code, log_id))

    def do_upload(self, file_paths_or_bytes, host, store_infos, params=None):
        threads = []
        uploader = Uploader(self, host, store_infos, file_paths_or_bytes, params)
        for i in range(UPLOAD_THREADS):
            thread = threading.Thread(target=uploader.async_upload)
            thread.start()
            threads.append(thread)
        for i in range(UPLOAD_THREADS):
            threads[i].join()
        return uploader

    def get_upload_auth_token(self, params):
        apply_token = self.get_sign_url("ApplyImageUpload", params)
        commit_token = self.get_sign_url("CommitImageUpload", params)

        ret = {
            "Version": "v1",
            "ApplyUploadToken": apply_token,
            "CommitUploadToken": commit_token,
        }
        data = json.dumps(ret)
        if sys.version_info[0] == 3:
            return base64.b64encode(data.encode("utf-8")).decode("utf-8")
        else:
            return base64.b64encode(data.decode("utf-8"))

    # tag 字段如下，可选择所需字段传入
    # upload_policy_dict = {
    #     "FileSizeUpLimit": "xxx",
    #     "FileSizeBottomLimit": "xxx",
    #     "ContentTypeBlackList":[
    #         "xxx"
    #     ],
    #     "ContentTypeWhiteList":[
    #         "xxx"
    #     ]
    # }
    # policy_str = json.dumps(upload_policy_dict)
    #
    # tag = {
    #     "UploadOverwrite": "true",
    #     "UploadPolicy": policy_str,
    # }
    def get_upload_auth(self, service_ids, expire=60 * 60, key_ptn="", tag=dict):
        apply_res = []
        commit_res = []
        if len(service_ids) == 0:
            apply_res.append(ResourceServiceIdTRN % "*")
            commit_res.append(ResourceServiceIdTRN % "*")
        else:
            for sid in service_ids:
                apply_res.append(ResourceServiceIdTRN % sid)
                commit_res.append(ResourceServiceIdTRN % sid)
        apply_res.append(ResourceStoreKeyTRN % key_ptn)

        inline_policy = Policy(
            [
                Statement.new_allow_statement(["ImageX:ApplyImageUpload"], apply_res),
                Statement.new_allow_statement(["ImageX:CommitImageUpload"], commit_res),
            ]
        )
        for k, v in tag.items():
            inline_policy.statements.append(
                Statement.new_allow_statement([k], [str(v)])
            )
        return self.sign_sts2(inline_policy, expire)
