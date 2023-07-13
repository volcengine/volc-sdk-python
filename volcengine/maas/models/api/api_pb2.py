# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: api/api.proto

import sys
_b=sys.version_info[0]<3 and (lambda x:x) or (lambda x:x.encode('latin1'))
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from google.protobuf import reflection as _reflection
from google.protobuf import symbol_database as _symbol_database
from google.protobuf import descriptor_pb2
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()


from .. import base_pb2 as base__pb2


DESCRIPTOR = _descriptor.FileDescriptor(
  name='api/api.proto',
  package='api',
  syntax='proto3',
  serialized_pb=_b('\n\rapi/api.proto\x12\x03\x61pi\x1a\nbase.proto\"(\n\x07Message\x12\x0c\n\x04role\x18\x01 \x01(\t\x12\x0f\n\x07\x63ontent\x18\x02 \x01(\t\"*\n\x05Model\x12\x0c\n\x04name\x18\x01 \x01(\t\x12\x13\n\x0b\x65ndpoint_id\x18\x02 \x01(\t\"6\n\x05\x45rror\x12\x0c\n\x04\x63ode\x18\x01 \x01(\t\x12\x0e\n\x06\x63ode_n\x18\x02 \x01(\x05\x12\x0f\n\x07message\x18\x03 \x01(\t\"6\n\tErrorResp\x12\x19\n\x05\x65rror\x18\x01 \x01(\x0b\x32\n.api.Error\x12\x0e\n\x06req_id\x18\x02 \x01(\t\"_\n\x06\x43hoice\x12\r\n\x05index\x18\x01 \x01(\x05\x12\x1d\n\x07message\x18\x02 \x01(\x0b\x32\x0c.api.Message\x12\x15\n\rfinish_reason\x18\x03 \x01(\t\x12\x10\n\x08logprobs\x18\x04 \x01(\x02\"\xcf\x01\n\nParameters\x12\x13\n\x0btemperature\x18\x01 \x01(\x02\x12\x12\n\nmax_tokens\x18\x02 \x01(\x03\x12\r\n\x05top_p\x18\x03 \x01(\x02\x12\x18\n\x10presence_penalty\x18\x04 \x01(\x02\x12\x19\n\x11\x66requency_penalty\x18\x05 \x01(\x02\x12\x16\n\x0emax_new_tokens\x18\x06 \x01(\x03\x12\x1a\n\x12repetition_penalty\x18\x07 \x01(\x02\x12\x11\n\tdo_sample\x18\x08 \x01(\x08\x12\r\n\x05top_k\x18\t \x01(\x03\"O\n\x05Usage\x12\x15\n\rprompt_tokens\x18\x01 \x01(\x03\x12\x19\n\x11\x63ompletion_tokens\x18\x02 \x01(\x03\x12\x14\n\x0ctotal_tokens\x18\x03 \x01(\x03\"\x89\x01\n\x07\x43hatReq\x12\x19\n\x05model\x18\x01 \x01(\x0b\x32\n.api.Model\x12\x1e\n\x08messages\x18\x02 \x03(\x0b\x32\x0c.api.Message\x12#\n\nparameters\x18\x03 \x01(\x0b\x32\x0f.api.Parameters\x12\x0e\n\x06stream\x18\x04 \x01(\x08\x12\x0e\n\x06req_id\x18\x05 \x01(\t\"m\n\x08\x43hatResp\x12\x0e\n\x06req_id\x18\x01 \x01(\t\x12\x19\n\x05\x65rror\x18\x02 \x01(\x0b\x32\n.api.Error\x12\x1b\n\x06\x63hoice\x18\x03 \x01(\x0b\x32\x0b.api.Choice\x12\x19\n\x05usage\x18\x04 \x01(\x0b\x32\n.api.Usage2B\n\nAPIService\x12\x34\n\x04\x43hat\x12\x0c.api.ChatReq\x1a\r.api.ChatResp\"\x0f\xd2\xc1\x18\x0b\x61pi/v1/chatb\x06proto3')
  ,
  dependencies=[base__pb2.DESCRIPTOR,])
_sym_db.RegisterFileDescriptor(DESCRIPTOR)




_MESSAGE = _descriptor.Descriptor(
  name='Message',
  full_name='api.Message',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='role', full_name='api.Message.role', index=0,
      number=1, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='content', full_name='api.Message.content', index=1,
      number=2, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=34,
  serialized_end=74,
)


