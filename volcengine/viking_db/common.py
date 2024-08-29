# coding:utf-8
import json
from enum import Enum


class FieldType(Enum):
    """
    type of collection filed
    """
    Vector = "vector"
    Int64 = "int64"
    List_Int64 = "list<int64>"
    String = "string"
    List_String = "list<string>"
    Float32 = "float32"
    Bool = "bool"
    Text = "text"
    Sparse_Vector = "sparse_vector"


class DistanceType(Enum):
    """
    distance type of vector ann index
    """
    L2 = "l2"
    IP = "ip"
    COSINE = "cosine"


class IndexType(Enum):
    """
    type of vector ann index
    """
    FLAT = "flat"
    HNSW = "hnsw"
    IVF = "ivf"
    DiskANN = "DiskANN"
    HNSW_HYBRID = "hnsw_hybrid"

class QuantType(Enum):
    """
    quant type of vector ann index
    """
    Float = "float"
    Int8 = "int8"
    Fix16 = "fix16"
    PQ = "pq"


class Order(Enum):
    """
    quant type of vector ann index
    """
    Asc = "asc"
    Desc = "desc"


class EmbModel(object):
    def __init__(self, model_name, params=None):
        self._model_name = model_name
        self._params = params

    @property
    def model_name(self):
        return self._model_name

    @property
    def params(self):
        return self._params


class RawData(object):
    def __init__(self, data_type, text="", image=""):
        self._data_type = data_type
        self._text = text
        self._image = image

    @property
    def data_type(self):
        return self._data_type

    @property
    def text(self):
        return self._text

    @property
    def image(self):
        return self._image


class Field(object):
    """
    Args:
        
    """

    def __init__(self, field_name, field_type, default_val=None, dim=None, is_primary_key=False, pipeline_name=None):
        self._field_name = field_name
        self._field_type = field_type
        self._default_val = default_val
        self._dim = dim
        self._is_primary_key = is_primary_key
        self._pipeline_name = pipeline_name

    @property
    def field_name(self):
        return self._field_name

    @property
    def field_type(self):
        return self._field_type

    @property
    def default_val(self):
        return self._default_val

    @property
    def dim(self):
        return self._dim

    @property
    def is_primary_key(self):
        return self._is_primary_key

    @property
    def pipeline_name(self):
        return self._pipeline_name


class Text(object):
    def __init__(self, text=None, url=None, base64=None):
        self._text = text
        self._url = url
        self._base64 = base64

    @property
    def text(self):
        return self._text

    @property
    def url(self):
        return self._url

    @property
    def base64(self):
        return self._base64


class Data(object):
    def __init__(self, fields, id=None, TTL=None, timestamp=None, score=None, text=None, dist=None):
        self._id = id
        self._fields = fields
        self._timestamp = timestamp
        self._TTL = TTL
        self._score = score
        self._text = text
        self._dist = dist

    @property
    def text(self):
        return self._text

    @property
    def TTL(self):
        return self._TTL

    @property
    def score(self):
        return self._score

    @property
    def id(self):
        return self._id

    @property
    def fields(self):
        return self._fields

    @property
    def timestamp(self):
        return self._timestamp
    
    @property
    def dist(self):
        return self._dist


class VectorIndexParams(object):
    def __init__(self, distance=DistanceType.IP, index_type=IndexType.HNSW, quant=QuantType.Int8, **kwargs):
        self._index_type = index_type
        self._distance = distance
        self._quant = quant
        self._hnsw_m = kwargs.get("hnsw_m", 20)
        self._hnsw_cef = kwargs.get("hnsw_cef", 400)
        self._hnsw_sef = kwargs.get("hnsw_sef", 800)

    def dic(self):
        return {"distance": self.distance.value, "index_type": self.index_type.value, "quant": self.quant.value,
                "hnsw_m": self.hnsw_m, "hnsw_cef": self.hnsw_cef, "hnsw_sef": self.hnsw_sef}

    @property
    def index_type(self):
        return self._index_type

    @property
    def distance(self):
        return self._distance

    @property
    def quant(self):
        return self._quant

    @property
    def hnsw_m(self):
        return self._hnsw_m

    @property
    def hnsw_cef(self):
        return self._hnsw_cef

    @property
    def hnsw_sef(self):
        return self._hnsw_sef


class VectorOrder(object):
    def __init__(self, vector=None, sparse_vectors=None ,id=None):
        self._vector = vector
        self._id = id
        self._sparse_vectors = sparse_vectors

    @property
    def vector(self):
        return self._vector

    @property
    def sparse_vectors(self):
        return self._sparse_vectors

    @property
    def id(self):
        return self._id


class ScalarOrder(object):
    def __init__(self, field_name, order):
        self._field_name = field_name
        self._order = order

    @property
    def field_name(self):
        return self._field_name

    @property
    def order(self):
        return self._order


class MyClassEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, VectorIndexParams):
            return {"distance": obj.distance, "index_type": obj.index_type, "quant": obj.quant,
                    "hnsw_m": obj.hnsw_m, "hnsw_cef": obj.hnsw_cef, "hnsw_sef": obj.hnsw_sef}
        # if isinstance(obj, IndexType):
        #     return {'FLAT': obj.FLAT, 'HNSW': obj.HNSW}
        # if isinstance(obj, QuantType):
        #     return {'Float': obj.Float, 'Int8': obj.Int8}
        return super().default(obj)
