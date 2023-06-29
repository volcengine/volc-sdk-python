class SSEDecoder(object):
    def __init__(self, source):
        self.source = source

    def _read(self):
        data = b''
        for chunk in self.source:
            for line in chunk.splitlines(True):
                data += line
                if data.endswith((b'\r\r', b'\n\n', b'\r\n\r\n')):
                    yield data
                    data = b''
        if data:
            yield data

    def next(self):
        for chunk in self._read():
            for line in chunk.splitlines():
                # skip comment
                if line.startswith(b':'):
                    continue

                if b':' in line:
                    field, value = line.split(b':', 1)
                else:
                    field, value = line, b''

                if field == b'data' and len(value) > 0:
                    yield value
