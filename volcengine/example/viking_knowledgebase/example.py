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
    