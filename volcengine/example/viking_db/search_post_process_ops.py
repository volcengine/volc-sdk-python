import utils

if __name__ == '__main__':
    vikingdb_service = utils.get_vikingdb_service()
    index = vikingdb_service.get_index("test_coll_for_sdk", "index_hnsw")
    datas = index.search(order=None, limit=5, post_process_input_limit=5,
                         post_process_ops=[
                             {'op': 'string_like', 'field':'f_string', 'pattern':'%doc9%'},
                             {'op': 'enum_freq_limiter', 'field':'f_string', 'threshold': 1}
                         ])
    for data in datas:
        print(data.id, data.fields, data.score)