_MODEL = _descriptor.Descriptor(
  name='Model',
  full_name='api.Model',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='name', full_name='api.Model.name', index=0,
      number=1, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='endpoint_id', full_name='api.Model.endpoint_id', index=1,
      number=2, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=76,
  serialized_end=118,
)


_ERROR = _descriptor.Descriptor(
  name='Error',
  full_name='api.Error',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='code', full_name='api.Error.code', index=0,
      number=1, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='code_n', full_name='api.Error.code_n', index=1,
      number=2, type=5, cpp_type=1, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='message', full_name='api.Error.message', index=2,
      number=3, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=120,
  serialized_end=174,
)


_ERRORRESP = _descriptor.Descriptor(
  name='ErrorResp',
  full_name='api.ErrorResp',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='error', full_name='api.ErrorResp.error', index=0,
      number=1, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='req_id', full_name='api.ErrorResp.req_id', index=1,
      number=2, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=176,
  serialized_end=230,
)


_CHOICE = _descriptor.Descriptor(
  name='Choice',
  full_name='api.Choice',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='index', full_name='api.Choice.index', index=0,
      number=1, type=5, cpp_type=1, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='message', full_name='api.Choice.message', index=1,
      number=2, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='finish_reason', full_name='api.Choice.finish_reason', index=2,
      number=3, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='logprobs', full_name='api.Choice.logprobs', index=3,
      number=4, type=2, cpp_type=6, label=1,
      has_default_value=False, default_value=float(0),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=232,
  serialized_end=327,
)


_PARAMETERS = _descriptor.Descriptor(
  name='Parameters',
  full_name='api.Parameters',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='temperature', full_name='api.Parameters.temperature', index=0,
      number=1, type=2, cpp_type=6, label=1,
      has_default_value=False, default_value=float(0),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='max_tokens', full_name='api.Parameters.max_tokens', index=1,
      number=2, type=3, cpp_type=2, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='top_p', full_name='api.Parameters.top_p', index=2,
      number=3, type=2, cpp_type=6, label=1,
      has_default_value=False, default_value=float(0),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='presence_penalty', full_name='api.Parameters.presence_penalty', index=3,
      number=4, type=2, cpp_type=6, label=1,
      has_default_value=False, default_value=float(0),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='frequency_penalty', full_name='api.Parameters.frequency_penalty', index=4,
      number=5, type=2, cpp_type=6, label=1,
      has_default_value=False, default_value=float(0),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='max_new_tokens', full_name='api.Parameters.max_new_tokens', index=5,
      number=6, type=3, cpp_type=2, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='repetition_penalty', full_name='api.Parameters.repetition_penalty', index=6,
      number=7, type=2, cpp_type=6, label=1,
      has_default_value=False, default_value=float(0),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='do_sample', full_name='api.Parameters.do_sample', index=7,
      number=8, type=8, cpp_type=7, label=1,
      has_default_value=False, default_value=False,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='top_k', full_name='api.Parameters.top_k', index=8,
      number=9, type=3, cpp_type=2, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=330,
  serialized_end=537,
)


_USAGE = _descriptor.Descriptor(
  name='Usage',
  full_name='api.Usage',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='prompt_tokens', full_name='api.Usage.prompt_tokens', index=0,
      number=1, type=3, cpp_type=2, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='completion_tokens', full_name='api.Usage.completion_tokens', index=1,
      number=2, type=3, cpp_type=2, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='total_tokens', full_name='api.Usage.total_tokens', index=2,
      number=3, type=3, cpp_type=2, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=539,
  serialized_end=618,
)


_CHATREQ = _descriptor.Descriptor(
  name='ChatReq',
  full_name='api.ChatReq',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='model', full_name='api.ChatReq.model', index=0,
      number=1, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='messages', full_name='api.ChatReq.messages', index=1,
      number=2, type=11, cpp_type=10, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='parameters', full_name='api.ChatReq.parameters', index=2,
      number=3, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='stream', full_name='api.ChatReq.stream', index=3,
      number=4, type=8, cpp_type=7, label=1,
      has_default_value=False, default_value=False,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='req_id', full_name='api.ChatReq.req_id', index=4,
      number=5, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=621,
  serialized_end=758,
)


_CHATRESP = _descriptor.Descriptor(
  name='ChatResp',
  full_name='api.ChatResp',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='req_id', full_name='api.ChatResp.req_id', index=0,
      number=1, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='error', full_name='api.ChatResp.error', index=1,
      number=2, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='choice', full_name='api.ChatResp.choice', index=2,
      number=3, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='usage', full_name='api.ChatResp.usage', index=3,
      number=4, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=760,
  serialized_end=869,
)

