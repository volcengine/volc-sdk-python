# coding:utf-8
from volcengine.imagex.v2.imagex_trait import ImagexTrait  # Modify it if necessary
from volcengine.imagex.v2.upload import Uploader
from volcengine.const.Const import *
from volcengine.imagex.v2.const import *

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
        uploader = self.do_upload(file_paths, host, addr["StoreInfos"])
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
        uploader = self.do_upload(img_datas, host, addr["StoreInfos"])
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

    def do_upload(self, file_paths_or_bytes, host, store_infos):
        threads = []
        uploader = Uploader(self, host, store_infos, file_paths_or_bytes)
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
