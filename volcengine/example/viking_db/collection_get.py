import utils

if __name__ == '__main__':
    vikingdb_service = utils.get_vikingdb_service()
    collection = vikingdb_service.get_collection("test_coll_for_sdk_with_vectorize")
    print(collection.collection_name)
    print(collection.description)
    print(collection.vectorize)