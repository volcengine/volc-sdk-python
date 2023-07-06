# coding=utf-8
class MaasException(Exception):
    def __init__(self, code_n, code, message):
        self.code_n = code_n
        self.code = code
        self.message = message

    def __str__(self):
        return ("Detailed exception information is listed below.\n" + \
                            "code_n: {}\n" + \
                            "code: {}\n" + \
                            "message: {}").format(self.code_n, self.code, self.message)

def new_client_sdk_request_error(raw):
    return MaasException(1709701, "ClientSDKRequestError", "MaaS SDK request error: {}".format(raw))
