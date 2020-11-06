# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: base/base.proto

from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from google.protobuf import reflection as _reflection
from google.protobuf import symbol_database as _symbol_database
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()


from google.protobuf import descriptor_pb2 as google_dot_protobuf_dot_descriptor__pb2


DESCRIPTOR = _descriptor.FileDescriptor(
  name='base/base.proto',
  package='Vcloud.Models.Base',
  syntax='proto3',
  serialized_options=b'\n\035com.bytedanceapi.model.commonB\004BaseP\001Z1github.com/TTvcloud/vcloud-sdk-golang/models/base\240\001\001\330\001\001\302\002\000\312\002\022Vcloud\\Models\\Base\342\002\031Vcloud\\Models\\GPBMetadata',
  create_key=_descriptor._internal_create_key,
  serialized_pb=b'\n\x0f\x62\x61se/base.proto\x12\x12Vcloud.Models.Base\x1a google/protobuf/descriptor.proto\"\x99\x01\n\x10ResponseMetadata\x12\x11\n\tRequestId\x18\x01 \x01(\t\x12\x0e\n\x06\x41\x63tion\x18\x02 \x01(\t\x12\x0f\n\x07Version\x18\x03 \x01(\t\x12\x0f\n\x07Service\x18\x04 \x01(\t\x12\x0e\n\x06Region\x18\x05 \x01(\t\x12\x30\n\x05\x45rror\x18\x06 \x01(\x0b\x32!.Vcloud.Models.Base.ResponseError\".\n\rResponseError\x12\x0c\n\x04\x43ode\x18\x01 \x01(\t\x12\x0f\n\x07Message\x18\x02 \x01(\t:6\n\x0cproduct_type\x12\x1c.google.protobuf.FileOptions\x18\x90N \x01(\t\x88\x01\x01\x42\x94\x01\n\x1d\x63om.bytedanceapi.model.commonB\x04\x42\x61seP\x01Z1github.com/TTvcloud/vcloud-sdk-golang/models/base\xa0\x01\x01\xd8\x01\x01\xc2\x02\x00\xca\x02\x12Vcloud\\Models\\Base\xe2\x02\x19Vcloud\\Models\\GPBMetadatab\x06proto3'
  ,
  dependencies=[google_dot_protobuf_dot_descriptor__pb2.DESCRIPTOR,])


PRODUCT_TYPE_FIELD_NUMBER = 10000
product_type = _descriptor.FieldDescriptor(
  name='product_type', full_name='Vcloud.Models.Base.product_type', index=0,
  number=10000, type=9, cpp_type=9, label=1,
  has_default_value=False, default_value=b"".decode('utf-8'),
  message_type=None, enum_type=None, containing_type=None,
  is_extension=True, extension_scope=None,
  serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key)


_RESPONSEMETADATA = _descriptor.Descriptor(
  name='ResponseMetadata',
  full_name='Vcloud.Models.Base.ResponseMetadata',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='RequestId', full_name='Vcloud.Models.Base.ResponseMetadata.RequestId', index=0,
      number=1, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='Action', full_name='Vcloud.Models.Base.ResponseMetadata.Action', index=1,
      number=2, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='Version', full_name='Vcloud.Models.Base.ResponseMetadata.Version', index=2,
      number=3, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='Service', full_name='Vcloud.Models.Base.ResponseMetadata.Service', index=3,
      number=4, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='Region', full_name='Vcloud.Models.Base.ResponseMetadata.Region', index=4,
      number=5, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='Error', full_name='Vcloud.Models.Base.ResponseMetadata.Error', index=5,
      number=6, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=74,
  serialized_end=227,
)


_RESPONSEERROR = _descriptor.Descriptor(
  name='ResponseError',
  full_name='Vcloud.Models.Base.ResponseError',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='Code', full_name='Vcloud.Models.Base.ResponseError.Code', index=0,
      number=1, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='Message', full_name='Vcloud.Models.Base.ResponseError.Message', index=1,
      number=2, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=229,
  serialized_end=275,
)

_RESPONSEMETADATA.fields_by_name['Error'].message_type = _RESPONSEERROR
DESCRIPTOR.message_types_by_name['ResponseMetadata'] = _RESPONSEMETADATA
DESCRIPTOR.message_types_by_name['ResponseError'] = _RESPONSEERROR
DESCRIPTOR.extensions_by_name['product_type'] = product_type
_sym_db.RegisterFileDescriptor(DESCRIPTOR)

ResponseMetadata = _reflection.GeneratedProtocolMessageType('ResponseMetadata', (_message.Message,), {
  'DESCRIPTOR' : _RESPONSEMETADATA,
  '__module__' : 'base.base_pb2'
  # @@protoc_insertion_point(class_scope:Vcloud.Models.Base.ResponseMetadata)
  })
_sym_db.RegisterMessage(ResponseMetadata)

ResponseError = _reflection.GeneratedProtocolMessageType('ResponseError', (_message.Message,), {
  'DESCRIPTOR' : _RESPONSEERROR,
  '__module__' : 'base.base_pb2'
  # @@protoc_insertion_point(class_scope:Vcloud.Models.Base.ResponseError)
  })
_sym_db.RegisterMessage(ResponseError)

google_dot_protobuf_dot_descriptor__pb2.FileOptions.RegisterExtension(product_type)

DESCRIPTOR._options = None
# @@protoc_insertion_point(module_scope)
