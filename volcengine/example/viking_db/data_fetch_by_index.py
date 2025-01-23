import utils

if __name__ == '__main__':
    vikingdb_service = utils.get_vikingdb_service()
    index = vikingdb_service.get_index("test_coll_for_sdk", "index_hnsw_hybrid")
    datas = index.fetch_data(["1", "2", "3"])
    for data in datas:
        print(data.id, data.fields)