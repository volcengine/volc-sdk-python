# coding:utf-8
import json
from enum import Enum

class FieldType(Enum):
    Int64 = "int64"
    List_Int64 = "list<int64>"
    String = "string"
    List_String = "list<string>"
    Float32 = "float32"
    Bool = "bool"

class EmbddingModelType(Enum):
    EmbeddingModelBgeLargeZhAndM3   = "bge-large-zh-and-m3"
    EmbeddingModelBgeLargeZh        = "bge-large-zh"
    EmbeddingModelBgeM3             = "bge-m3"
    EmbeddingModelDoubao            = "doubao-embedding"
    EmbeddingModelDoubaoAndM3       = "doubao-embedding-and-m3"
    EmbeddingModelDoubaoLarge       = "doubao-embedding-large"
    EmbeddingModelDoubaoLargeAndM3  = "doubao-embedding-large-and-m3"

class IndexType(Enum):
    FLAT = "flat"
    HNSW = "hnsw"
    HNSW_HYBRID = "hnsw_hybrid"

class QuantType(Enum):
    Float = "float"
    Int8 = "int8"
    Fix16 = "fix16"

class Field(object):
    
    def __init__(self, kwargs):
        self._field_name        = kwargs.get("field_name")
        self._field_type        = kwargs.get("field_type")
        self._field_val         = kwargs.get("default_val") if kwargs.get("default_val") \
                                            is not None else kwargs.get("field_value") 
        self._dim               = kwargs.get("dim", 1)
        self._is_primary_key    = kwargs.get("is_primary_key", False)
        self._pipeline_name     = kwargs.get("pipeline_name")

    @property
    def field_name(self):
        return self._field_name

    @property
    def field_type(self):
        return self._field_type

    @property
    def field_val(self):
        return self._field_val

    @property
    def dim(self):
        return self._dim

    @property
    def is_primary_key(self):
        return self._is_primary_key

    @property
    def pipeline_name(self):
        return self._pipeline_name


class EnumEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, Enum):
            return obj.value
        if isinstance(obj, dict):
            return {k: self.default(v) for k, v in obj.items()}
        return super().default(obj)
