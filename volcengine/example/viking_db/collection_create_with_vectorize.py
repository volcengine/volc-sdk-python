import utils
import volcengine.viking_db as vkdb

if __name__ == '__main__':
    vikingdb_service = utils.get_vikingdb_service()
    fields = [
        vkdb.Field(field_name="f_id", field_type=vkdb.FieldType.String, is_primary_key=True),
        vkdb.Field(field_name="f_string", field_type=vkdb.FieldType.String, default_val=""),
        vkdb.Field(field_name="f_text1", field_type=vkdb.FieldType.Text),
        vkdb.Field(field_name="f_text2", field_type=vkdb.FieldType.Text),
        vkdb.Field(field_name="f_image1", field_type=vkdb.FieldType.Image),
        vkdb.Field(field_name="f_image2", field_type=vkdb.FieldType.Image),
    ]
    vectorize = [vkdb.VectorizeTuple(
        dense=vkdb.VectorizeModelConf(
            model_name="doubao-embedding-vision",
            model_version="241215",
            text_field="f_text1",
            image_field="f_image1",
            dim=3072,
        ),
        sparse=vkdb.VectorizeModelConf(
            model_name="bge-m3",
            text_field="f_text1",
        )
    )]

    collection = vikingdb_service.create_collection("test_coll_for_sdk_with_vectorize",
                                                    fields=fields, description="test for sdk", vectorize=vectorize)
    print(collection.collection_name)
    print(collection.description)
    print(collection.vectorize)
