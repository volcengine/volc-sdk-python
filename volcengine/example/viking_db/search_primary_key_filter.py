import utils

if __name__ == '__main__':
    vikingdb_service = utils.get_vikingdb_service()
    index = vikingdb_service.get_index("test_coll_for_sdk", "index_hnsw")

    datas = index.search(order=None, limit=5, primary_key_in=[1, 2, 3, 4, 5, 6, 7, 8, 9, 10], primary_key_not_in=[1])
    for data in datas:
        print(data.id, data.fields, data.score)
    print("========================")

    datas = index.search_by_id(id=2, limit=5, output_fields=["f_id", 'f_vector'],  primary_key_in=[1, 2, 3, 4, 5, 6, 7, 8, 9, 10], primary_key_not_in=[1])
    for data in datas:
        print(data.id, data.fields, data.score)
    print("========================")

    datas = index.search_by_vector(vector=[0,0,0,0], limit=10, primary_key_in=[1, 2, 3, 4, 5, 6, 7, 8, 9, 10], primary_key_not_in=[5, 6, 7, 8, 9, 10])
    for data in datas:
        print(data.id, data.fields, data.score)
    print("========================")

