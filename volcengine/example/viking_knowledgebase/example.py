import sys
import os
import asyncio
current_directory = os.path.dirname(os.path.abspath(__file__))
seek = os.path.dirname(os.path.dirname(os.path.dirname(current_directory)))  
sys.path.insert(0, seek)

from volcengine.viking_knowledgebase import VikingKnowledgeBaseService, Collection, Doc, Point
from volcengine.viking_knowledgebase.common import Field, FieldType, IndexType, EmbddingModelType

collection_name = ""


viking_knowledgebase_service = VikingKnowledgeBaseService()
points = viking_knowledgebase_service.search_collection(collection_name=collection_name,query="", rerank_switch=True, retrieve_count=20)
for point in points:
    print(point.content)
    print(point.chunk_id)
    print(point.point_id)
    print(point.doc_id)
    print(point.project)
    print("=======")
    
#假定用户已经在知识库中创建了一个collection，并上传了文档，A公司_2022年财报.pdf，A公司_2023年财报.pdf
m_messages = [{
    "role": "system",
    "content": """ system pe """
    },
    {
        "role": "user",
        "content": "22年A公司财报中提到的风险,在23年应对的如何" # 用户提问
    }
]
# chat_completion without streaming
print("#"*10,"chat_completion without streaming","#"*10)
res = viking_knowledgebase_service.chat_completion(model="Doubao-pro-32k", messages=m_messages, max_tokens=4096,
                                                    temperature=0.1)
data = res["generated_answer"]
token_usage = res["usage"]
print(data)
print(token_usage)
# chat_completion with streaming
print("#"*10,"chat_completion with streaming","#"*10)
res = viking_knowledgebase_service.chat_completion(model="Doubao-pro-32k", messages=m_messages, max_tokens=4096,
                                                    temperature=0.1,stream=True)
for data in res:
    print(data,end="",flush=True)
print("")
print(res.token_usage())
    