from google.protobuf import message as _message
from google.protobuf.internal import decoder as _decoder
from google.protobuf.internal import wire_format as _wire_format
from volcengine.tls import log_pb2


def ParseLogGroupListFromString(log_group_list, serialized_data):
    buffer = memoryview(serialized_data)
    pos = 0
    end = len(buffer)
    log_group_list.Clear()
    while pos < end:
        tag_bytes, pos = _decoder.ReadTag(buffer, pos)
        tag = _decoder._DecodeVarint(tag_bytes, 0)[0]
        field_num, wire_type = _wire_format.UnpackTag(tag)

        if field_num == 1 and wire_type == _wire_format.WIRETYPE_LENGTH_DELIMITED:
            pos = _parse_log_groups(log_group_list, buffer, pos, end)
        else:
            pos = _decoder.SkipField(buffer, pos, end, tag_bytes)  # pylint: disable=no-member
    return pos


def _parse_log_groups(log_group_list, buffer, pos, end):
    size, pos = _decoder._DecodeVarint(buffer, pos)
    group_end = pos + size
    if group_end > end:
        raise _message.DecodeError("Truncated LogGroupList.log_groups")

    group = log_pb2.LogGroup()
    ParseLogGroupFromString(group, buffer[pos:group_end].tobytes())
    log_group_list.log_groups.append(group)
    return group_end


def ParseLogGroupFromString(log_group, serialized_data):
    buffer = memoryview(serialized_data)
    pos = 0
    end = len(buffer)
    log_group.Clear()
    while pos < end:
        tag_bytes, pos = _decoder.ReadTag(buffer, pos)
        tag = _decoder._DecodeVarint(tag_bytes, 0)[0]
        field_num, wire_type = _wire_format.UnpackTag(tag)

        if field_num == 1 and wire_type == _wire_format.WIRETYPE_LENGTH_DELIMITED:
            pos = _parse_logs(log_group, buffer, pos, end)
        elif field_num == 2 and wire_type == _wire_format.WIRETYPE_LENGTH_DELIMITED:
            pos = _parse_source(log_group, buffer, pos, end)
        elif field_num == 3 and wire_type == _wire_format.WIRETYPE_LENGTH_DELIMITED:
            pos = _parse_log_tags(log_group, buffer, pos, end)  # 补充：解析log_tags
        elif field_num == 4 and wire_type == _wire_format.WIRETYPE_LENGTH_DELIMITED:
            pos = _parse_filename(log_group, buffer, pos, end)  # 补充：解析filename
        elif field_num == 5 and wire_type == _wire_format.WIRETYPE_LENGTH_DELIMITED:
            pos = _parse_context_flow(log_group, buffer, pos, end)  # 补充：解析context_flow
        else:
            pos = _decoder.SkipField(buffer, pos, end, tag_bytes)  # pylint: disable=no-member
    return pos

def _parse_logs(log_group, buffer, pos, end):
    """原代码逻辑不变"""
    size, pos = _decoder._DecodeVarint(buffer, pos)
    log_end = pos + size
    if log_end > end:
        raise _message.DecodeError("Truncated LogGroup.logs")

    log = log_pb2.Log()
    ParseLogFromString(log, buffer[pos:log_end].tobytes())
    log_group.logs.append(log)
    return log_end

def _parse_source(log_group, buffer, pos, end):
    """原代码逻辑不变"""
    size, pos = _decoder._DecodeVarint(buffer, pos)
    new_pos = pos + size
    if new_pos > end:
        raise _message.DecodeError("Truncated LogGroup.source")
    log_group.source = buffer[pos:new_pos].tobytes().decode('utf-8')
    return new_pos

def _parse_log_tags(log_group, buffer, pos, end):
    """补充：解析log_tags字段（参考_parse_logs逻辑）"""
    size, pos = _decoder._DecodeVarint(buffer, pos)
    tag_end = pos + size
    if tag_end > end:
        raise _message.DecodeError("Truncated LogGroup.log_tags")

    tag = log_pb2.LogTag()
    ParseLogTagFromString(tag, buffer[pos:tag_end].tobytes())
    log_group.log_tags.append(tag)
    return tag_end

def _parse_filename(log_group, buffer, pos, end):
    """补充：解析filename字段（参考_parse_source逻辑）"""
    size, pos = _decoder._DecodeVarint(buffer, pos)
    new_pos = pos + size
    if new_pos > end:
        raise _message.DecodeError("Truncated LogGroup.filename")
    log_group.filename = buffer[pos:new_pos].tobytes().decode('utf-8')
    return new_pos

