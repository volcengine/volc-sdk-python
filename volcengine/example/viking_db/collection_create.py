import utils
import volcengine.viking_db as vkdb

if __name__ == '__main__':
    vikingdb_service = utils.get_vikingdb_service()
    fields = [
        vkdb.Field(field_name="f_id", field_type=vkdb.FieldType.String, is_primary_key=True),
        vkdb.Field(field_name="f_string", field_type=vkdb.FieldType.String, default_val=""),
        vkdb.Field(field_name="f_int64", field_type=vkdb.FieldType.Int64, default_val=0),
        vkdb.Field(field_name="f_text", field_type=vkdb.FieldType.Text, default_val=0, pipeline_name="text_doubao_embedding_and_m3"),
    ]

    collection = vikingdb_service.create_collection("test_coll_for_sdk", fields=fields, description="test for sdk")
    print(collection.collection_name)
    print(collection.description)
