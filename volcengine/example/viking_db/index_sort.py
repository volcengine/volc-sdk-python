import utils

if __name__ == '__main__':
    vikingdb_service = utils.get_vikingdb_service()
    index = vikingdb_service.get_index("test_coll_for_sdk_1", "index_sort")

    index_sort_result = index.sort(query_vector=[0.0, 1.1, 2.2, -1.1], primary_keys=["docx", "doc1", "doc2", "doc3", "doc0"])
    print(index_sort_result.primary_key_not_exist)
    for item in index_sort_result.sort_result:
        print(item.primary_key, item.score)