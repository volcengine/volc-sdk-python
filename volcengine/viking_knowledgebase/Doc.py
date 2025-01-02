from .common import Field
import json

class Doc(object):
    """
    KnowledgeBase Doc data wrapper
    """
    def __init__(self, kwargs):
        self.collection_name    = kwargs.get("collection_name")
        self.doc_name           = kwargs.get("doc_name")
        self.doc_id             = kwargs.get("doc_id")
        self.doc_type           = kwargs.get("doc_type")
        self.create_time        = kwargs.get("create_time")
        self.added_by           = kwargs.get("added_by")
        self.update_time        = kwargs.get("update_time")
        self.url                = kwargs.get("url")
        self.tos_path           = kwargs.get("tos_path")
        self.point_num          = kwargs.get("point_num")
        self.status             = kwargs.get("status")
        self.title              = kwargs.get("title")
        self.source             = kwargs.get("source")
        self.fields             = []
        meta                    = kwargs.get("doc_meta") or kwargs.get("meta")
        if meta is not None:
            meta                = json.loads(meta)
            self.fields         = [Field(field) for field in meta]
        
        self.project            = kwargs.get("project", "default")
        self.resource_id        = kwargs.get("resource_id")