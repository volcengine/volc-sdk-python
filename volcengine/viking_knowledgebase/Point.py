from deprecated import deprecated

from .Doc import Doc    

class Point(object):
    """
    Knowledge Point data wrapper
    """
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
        
        self.project                = kwargs.get("project", "default")
        self.resource_id            = kwargs.get("resource_id")
        self.table_chunk_fields     = kwargs.get("table_chunk_fields")

    @property
    @deprecated(reason="The 'doc_id' property is deprecated. Use 'doc_info.doc_id' instead.")
    def doc_id(self):
        return self.doc_info.doc_id