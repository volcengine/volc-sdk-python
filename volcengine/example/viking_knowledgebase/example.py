import sys
import os

current_directory = os.path.dirname(os.path.abspath(__file__))
seek = os.path.dirname(os.path.dirname(os.path.dirname(current_directory)))  
sys.path.insert(0, seek)

from volcengine.viking_knowledgebase import VikingKnowledgeBaseService, Collection, Doc, Point
from volcengine.viking_knowledgebase.common import Field, FieldType, IndexType, EmbddingModelType


collection_name = "test_sdks"

viking_knowledgebase_service = VikingKnowledgeBaseService()
points = viking_knowledgebase_service.search_collection(collection_name=collection_name,query="银屑病是什么？")
for point in points:
    print(point.content)
    print(point.chunk_id)
    print(point.point_id)
    print("=======")
# c = Collection(vikingkb_service, collection_name)
# tos_path = "viking-db-tos/djk_test/test_0401/"
# c.add_doc(add_type="tos", tos_path=tos_path)

# 默认参数构建知识库
# my_collection = vikingkb_service.create_collection(collection_name)

# 自定义index配置、preprocess文档配置构建知识库
# index = {
#    "index_type": IndexType.HNSW_HYBRID,
#    "index_config": {
#         "fields": [{
#             "field_name": "chunk_len",
#             "field_type": FieldType.Int64,
#             "default_val": 0
#             }],
#         "cpu_quota": 1,
#         "embedding_model":EmbddingModelType.EmbeddingModelBgeLargeZhAndM3
#   }
# }
# preprocessing = {
#     "chunk_length" :200
# }
# my_collection = vikingkb_service.create_collection(collection_name=collection_name, index=index, preprocessing=preprocessing)

# 获取collection详细信息

# my_collection = vikingkb_service.get_collection(collection_name=collection_name)



# 由tos路径上传doc
# tos_path = "viking-db-tos/djk_test/test_0329/"
# my_collection.add_doc(add_type="tos", tos_path=tos_path)

# 由url上传doc
# url = "https://viking-db-tos.tos-cn-beijing.volces.com/hax_test/1151064.doc"
# my_collection.add_doc(add_type="url", doc_id="t01", doc_name="test_doc", doc_type="doc", url=url)

# 查询
# query = "周杨被罚了几年"
# points = vikingkb_service.search_collection(collection_name=collection_name, query=query)

# for point in points:
#     print(point.content)
#     print(point.score)