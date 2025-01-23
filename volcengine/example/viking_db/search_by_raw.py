import utils
import volcengine.viking_db as vkdb

if __name__ == '__main__':
    vikingdb_service = utils.get_vikingdb_service()
    index = vikingdb_service.get_index("test_coll_for_sdk", "index_hnsw_hybrid")
    datas = index.search_by_text(text=vkdb.Text(text="ecjghdjeichjghdaceajfejecfcfdghhiadcaachdhdfjjcecc"),
                                 limit=5, need_instruction=False, primary_key_in=["1", "2", "3", "4"])
    for data in datas:
        print(data.id, data.fields, data.score)