from io import BytesIO

import avro.schema
from avro.io import DatumReader, BinaryDecoder

RecordSchema: str = "com.bytedance.dts.subscribe.avro.Record"


class RecordDeserializer:
    # schema_file: path of schema file
    def __init__(self, schema_file: str):
        s = avro.schema.parse(open(schema_file, "rb").read())
        self.all_schema = s
        for schema in self.all_schema.schemas:
            if isinstance(schema, avro.schema.RecordSchema) and schema.fullname == RecordSchema:
                self.record_schema = schema
                break

    def deserialize(self, data: bytes) -> dict:
        bio = BytesIO(initial_bytes=data)
        decoder = BinaryDecoder(bio)
        res = DatumReader(writers_schema=self.record_schema).read(decoder)
        return res
