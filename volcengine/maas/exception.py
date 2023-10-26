# coding=utf-8
class MaasException(Exception):
    def __init__(self, code_n, code, message, req_id):
        self.code_n = code_n
        self.code = code
        self.message = message
        self.req_id = req_id

    def __str__(self):
        return ("Detailed exception information is listed below.\n" + \
                            "req_id: {}\n" + \
                            "code_n: {}\n" + \
                            "code: {}\n" + \
                            "message: {}").format(self.req_id, self.code_n, self.code, self.message)


def new_client_sdk_request_error(raw, req_id=""):
    return MaasException(1709701, "ClientSDKRequestError", "MaaS SDK request error: {}".format(raw), req_id)
