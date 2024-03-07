from typing import Iterator, Optional


class BinaryResponseContent:
    def __init__(self, response, request_id) -> None:
        self.response = response
        self.request_id = request_id

    def stream_to_file(
            self,
            file: str
    ) -> None:
        with open(file, mode="wb") as f:
            for data in self.response:
                f.write(data)

    def iter_bytes(self) -> Iterator[bytes]:
        for data in self.response:
            yield data
