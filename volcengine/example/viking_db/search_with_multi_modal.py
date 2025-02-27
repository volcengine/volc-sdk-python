import utils

if __name__ == '__main__':
    vikingdb_service = utils.get_vikingdb_service()
    index = vikingdb_service.get_index("test_coll_for_sdk_with_vectorize", "index_hnsw_hybrid")
    datas = index.search_with_multi_modal(
        text="这是一个测试",
        image="tos://{your_bucket}/{your_object}",
        limit=5,
        need_instruction=False)
    for data in datas:
        print(data.id, data.fields, data.score)