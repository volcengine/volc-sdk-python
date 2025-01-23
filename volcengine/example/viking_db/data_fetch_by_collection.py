import utils

if __name__ == '__main__':
    vikingdb_service = utils.get_vikingdb_service()
    collection = vikingdb_service.get_collection("test_coll_for_sdk")
    datas = collection.fetch_data(["1", "2", "3"])
    for data in datas:
        print(data.id, data.fields, data.TTL)