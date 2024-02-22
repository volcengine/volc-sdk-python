import json


class ChatRole:
    USER = "user"
    ASSISTANT = "assistant"
    SYSTEM = "system"
    FUNCTION = "function"


class _Dict(dict):
    __setattr__ = dict.__setitem__
    __getattr__ = dict.__getitem__

    def __missing__(self, key):
        return None


def dict_to_object(dict_obj):
    # 支持嵌套类型
    if isinstance(dict_obj, list):
        insts = []
        for i in dict_obj:
            insts.append(dict_to_object(i))
        return insts

    if isinstance(dict_obj, dict):
        inst = _Dict()
        for k, v in dict_obj.items():
            inst[k] = dict_to_object(v)
        return inst

    return dict_obj


def json_to_object(json_str, req_id=None):
    obj = dict_to_object(json.loads(json_str))
    if obj and isinstance(obj, dict) and req_id:
        obj["req_id"] = req_id
    return obj
