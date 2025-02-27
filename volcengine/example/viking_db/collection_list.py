import utils

if __name__ == '__main__':
    vikingdb_service = utils.get_vikingdb_service()
    collection_list = vikingdb_service.list_collections()
    for collection in collection_list:
        print(collection.collection_name)
        print(collection.description)
        print(collection.vectorize)