
from .Doc import Doc    

class Point(object):  
    def __init__(self, kwargs):
        self.collection_name        = kwargs.get("collection_name")
        self.point_id               = kwargs.get("point_id")
        self.chunk_title            = kwargs.get("chunk_title") 
        self.original_question      = kwargs.get("original_question") 
        self.process_time           = kwargs.get("process_time") 
        self.content                = kwargs.get("content") 
        self.rerank_score           = kwargs.get("rerank_score")
        self.score                  = kwargs.get("score")
        self.doc_info               = Doc(kwargs.get("doc_info"))
        self.chunk_id               = kwargs.get("chunk_id")
        