import asyncio
import base64
import os, sys
import random

from volcengine.viking_db import *

sys.path.insert(0, "/data00/home/xiejianqiao.1027/project/volc-sdk-python/volcengine")

# from ...viking_db import VikingDBService, Field, FieldType
# from ../../viking_db import *


if __name__ == '__main__':
    vikingdb_service = VikingDBService()
    vikingdb_service.set_ak()
    vikingdb_service.set_sk()

    # id = vikingdb_service.create_task(TaskType.Filter_Delete, {"collection_name": "example", "filter": {"like": [2]}})
    # print(id)

    # res = vikingdb_service.update_task("ae6f9a4e-9a68-5374-9687-36017c1ddd3e", task_status=TaskStatus.Confirmed)

    # id = vikingdb_service.create_task(TaskType.Data_Import, {"tos_path": "demo-1028/demo_1030", "file_type":"json", "ignore_error":False, "collection_name":"sparse"})
    # print(id)

    # task = vikingdb_service.get_task("bc5e952d-3f95-5e0c-b310-548933890308")
    # print(task.task_status)

    # tasks = vikingdb_service.list_tasks()
    # for item in tasks:
    #     print(item.process_info)

    # res = vikingdb_service.drop_task("01f7f554-46b9-55d6-af6c-b2aa9502d229")



    # dense_sparse
    # fields = [
    #     Field(
    #         field_name="id",
    #         field_type=FieldType.String,
    #         is_primary_key=True
    #     ),
    #     Field(
    #         field_name="vector",
    #         field_type=FieldType.Vector,
    #         dim=10
    #     ),
    #     Field(
    #         field_name="sparse",
    #         field_type=FieldType.Sparse_Vector,
    #         default_val=0
    #     ),
    # ]
    # res = vikingdb_service.create_collection("sparse", fields)
    # print(res)

    # res = vikingdb_service.get_collection("sparse")
    # for item in res.fields:
    #     print(item.field_type, item.field_name)

    def gen_random_vector(dim):
        res = [0, ] * dim
        for i in range(dim):
            res[i] = random.random() - 0.5
        return res


    # collection = vikingdb_service.get_collection("sparse")
    # field1 = {"id": "111", "vector": gen_random_vector(10), "sparse": {"hello1": 0.01, "world1": 0.02}}
    # field2 = {"id": "222", "vector": gen_random_vector(10), "sparse": {"hello2": 0.02, "world2": 0.03}}
    # field3 = {"id": "333", "vector": gen_random_vector(10), "sparse": {"hello3": 0.03, "world3": 0.04}}
    # field4 = {"id": "444", "vector": gen_random_vector(10), "sparse": {"hello4": 0.04, "world4": 0.05}}
    # data1 = Data(field1)
    # data2 = Data(field2)
    # data3 = Data(field3)
    # data4 = Data(field4)
    # datas = [data1, data2, data3, data4]
    # collection.upsert_data(datas)

    # collection = vikingdb_service.get_collection("example")
    # res = collection.fetch_data(555)
    # print(res.fields)

    # vector_index = VectorIndexParams(distance=DistanceType.COSINE, index_type=IndexType.HNSW_HYBRID,
    #                                  quant=QuantType.Float)
    # res = vikingdb_service.create_index("sparse", "sparse", vector_index)

    # res = vikingdb_service.get_index("sparse", "sparse")
    # print(res.vector_index)

    # index = vikingdb_service.get_index("sparse_go", "sparse_go_test5")
    # res = index.search_by_vector(vector=gen_random_vector(12), sparse_vectors={"he": 0.05}, dense_weight=0.1, retry=True)
    # print(res)

    # index = vikingdb_service.get_index("sparse_go", "sparse_go_test5")
    # res = index.search_by_id("111", dense_weight=0.1)
    # print(res)

    # index = vikingdb_service.get_index("sparse", "sparse")
    # res = index.search_by_id("111", dense_weight=0.1)
    # print(res)

    # index = vikingdb_service.get_index("sparse", "sparse")
    # res = index.search(VectorOrder(vector=gen_random_vector(10), sparse_vectors={"he": 0.05}), dense_weight=0.1)
    # print(res)

    # list = [RawData("text", "hello1"), RawData("text", "hello2")]
    # res = vikingdb_service.embedding_v2(EmbModel("bge-m3"), list)
    # print(res)

    # datas = [{
    #     "query": "退改",
    #     "content": "如果您需要人工服务，可以拨打人工客服电话：4006660921",
    #     "title": "无"
    # }, {
    #     "query": "退改",
    #     "content": "1、1日票 1.5日票 2日票的退款政策： -到访日前2天的00:00前，免费退款 - 到访日前2天的00:00至到访日前夜23:59期间,退款需扣除服务费（人民币80元） - 到访日当天（00:00 之后），不可退款 2、半日票的退款政策： - 未使用的们票可在所选入...",
    #     "title": "门票退改政策｜北京环球影城的门票退改政策"
    # }, {
    #     "query": "退改",
    #     "content": "如果您需要人工服务，可以拨打人工客服电话：4006660921",
    # }]
    # res = vikingdb_service.batch_rerank(datas)
    # print(res)

    # 写给用户的样例
    # fields = [
    #     Field(
    #         field_name="doc_id",
    #         field_type=FieldType.String,
    #         is_primary_key=True
    #     ),
    #     Field(
    #         field_name="text_vector",
    #         field_type=FieldType.Vector,
    #         dim=12
    #     ),
    #     Field(
    #         field_name="like",
    #         field_type=FieldType.Int64,
    #         default_val=0
    #     ),
    #     Field(
    #         field_name="price",
    #         field_type=FieldType.Float32,
    #         default_val=0
    #     ),
    #     Field(
    #         field_name="author",
    #         field_type=FieldType.List_String,
    #         default_val=[]
    #     ),
    #     Field(
    #         field_name="aim",
    #         field_type=FieldType.Bool,
    #         default_val=True
    #     ),
    # ]
    # res = vikingdb_service.create_collection("example", fields, "This is an example")
    # # 返回一个collection实例
    # print(res)
    #
    # res = vikingdb_service.get_collection("example")
    # # 返回一个collection实例
    # print(res.update_person)
    # #
    # vikingdb_service.drop_collection("example")  # 无返回
    #
    # res = vikingdb_service.list_collections()
    # 返回一个列表
    # for item in res:
    #     print(item.indexes)

    #
    # vector_index = VectorIndexParams(distance=DistanceType.COSINE,index_type=IndexType.DiskANN,
    #                                  quant=QuantType.Float)
    # res = vikingdb_service.create_index("example1","example1", vector_index, cpu_quota=2,
    #                                     description="This is an index", scalar_index=['price', 'like'], shard_policy=ShardType.Custom, shard_count=10)
    # # 返回一个index实例
    # print(res)
    #
    # res = vikingdb_service.get_index("example", "example")
    # 返回一个index实例
    # print(res.shard_count, res.shard_policy)
    #
    # vikingdb_service.drop_index("example", "example")  # 无返回
    #
    # res = vikingdb_service.list_indexes("example")
    # 返回一个列表
    # for item in res:
    #     print(item.shard_count)
    #     print(item.shard_policy)
    #     print(item.update_time)
    #     print(item.create_time)
    #
    # def gen_random_vector(dim):
    #     res = [0, ] * dim
    #     for i in range(dim):
    #         res[i] = random.random() - 0.5
    #     return res
    # collection = vikingdb_service.get_collection("example")
    # field1 = {"doc_id": "111", "text_vector": gen_random_vector(12), "like": 1, "price": 1.11,
    #           "author": ["gy"], "aim": True}
    # field2 = {"doc_id": "222", "text_vector": gen_random_vector(12), "like": 2, "price": 2.22,
    #           "author": ["gy", "xjq"], "aim": False}
    # field3 = {"doc_id": "333", "text_vector": gen_random_vector(12), "like": 3, "price": 3.33,
    #           "author": ["gy", "xjq"], "aim": False}
    # field4 = {"doc_id": "444", "text_vector": gen_random_vector(12), "like": 4, "price": 4.44,
    #           "author": ["gy", "xjq"], "aim": False}
    # data1 = Data(field1)
    # data2 = Data(field2)
    # data3 = Data(field3)
    # data4 = Data(field4)
    # datas = []
    # datas.append(data1)
    # datas.append(data2)
    # datas.append(data3)
    # datas.append(data4)
    # collection.upsert_data(datas)  # 无返回

    #
    # collection = vikingdb_service.get_collection("example")
    # res = collection.fetch_data("333")
    # print(res.fields)
    # res = collection.fetch_data(["111", "222", "333", "444"])
    # # 返回一个列表
    # for item in res:
    #     print(item)
    #     print(item.fields)
    #
    # collection = vikingdb_service.get_collection("example")
    # collection.delete_data("11")  # 无返回
    #
    # index = vikingdb_service.get_index("sparse_go", "sparse_go_test5")
    # res = index.fetch_data(["111"])
    # # 返回一个列表
    # for item in res:
    #     print(item)
    #     print(item.fields)
    #
    # index = vikingdb_service.get_index("sparse_go", "sparse_go_test5")
    # res = index.search_by_vector(gen_random_vector(10), sparse_vectors={'1':1.1})
    # # 返回一个列表
    # print(res)

    # index = vikingdb_service.get_index("example", "example_index")
    # def gen_random_vector(dim):
    #     res = [0, ] * dim
    #     for i in range(dim):
    #         res[i] = random.random() - 0.5
    #     return res
    # res = index.search_by_vector(gen_random_vector(10), limit=2, output_fields=["doc_id", "like", "text_vector"],
    #                              )
    # 返回一个列表
    # for item in res:
    #     print(item)
    #     print(item.score)
    #
    # index = vikingdb_service.get_index("example", "example_index")
    # def gen_random_vector(dim):
    #     res = [0, ] * dim
    #     for i in range(dim):
    #         res[i] = random.random() - 0.5
    #     return res
    # res = index.search(order=VectorOrder(gen_random_vector(10)), limit=2,
    #                    output_fields=["doc_id", "like", "text_vector"],
    #                     filter={"op": "range", "field": "price", "lt": 3.5})
    # 返回一个列表
    # for item in res:
    #     print(item)
    #     print(item.score)
    # res = index.search(order=ScalarOrder("price", Order.Desc), limit=6,
    #                    output_fields=["price"],
    #                    filter={"op": "range", "field": "price", "lt": 5})
    # # 返回一个列表
    # for item in res:
    #     print(item)
    #     print(item.score)
    # index = vikingdb_service.get_index("example", "example_index")
    # res = index.search(limit=5, output_fields=["doc_id", "like"],
    #                 filter={"op": "range", "field": "price", "lt": 3.5})
    # 返回一个列表
    # for item in res:
    #     print(item.fields)
    #     print(item.score)
    #
    # 含有text字段的测试
    # fields = [
    #     Field(
    #         field_name="doc_id",
    #         field_type=FieldType.String,
    #         is_primary_key=True
    #     ),
    #     Field(
    #         field_name="text",
    #         field_type=FieldType.Text,
    #         pipeline_name="text_split_bge_large_zh"
    #     ),
    #     Field(
    #         field_name="like",
    #         field_type=FieldType.Int64,
    #         default_val=0
    #     ),
    #     Field(
    #         field_name="price",
    #         field_type=FieldType.Float32,
    #         default_val=0
    #     ),
    #     Field(
    #         field_name="author",
    #         field_type=FieldType.List_String,
    #         default_val=[]
    #     ),
    #     Field(
    #         field_name="aim",
    #         field_type=FieldType.Bool,
    #         default_val=True
    #     ),
    # ]
    # res = vikingdb_service.create_collection("example_text", fields, "This is an example include text")
    #
    # vector_index = VectorIndexParams(distance=DistanceType.IP, index_type=IndexType.FLAT,
    #                                  quant=QuantType.Int8)
    # res = vikingdb_service.create_index("example", "example1")
    #
    # collection = vikingdb_service.get_collection("example_text")
    # field1 = {"doc_id": "11", "text": {"text":"this is one"}, "like": 1, "price": 1.11,
    #           "author": ["gy"], "aim": True}
    # field2 = {"doc_id": "22", "text": {"text":"this is two"}, "like": 2, "price": 2.22,
    #           "author": ["gy", "xjq"], "aim": False}
    # field3 = {"doc_id": "33", "text": {"text":"this is three"}, "like": 1, "price": 3.33,
    #           "author": ["gy", "xjq"], "aim": False}
    # field4 = {"doc_id": "44", "text": {"text":"this is four"}, "like": 1, "price": 4.44,
    #           "author": ["gy", "xjq"], "aim": False}
    # data1 = Data(field1)
    # data2 = Data(field2)
    # data3 = Data(field3)
    # data4 = Data(field4)
    # datas = []
    # datas.append(data1)
    # datas.append(data2)
    # datas.append(data3)
    # datas.append(data4)
    # collection.upsert_data(datas)  # 无返回
    #
    # index = vikingdb_service.get_index("example_text", "example_index_text")
    # res = index.search_by_text(Text(text="this is five"), filter={"op": "range", "field": "price", "lt": 4},
    #                            limit=3, output_fields=["doc_id", "text", "price", "like"], partition=1)
    # for item in res:
    #     print(item)
    #     print(item.text)
    # list = [RawData("text","hello1"), RawData("text","hello2")]
    # res = vikingdb_service.embedding(EmbModel("bge_large_zh"), list)
    # print(res)
    # for item in res:
    #     print(item)

    # fields = [
    #     Field(
    #         field_name="like1",
    #         field_type=FieldType.Float32,
    #         default_val=0
    #     ),
    #     Field(
    #         field_name="price1",
    #         field_type=FieldType.String,
    #         default_val=""
    #     ),
    # ]
    # vikingdb_service.update_collection("example",fields,description="change")
    # res = vikingdb_service.get_collection("example")
    # print(res.description)
    # for field in res.fields:
    #     print(field.field_name)
    #     print(field.field_type)
    #     print(field.default_val)
    #     print(field.dim)
    #     print(field.pipeline_name)
    #     print("--------------------")

    # res = vikingdb_service.get_index("example", "example_index")
    # print(res.description)
    # print(res.cpu_quota)
    # print(res.scalar_index)
    #
    # vikingdb_service.update_index("example", "example_index", shard_count=3)
    #
    # res = vikingdb_service.get_index("example", "example_index")
    # print(res.description)
    # print(res.cpu_quota)
    # print(res.scalar_index)

    # score = vikingdb_service.rerank("退改", "如果您需要人工服务，可以拨打人工客服电话：4006660921", "转人工")
    # print(score)

    # async def create_collection():
    #     fields = [
    #         Field(
    #             field_name="doc_id",
    #             field_type=FieldType.String,
    #             is_primary_key=True
    #         ),
    #         Field(
    #             field_name="text_vector",
    #             field_type=FieldType.Vector,
    #             dim=10
    #         ),
    #         Field(
    #             field_name="like",
    #             field_type=FieldType.Int64,
    #             default_val=0
    #         ),
    #         Field(
    #             field_name="price",
    #             field_type=FieldType.Float32,
    #             default_val=0
    #         ),
    #         Field(
    #             field_name="author",
    #             field_type=FieldType.List_String,
    #             default_val=[]
    #         ),
    #         Field(
    #             field_name="aim",
    #             field_type=FieldType.Bool,
    #             default_val=True
    #         ),
    #     ]
    #     res = await vikingdb_service.async_create_collection("async", fields, "This is an example")
    #     print(res)


    # async def get_collection():
    #     res = await vikingdb_service.async_get_collection("async")
    #     for item in res.fields:
    #         print(item.field_type, item.field_name)


    # async def del_collection():
    #     await vikingdb_service.async_drop_collection("async")


    # async def list_collections():
    #     res = await vikingdb_service.async_list_collections()
    #     print(res)


    # async def create_index():
    #     vector_index = VectorIndexParams(distance=DistanceType.COSINE, index_type=IndexType.HNSW,
    #                                      quant=QuantType.Float)
    #     res = await vikingdb_service.async_create_index("async", "async", vector_index, cpu_quota=2,
    #                                                     description="This is an index", scalar_index=['price', 'like'], shard_policy=ShardType.Custom, shard_count=10)
    #     print(res)


    # async def get_index():
    #     res = await vikingdb_service.async_get_index("async", "async")
    #     print(res.shard_count, res.shard_policy)


    # async def del_index():
    #     await vikingdb_service.async_drop_index("async", "async")


    # async def list_index():
    #     res = await vikingdb_service.async_list_indexes("async")
    #     print(res)
    #     for item in res:
    #         print(item.index_name)


    # async def embedding():
    #     list = [RawData("text", "hello1"), RawData("text", "hello2")]
    #     res = await vikingdb_service.async_embedding(EmbModel("bge_large_zh"), list)
    #     print(res)


    # async def update_index():
    #     await vikingdb_service.async_update_index("async", "async", shard_count=3)


    # async def update_collection():
    #     fields = [
    #         Field(
    #             field_name="like1",
    #             field_type=FieldType.Float32,
    #             default_val=0
    #         ),
    #         Field(
    #             field_name="price1",
    #             field_type=FieldType.String,
    #             default_val=""
    #         ),
    #     ]
    #     await vikingdb_service.async_update_collection("async1", fields)


    # async def rerank():
    #     score = await vikingdb_service.async_rerank("退改", "如果您需要人工服务，可以拨打人工客服电话：4006660921",
    #                                                 "转人工")
    #     print(score)


    # async def batch_rerank():
    #     datas = [{
    #         "query": "退改",
    #         "content": "如果您需要人工服务，可以拨打人工客服电话：4006660921",
    #         "title": "无"
    #     }, {
    #         "query": "退改",
    #         "content": "1、1日票 1.5日票 2日票的退款政策： -到访日前2天的00:00前，免费退款 - 到访日前2天的00:00至到访日前夜23:59期间,退款需扣除服务费（人民币80元） - 到访日当天（00:00 之后），不可退款 2、半日票的退款政策： - 未使用的们票可在所选入...",
    #         "title": "门票退改政策｜北京环球影城的门票退改政策"
    #     }, {
    #         "query": "退改",
    #         "content": "如果您需要人工服务，可以拨打人工客服电话：4006660921",
    #     }]
    #     res = await vikingdb_service.async_batch_rerank(datas)
    #     print(res)


    # async def embedding_v2():
    #     list = [RawData("text", "hello1"), RawData("text", "hello2")]
    #     res = await vikingdb_service.async_embedding_v2(EmbModel("bge-m3"), list)
    #     print(res)


    # async def upsert_data():
    #     def gen_random_vector(dim):
    #         res = [0, ] * dim
    #         for i in range(dim):
    #             res[i] = random.random() - 0.5
    #         return res

    #     collection = await vikingdb_service.async_get_collection("example")
    #     field1 = {"doc_id": "111", "text_vector": gen_random_vector(10), "like": 1, "price": 1.11,
    #               "author": ["gy"], "aim": True}
    #     field2 = {"doc_id": "222", "text_vector": gen_random_vector(10), "like": 2, "price": 2.22,
    #               "author": ["gy", "xjq"], "aim": False}
    #     field3 = {"doc_id": "333", "text_vector": gen_random_vector(10), "like": 3, "price": 3.33,
    #               "author": ["gy", "xjq"], "aim": False}
    #     field4 = {"doc_id": "444", "text_vector": gen_random_vector(10), "like": 4, "price": 4.44,
    #               "author": ["gy", "xjq"], "aim": False}
    #     data1 = Data(field1)
    #     data2 = Data(field2)
    #     data3 = Data(field3)
    #     data4 = Data(field4)
    #     datas = [data1, data2, data3, data4]
    #     await collection.async_upsert_data(datas)


    # async def fetch_data():
    #     collection = vikingdb_service.get_collection("async")
    #     res = await collection.async_fetch_data(["111", "222"])
    #     for item in res:
    #         print(item.fields)


    # async def del_data():
    #     collection = vikingdb_service.get_collection("async")
    #     res = await collection.async_delete_data("111")


    # async def search_by_id():
    #     index = await vikingdb_service.async_get_index("async", "async")
    #     res = await index.async_search_by_id("222")
    #     for item in res:
    #         print(item.fields)


    # async def search_by_vector():
    #     def gen_random_vector(dim):
    #         res = [0, ] * dim
    #         for i in range(dim):
    #             res[i] = random.random() - 0.5
    #         return res

    #     index = await vikingdb_service.async_get_index("async", "async")
    #     res = await index.async_search_by_vector(gen_random_vector(10))
    #     for item in res:
    #         print(item.fields)


    # async def index_fetch_data():
    #     index = await vikingdb_service.async_get_index("async", "async")
    #     res = await index.async_fetch_data(["111", "222", "333", "444"])
    #     for item in res:
    #         print(item.fields)


    # async def search():
    #     index = vikingdb_service.get_index("async", "async")

    #     def gen_random_vector(dim):
    #         res = [0, ] * dim
    #         for i in range(dim):
    #             res[i] = random.random() - 0.5
    #         return res

    #     res = index.search(order=VectorOrder(gen_random_vector(10)), limit=2,
    #                        output_fields=["doc_id", "like", "text_vector"],
    #                        filter={"op": "range", "field": "price", "lt": 3.5})
    #     print("-----------search_vector---------")
    #     for item in res:
    #         print(item)
    #         print(item.score)
    #     print("-----------search_scalar---------")
    #     res = index.search(order=ScalarOrder("price", Order.Desc), limit=6,
    #                        output_fields=["price"],
    #                        filter={"op": "range", "field": "price", "lt": 5})
    #     for item in res:
    #         print(item)
    #         print(item.score)
    #     print("-----------search_None---------")
    #     res = index.search(limit=5, output_fields=["doc_id", "like"],
    #                        filter={"op": "range", "field": "price", "lt": 3.5})
    #     for item in res:
    #         print(item.fields)
    #         print(item.score)


    # asyncio.run(create_collection())
    # asyncio.run(get_collection())
    # asyncio.run(del_collection())
    # asyncio.run(list_collections())
    # asyncio.run(create_index())
    # asyncio.run(get_index())
    # asyncio.run(del_index())
    # asyncio.run(list_index())
    # asyncio.run(embedding())
    # asyncio.run(update_index())
    # asyncio.run(update_collection())
    # asyncio.run(rerank())
    # asyncio.run(batch_rerank())
    # asyncio.run(embedding_v2())
    # asyncio.run(upsert_data())
    # asyncio.run(fetch_data())
    # asyncio.run(del_data())
    # asyncio.run(search_by_id())
    # asyncio.run(search_by_vector())
    # asyncio.run(index_fetch_data())
    # asyncio.run(search())

    # with open('', 'rb') as file:
    #     file_content = file.read()
    # encoded_image_content = base64.b64encode(file_content).decode()
    # list = [RawData("image", image=encoded_image_content), RawData("image", image=encoded_image_content)]
    # res = vikingdb_service.embedding_v2(EmbModel(""), list)
    # print(res)
