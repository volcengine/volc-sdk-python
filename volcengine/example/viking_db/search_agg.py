import utils

if __name__ == '__main__':
    vikingdb_service = utils.get_vikingdb_service()
    index = vikingdb_service.get_index("test_coll_for_sdk", "index_hnsw_hybrid")

    agg_result = index.search_agg(agg={'op':'count'})
    print(agg_result.agg_op, agg_result.group_by_field, agg_result.agg_result)
    print("==========")

    agg_result = index.search_agg(agg={'op': 'count', 'field': 'f_string', 'cond': {'gt': 0}}, filter={'op': 'range', 'field': 'f_int64', 'gt': 90})
    print(agg_result.agg_op, agg_result.group_by_field, agg_result.agg_result)