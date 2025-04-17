# coding:utf-8
import json
import random
from enum import Enum
from typing import List

INITIAL_RETRY_DELAY = 0.5
MAX_RETRY_DELAY = 8.0
MAX_RETRIES = 3

class RetryRemaining(object):
    def __init__(self, remaining_retries, remaining_delay):
        self.remaining_retries = remaining_retries
        self.remaining_delay = remaining_delay

    def has_remaining(self):
        return self.remaining_retries > 0 and self.remaining_delay > 0

class RetryOption(object):
    def __init__(self):
        self.initial_retry_delay = INITIAL_RETRY_DELAY
        self.max_retry_delay = MAX_RETRY_DELAY
        self.max_retries = MAX_RETRIES
        self.retry_when_quota_limit = True
        self.retry_when_session_timeout = True

    def new_remaining(self, retry=True):
        remaining_retries = self.max_retries if retry else 0
        remaining_delay = self.max_retry_delay if retry else 0
        return RetryRemaining(remaining_retries, remaining_delay)

    def calculate_retry_timeout(self, remaining):
        remaining.remaining_retries  = remaining.remaining_retries - 1
        nb_retries = self.max_retries - remaining.remaining_retries
        sleep_seconds = min(self.initial_retry_delay * pow(2.0, nb_retries), self.max_retry_delay)
        jitter = 1 - 0.25 * random.random()
        timeout = sleep_seconds * jitter
        remaining.remaining_delay  = remaining.remaining_delay - timeout
        return timeout if timeout >= 0 else 0

class ShardType(Enum):
    """
    type of shard policy
    """
    Auto = "auto"
    Custom = "custom"


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
    Image = "image"
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
    SORT = "sort"

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

class TaskType(Enum):
    Data_Import = "data_import"
    Filter_Delete = "filter_delete"
    Data_export = "data_export"
    Filter_Update = "filter_update"

class TaskStatus(Enum):
    Init = "init"
    Queued = "queued"
    Running = "running"
    Done = "done"
    Fail = "fail"
    Confirm = "confirm"
    Confirmed = "confirmed"

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

class VectorizeTuple(object):
    def __init__(self, dense, sparse=None):
        assert isinstance(dense, VectorizeModelConf)
        if sparse is not None:
            assert isinstance(sparse, VectorizeModelConf)
        self._dense = dense
        self._sparse = sparse

    @property
    def dense(self):
        return self._dense

    @property
    def sparse(self):
        return self._sparse

class VectorizeModelConf(object):
    def __init__(self, model_name, model_version=None, dim=None, text_field=None, image_field=None):
        self._model_name = model_name
        self._model_version = model_version
        self._dim = dim
        self._text_field = text_field
        self._image_field = image_field

    @property
    def model_name(self):
        return self._model_name

    @property
    def model_version(self):
        return self._model_version

    @property
    def dim(self):
        return self._dim

    @property
    def text_field(self):
        return self._text_field

    @property
    def image_field(self):
        return self._image_field

def convert_vectorize_tuple_to_dict(vectorize_tuple):
    assert isinstance(vectorize_tuple, VectorizeTuple)
    result = {}
    if vectorize_tuple.dense is not None:
        result['dense'] = convert_vectorize_conf_to_dict(vectorize_tuple.dense)
    if vectorize_tuple.sparse is not None:
        result['sparse'] = convert_vectorize_conf_to_dict(vectorize_tuple.sparse)
    return result

def convert_vectorize_conf_to_dict(vectorize_conf):
    assert isinstance(vectorize_conf, VectorizeModelConf)
    result = {}
    if vectorize_conf.text_field is not None:
        result['text_field'] = vectorize_conf.text_field
    if vectorize_conf.image_field is not None:
        result['image_field'] = vectorize_conf.image_field
    if vectorize_conf.model_name is not None:
        result['model_name'] = vectorize_conf.model_name
    if vectorize_conf.model_version is not None:
        result['model_version'] = vectorize_conf.model_version
    if vectorize_conf.dim is not None:
        result['dim'] = vectorize_conf.dim
    return result

def convert_dict_to_vectorize_tuple(vectorize_tuple_dict):
    assert isinstance(vectorize_tuple_dict, dict)
    dense_dict = vectorize_tuple_dict.get('dense', None)
    sparse_dict = vectorize_tuple_dict.get('sparse', None)
    return VectorizeTuple(
        dense=convert_dict_to_vectorize_conf(dense_dict),
        sparse=convert_dict_to_vectorize_conf(sparse_dict),
    )

def convert_dict_to_vectorize_conf(vectorize_conf_dict):
    if vectorize_conf_dict is None:
        return None
    assert isinstance(vectorize_conf_dict, dict)
    return VectorizeModelConf(
        vectorize_conf_dict['model_name'],
        model_version=vectorize_conf_dict.get('model_version', None),
        dim=vectorize_conf_dict.get('dim', None),
        text_field=vectorize_conf_dict.get('text_field', None),
        image_field=vectorize_conf_dict.get('image_field', None),
    )

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

class AggResult(object):
    def __init__(self, agg_op, group_by_field, agg_result):
        self._agg_op = agg_op
        self._group_by_field = group_by_field
        self._agg_result = agg_result

    @property
    def agg_op(self):
        return self._agg_op

    @property
    def group_by_field(self):
        return self._group_by_field

    @property
    def agg_result(self):
        return self._agg_result

class SortResultItem(object):
    def __init__(self, primary_key, score):
        self._primary_key = primary_key
        self._score = score

    @property
    def primary_key(self):
        return self._primary_key

    @property
    def score(self):
        return self._score

class IndexSortResult(object):
    def __init__(self, sort_result: List[SortResultItem], primary_key_not_exist: List):
        self._sort_result: List[SortResultItem] = sort_result
        self._primary_key_not_exist = primary_key_not_exist

    @property
    def sort_result(self):
        return self._sort_result

    @property
    def primary_key_not_exist(self):
        return self._primary_key_not_exist

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