def _parse_context_flow(log_group, buffer, pos, end):
    """补充：解析context_flow字段（参考_parse_source逻辑）"""
    size, pos = _decoder._DecodeVarint(buffer, pos)
    new_pos = pos + size
    if new_pos > end:
        raise _message.DecodeError("Truncated LogGroup.context_flow")
    log_group.context_flow = buffer[pos:new_pos].tobytes().decode('utf-8')
    return new_pos

def ParseLogTagFromString(log_tag, serialized_data):
    """反序列化：解析字段1（key）和字段2（value）"""
    buffer = memoryview(serialized_data)
    pos = 0
    end = len(buffer)
    log_tag.Clear()
    while pos < end:
        tag_bytes, pos = _decoder.ReadTag(buffer, pos)
        tag = _decoder._DecodeVarint(tag_bytes, 0)[0]
        field_num, wire_type = _wire_format.UnpackTag(tag)

        if field_num == 1 and wire_type == _wire_format.WIRETYPE_LENGTH_DELIMITED:
            pos = _parse_key(log_tag, buffer, pos, end)
        elif field_num == 2 and wire_type == _wire_format.WIRETYPE_LENGTH_DELIMITED:
            pos = _parse_value(log_tag, buffer, pos, end)
        else:
            pos = _decoder.SkipField(buffer, pos, end, tag_bytes)  # pylint: disable=no-member
    return pos

def _parse_key(item, buffer, pos, end):
    size, pos = _decoder._DecodeVarint(buffer, pos)
    new_pos = pos + size
    if new_pos > end:
        raise _message.DecodeError("Truncated LogTag.key")
    item.key = buffer[pos:new_pos].tobytes().decode('utf-8', errors='replace')
    return new_pos

def _parse_value(item, buffer, pos, end):
    size, pos = _decoder._DecodeVarint(buffer, pos)
    new_pos = pos + size
    if new_pos > end:
        raise _message.DecodeError("Truncated LogTag.value")
    raw_bytes = buffer[pos:new_pos].tobytes()
    item.value = raw_bytes.decode('utf-8', errors='replace')
    return new_pos

def ParseLogFromString(log, serialized_data):
    buffer = memoryview(serialized_data)
    pos = 0
    end = len(buffer)
    log.Clear()
    while pos < end:
        tag_bytes, pos = _decoder.ReadTag(buffer, pos)
        tag = _decoder._DecodeVarint(tag_bytes, 0)[0]
        field_num, wire_type = _wire_format.UnpackTag(tag)

        if field_num == 1 and wire_type == _wire_format.WIRETYPE_VARINT:
            pos = _parse_time(log, buffer, pos, end)
        elif field_num == 2 and wire_type == _wire_format.WIRETYPE_LENGTH_DELIMITED:
            pos = _parse_contents(log, buffer, pos, end)
        else:
            pos = _decoder.SkipField(buffer, pos, end, tag_bytes)  # pylint: disable=no-member
    return pos

def _parse_time(log, buffer, pos, end):
    value, pos = _decoder._DecodeSignedVarint32(buffer, pos)
    log.time = value
    return pos

def _parse_contents(log, buffer, pos, end):
    size, pos = _decoder._DecodeVarint(buffer, pos)
    content_end = pos + size
    if content_end > end:
        raise _message.DecodeError("Truncated Log.contents")

    content = log_pb2.LogContent()
    ParseLogContentFromString(content, buffer[pos:content_end].tobytes())
    log.contents.append(content)
    return content_end

def ParseLogContentFromString(content, serialized_data):
    buffer = memoryview(serialized_data)
    pos = 0
    end = len(buffer)
    content.Clear()
    while pos < end:
        tag_bytes, pos = _decoder.ReadTag(buffer, pos)
        tag = _decoder._DecodeVarint(tag_bytes, 0)[0]
        field_num, wire_type = _wire_format.UnpackTag(tag)

        if field_num == 1 and wire_type == _wire_format.WIRETYPE_LENGTH_DELIMITED:
            pos = _parse_key(content, buffer, pos, end)
        elif field_num == 2 and wire_type == _wire_format.WIRETYPE_LENGTH_DELIMITED:
            pos = _parse_value(content, buffer, pos, end)
        else:
            pos = _decoder.SkipField(buffer, pos, end, tag_bytes)  # pylint: disable=no-member
    return pos