_ERRORRESP.fields_by_name['error'].message_type = _ERROR
_CHOICE.fields_by_name['message'].message_type = _MESSAGE
_CHATREQ.fields_by_name['model'].message_type = _MODEL
_CHATREQ.fields_by_name['messages'].message_type = _MESSAGE
_CHATREQ.fields_by_name['parameters'].message_type = _PARAMETERS
_CHATRESP.fields_by_name['error'].message_type = _ERROR
_CHATRESP.fields_by_name['choice'].message_type = _CHOICE
_CHATRESP.fields_by_name['usage'].message_type = _USAGE
DESCRIPTOR.message_types_by_name['Message'] = _MESSAGE
DESCRIPTOR.message_types_by_name['Model'] = _MODEL
DESCRIPTOR.message_types_by_name['Error'] = _ERROR
DESCRIPTOR.message_types_by_name['ErrorResp'] = _ERRORRESP
DESCRIPTOR.message_types_by_name['Choice'] = _CHOICE
DESCRIPTOR.message_types_by_name['Parameters'] = _PARAMETERS
DESCRIPTOR.message_types_by_name['Usage'] = _USAGE
DESCRIPTOR.message_types_by_name['ChatReq'] = _CHATREQ
DESCRIPTOR.message_types_by_name['ChatResp'] = _CHATRESP

Message = _reflection.GeneratedProtocolMessageType('Message', (_message.Message,), dict(
  DESCRIPTOR = _MESSAGE,
  __module__ = 'api.api_pb2'
  # @@protoc_insertion_point(class_scope:api.Message)
  ))
_sym_db.RegisterMessage(Message)

Model = _reflection.GeneratedProtocolMessageType('Model', (_message.Message,), dict(
  DESCRIPTOR = _MODEL,
  __module__ = 'api.api_pb2'
  # @@protoc_insertion_point(class_scope:api.Model)
  ))
_sym_db.RegisterMessage(Model)

Error = _reflection.GeneratedProtocolMessageType('Error', (_message.Message,), dict(
  DESCRIPTOR = _ERROR,
  __module__ = 'api.api_pb2'
  # @@protoc_insertion_point(class_scope:api.Error)
  ))
_sym_db.RegisterMessage(Error)

ErrorResp = _reflection.GeneratedProtocolMessageType('ErrorResp', (_message.Message,), dict(
  DESCRIPTOR = _ERRORRESP,
  __module__ = 'api.api_pb2'
  # @@protoc_insertion_point(class_scope:api.ErrorResp)
  ))
_sym_db.RegisterMessage(ErrorResp)

Choice = _reflection.GeneratedProtocolMessageType('Choice', (_message.Message,), dict(
  DESCRIPTOR = _CHOICE,
  __module__ = 'api.api_pb2'
  # @@protoc_insertion_point(class_scope:api.Choice)
  ))
_sym_db.RegisterMessage(Choice)

Parameters = _reflection.GeneratedProtocolMessageType('Parameters', (_message.Message,), dict(
  DESCRIPTOR = _PARAMETERS,
  __module__ = 'api.api_pb2'
  # @@protoc_insertion_point(class_scope:api.Parameters)
  ))
_sym_db.RegisterMessage(Parameters)

Usage = _reflection.GeneratedProtocolMessageType('Usage', (_message.Message,), dict(
  DESCRIPTOR = _USAGE,
  __module__ = 'api.api_pb2'
  # @@protoc_insertion_point(class_scope:api.Usage)
  ))
_sym_db.RegisterMessage(Usage)

ChatReq = _reflection.GeneratedProtocolMessageType('ChatReq', (_message.Message,), dict(
  DESCRIPTOR = _CHATREQ,
  __module__ = 'api.api_pb2'
  # @@protoc_insertion_point(class_scope:api.ChatReq)
  ))
_sym_db.RegisterMessage(ChatReq)

ChatResp = _reflection.GeneratedProtocolMessageType('ChatResp', (_message.Message,), dict(
  DESCRIPTOR = _CHATRESP,
  __module__ = 'api.api_pb2'
  # @@protoc_insertion_point(class_scope:api.ChatResp)
  ))
_sym_db.RegisterMessage(ChatResp)


# @@protoc_insertion_point(module_scope)