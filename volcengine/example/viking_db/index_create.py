import utils
import volcengine.viking_db as vkdb

if __name__ == '__main__':
    vikingdb_service = utils.get_vikingdb_service()
    vector_index = vkdb.VectorIndexParams(distance=vkdb.DistanceType.COSINE, index_type=vkdb.IndexType.HNSW_HYBRID, quant=vkdb.QuantType.Int8)
    index = vikingdb_service.create_index("test_coll_for_sdk", "index_hnsw_hybrid", vector_index=vector_index)
    print(index.index_name)