# coding=utf-8
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import json
from json import JSONDecodeError

from requests import Response

from volcengine.tls.const import *


class TLSException(Exception):
    def __init__(self, response: Response = None, error_code: str = None, error_message: str = None):
        if response is not None:
            self.http_code = response.status_code
            self.response_header = response.headers
            self.request_id = response.headers.get(X_TLS_REQUEST_ID)

            try:
                response_body = json.loads(response.text)
                self.error_code = response_body["ErrorCode"]
                self.error_message = response_body["ErrorMessage"]
            except JSONDecodeError:
                self.error_code = response.text
                self.error_message = response.text
        else:
            self.error_code = error_code
            self.error_message = error_message

    def __str__(self):
        exception_info = "Detailed exception information is listed below."

        if "request_id" in self.__dict__:
            exception_info += "\nRequestId: {}\nHTTP status code: {}".format(self.request_id, self.http_code)

        exception_info += "\nErrorCode: {}\nErrorMessage: {}".format(self.error_code, self.error_message)

        return exception_info
