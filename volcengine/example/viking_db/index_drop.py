import utils

if __name__ == '__main__':
    vikingdb_service = utils.get_vikingdb_service()
    collection = vikingdb_service.drop_index("test_coll_for_sdk_1", "index_sort_2")