from typing import Iterator, Optional

from volcengine.maas.exception import new_client_sdk_request_error, MaasException
from volcengine.maas.utils import json_to_object


class BinaryResponseContent:
    def __init__(self, response, request_id) -> None:
        self.response = response
        self.request_id = request_id

    def stream_to_file(
            self,
            file: str
    ) -> None:
        is_first = True
        error_bytes = b''
        with open(file, mode="wb") as f:
            for data in self.response:
                if len(error_bytes) > 0 or (is_first and "\"error\":" in str(data)):
                    error_bytes += data
                else:
                    f.write(data)

        if len(error_bytes) > 0:
            resp = json_to_object(str(error_bytes, encoding="utf-8"), req_id=self.request_id)
            raise MaasException(
                resp.error.code_n, resp.error.code, resp.error.message, self.request_id
            )

    def iter_bytes(self) -> Iterator[bytes]:
        for data in self.response:
            yield data
