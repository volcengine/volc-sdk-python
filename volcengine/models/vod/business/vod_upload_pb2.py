# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: vod/business/vod_upload.proto

from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from google.protobuf import reflection as _reflection
from google.protobuf import symbol_database as _symbol_database
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()


from volcengine.models.vod.business import vod_common_pb2 as vod_dot_business_dot_vod__common__pb2


DESCRIPTOR = _descriptor.FileDescriptor(
  name='vod/business/vod_upload.proto',
  package='Volcengine.Models.Vod.Business',
  syntax='proto3',
  serialized_options=b'\n!com.volcengine.model.vod.businessB\tVodUploadP\001Z9github.com/volcengine/volc-sdk-golang/models/vod/business\240\001\001\330\001\001\302\002\000\312\002\030Volc\\Models\\Vod\\Business\342\002\033Volc\\Models\\Vod\\GPBMetadata',
  create_key=_descriptor._internal_create_key,
  serialized_pb=b'\n\x1dvod/business/vod_upload.proto\x12\x1eVolcengine.Models.Vod.Business\x1a\x1dvod/business/vod_common.proto\"\xa2\x01\n\x12VodUrlUploadURLSet\x12\x11\n\tSourceUrl\x18\x01 \x01(\t\x12\x14\n\x0c\x43\x61llbackArgs\x18\x02 \x01(\t\x12\x0b\n\x03Md5\x18\x03 \x01(\t\x12\x12\n\nTemplateId\x18\x04 \x01(\t\x12\r\n\x05Title\x18\x05 \x01(\t\x12\x13\n\x0b\x44\x65scription\x18\x06 \x01(\t\x12\x0c\n\x04Tags\x18\x07 \x01(\t\x12\x10\n\x08\x43\x61tegory\x18\x08 \x01(\t\"M\n\x12VodUrlResponseData\x12\x37\n\x04\x44\x61ta\x18\x01 \x03(\x0b\x32).Volcengine.Models.Vod.Business.ValuePair\"-\n\tValuePair\x12\r\n\x05JobId\x18\x01 \x01(\t\x12\x11\n\tSourceUrl\x18\x02 \x01(\t\"R\n\x0cVodQueryData\x12\x42\n\x04\x44\x61ta\x18\x01 \x01(\x0b\x32\x34.Volcengine.Models.Vod.Business.VodQueryUploadResult\"p\n\x14VodQueryUploadResult\x12@\n\rMediaInfoList\x18\x01 \x03(\x0b\x32).Volcengine.Models.Vod.Business.VodURLSet\x12\x16\n\x0eNotExistJobIds\x18\x02 \x03(\t\"^\n\rVodCommitData\x12M\n\x04\x44\x61ta\x18\x01 \x01(\x0b\x32?.Volcengine.Models.Vod.Business.VodCommitUploadInfoResponseData\"\x9a\x01\n\x1fVodCommitUploadInfoResponseData\x12\x0b\n\x03Vid\x18\x01 \x01(\t\x12\x41\n\nSourceInfo\x18\x02 \x01(\x0b\x32-.Volcengine.Models.Vod.Business.VodSourceInfo\x12\x11\n\tPosterUri\x18\x03 \x01(\t\x12\x14\n\x0c\x43\x61llbackArgs\x18\x04 \x01(\t\"\xc5\x01\n\tVodURLSet\x12\x11\n\tRequestId\x18\x01 \x01(\t\x12\r\n\x05JobId\x18\x02 \x01(\t\x12\x11\n\tSourceUrl\x18\x03 \x01(\t\x12\r\n\x05State\x18\x04 \x01(\t\x12\x0b\n\x03Vid\x18\x05 \x01(\t\x12\x11\n\tSpaceName\x18\x06 \x01(\t\x12\x11\n\tAccountId\x18\x07 \x01(\t\x12\x41\n\nSourceInfo\x18\x08 \x01(\x0b\x32-.Volcengine.Models.Vod.Business.VodSourceInfo\"`\n\x18VodApplyUploadInfoResult\x12\x44\n\x04\x44\x61ta\x18\x01 \x01(\x0b\x32\x36.Volcengine.Models.Vod.Business.VodApplyUploadInfoData\"a\n\x16VodApplyUploadInfoData\x12G\n\rUploadAddress\x18\x01 \x01(\x0b\x32\x30.Volcengine.Models.Vod.Business.VodUploadAddress\"\xc2\x01\n\x10VodUploadAddress\x12@\n\nStoreInfos\x18\x01 \x03(\x0b\x32,.Volcengine.Models.Vod.Business.VodStoreInfo\x12\x13\n\x0bUploadHosts\x18\x02 \x03(\t\x12\x43\n\x0cUploadHeader\x18\x03 \x03(\x0b\x32-.Volcengine.Models.Vod.Business.VodHeaderPair\x12\x12\n\nSessionKey\x18\x04 \x01(\t\".\n\x0cVodStoreInfo\x12\x10\n\x08StoreUri\x18\x01 \x01(\t\x12\x0c\n\x04\x41uth\x18\x02 \x01(\t\"+\n\rVodHeaderPair\x12\x0b\n\x03Key\x18\x01 \x01(\t\x12\r\n\x05Value\x18\x02 \x01(\t\"b\n\x19VodCommitUploadInfoResult\x12\x45\n\x04\x44\x61ta\x18\x01 \x01(\x0b\x32\x37.Volcengine.Models.Vod.Business.VodCommitUploadInfoData\"|\n\x17VodCommitUploadInfoData\x12\x0b\n\x03Vid\x18\x01 \x01(\t\x12\x11\n\tPosterUri\x18\x02 \x01(\t\x12\x41\n\nSourceInfo\x18\x03 \x01(\x0b\x32-.Volcengine.Models.Vod.Business.VodSourceInfoB\xad\x01\n!com.volcengine.model.vod.businessB\tVodUploadP\x01Z9github.com/volcengine/volc-sdk-golang/models/vod/business\xa0\x01\x01\xd8\x01\x01\xc2\x02\x00\xca\x02\x18Volc\\Models\\Vod\\Business\xe2\x02\x1bVolc\\Models\\Vod\\GPBMetadatab\x06proto3'
  ,
  dependencies=[vod_dot_business_dot_vod__common__pb2.DESCRIPTOR,])




_VODURLUPLOADURLSET = _descriptor.Descriptor(
  name='VodUrlUploadURLSet',
  full_name='Volcengine.Models.Vod.Business.VodUrlUploadURLSet',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='SourceUrl', full_name='Volcengine.Models.Vod.Business.VodUrlUploadURLSet.SourceUrl', index=0,
      number=1, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='CallbackArgs', full_name='Volcengine.Models.Vod.Business.VodUrlUploadURLSet.CallbackArgs', index=1,
      number=2, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='Md5', full_name='Volcengine.Models.Vod.Business.VodUrlUploadURLSet.Md5', index=2,
      number=3, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='TemplateId', full_name='Volcengine.Models.Vod.Business.VodUrlUploadURLSet.TemplateId', index=3,
      number=4, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='Title', full_name='Volcengine.Models.Vod.Business.VodUrlUploadURLSet.Title', index=4,
      number=5, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='Description', full_name='Volcengine.Models.Vod.Business.VodUrlUploadURLSet.Description', index=5,
      number=6, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='Tags', full_name='Volcengine.Models.Vod.Business.VodUrlUploadURLSet.Tags', index=6,
      number=7, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='Category', full_name='Volcengine.Models.Vod.Business.VodUrlUploadURLSet.Category', index=7,
      number=8, type=9, cpp_type=9, label=1,
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
  serialized_start=97,
  serialized_end=259,
)


_VODURLRESPONSEDATA = _descriptor.Descriptor(
  name='VodUrlResponseData',
  full_name='Volcengine.Models.Vod.Business.VodUrlResponseData',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='Data', full_name='Volcengine.Models.Vod.Business.VodUrlResponseData.Data', index=0,
      number=1, type=11, cpp_type=10, label=3,
      has_default_value=False, default_value=[],
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
  serialized_start=261,
  serialized_end=338,
)


_VALUEPAIR = _descriptor.Descriptor(
  name='ValuePair',
  full_name='Volcengine.Models.Vod.Business.ValuePair',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='JobId', full_name='Volcengine.Models.Vod.Business.ValuePair.JobId', index=0,
      number=1, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='SourceUrl', full_name='Volcengine.Models.Vod.Business.ValuePair.SourceUrl', index=1,
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
  serialized_start=340,
  serialized_end=385,
)


_VODQUERYDATA = _descriptor.Descriptor(
  name='VodQueryData',
  full_name='Volcengine.Models.Vod.Business.VodQueryData',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='Data', full_name='Volcengine.Models.Vod.Business.VodQueryData.Data', index=0,
      number=1, type=11, cpp_type=10, label=1,
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
  serialized_start=387,
  serialized_end=469,
)


_VODQUERYUPLOADRESULT = _descriptor.Descriptor(
  name='VodQueryUploadResult',
  full_name='Volcengine.Models.Vod.Business.VodQueryUploadResult',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='MediaInfoList', full_name='Volcengine.Models.Vod.Business.VodQueryUploadResult.MediaInfoList', index=0,
      number=1, type=11, cpp_type=10, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='NotExistJobIds', full_name='Volcengine.Models.Vod.Business.VodQueryUploadResult.NotExistJobIds', index=1,
      number=2, type=9, cpp_type=9, label=3,
      has_default_value=False, default_value=[],
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
  serialized_start=471,
  serialized_end=583,
)


_VODCOMMITDATA = _descriptor.Descriptor(
  name='VodCommitData',
  full_name='Volcengine.Models.Vod.Business.VodCommitData',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='Data', full_name='Volcengine.Models.Vod.Business.VodCommitData.Data', index=0,
      number=1, type=11, cpp_type=10, label=1,
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
  serialized_start=585,
  serialized_end=679,
)


_VODCOMMITUPLOADINFORESPONSEDATA = _descriptor.Descriptor(
  name='VodCommitUploadInfoResponseData',
  full_name='Volcengine.Models.Vod.Business.VodCommitUploadInfoResponseData',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='Vid', full_name='Volcengine.Models.Vod.Business.VodCommitUploadInfoResponseData.Vid', index=0,
      number=1, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='SourceInfo', full_name='Volcengine.Models.Vod.Business.VodCommitUploadInfoResponseData.SourceInfo', index=1,
      number=2, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='PosterUri', full_name='Volcengine.Models.Vod.Business.VodCommitUploadInfoResponseData.PosterUri', index=2,
      number=3, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='CallbackArgs', full_name='Volcengine.Models.Vod.Business.VodCommitUploadInfoResponseData.CallbackArgs', index=3,
      number=4, type=9, cpp_type=9, label=1,
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
  serialized_start=682,
  serialized_end=836,
)


_VODURLSET = _descriptor.Descriptor(
  name='VodURLSet',
  full_name='Volcengine.Models.Vod.Business.VodURLSet',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='RequestId', full_name='Volcengine.Models.Vod.Business.VodURLSet.RequestId', index=0,
      number=1, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='JobId', full_name='Volcengine.Models.Vod.Business.VodURLSet.JobId', index=1,
      number=2, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='SourceUrl', full_name='Volcengine.Models.Vod.Business.VodURLSet.SourceUrl', index=2,
      number=3, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='State', full_name='Volcengine.Models.Vod.Business.VodURLSet.State', index=3,
      number=4, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='Vid', full_name='Volcengine.Models.Vod.Business.VodURLSet.Vid', index=4,
      number=5, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='SpaceName', full_name='Volcengine.Models.Vod.Business.VodURLSet.SpaceName', index=5,
      number=6, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='AccountId', full_name='Volcengine.Models.Vod.Business.VodURLSet.AccountId', index=6,
      number=7, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='SourceInfo', full_name='Volcengine.Models.Vod.Business.VodURLSet.SourceInfo', index=7,
      number=8, type=11, cpp_type=10, label=1,
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
  serialized_start=839,
  serialized_end=1036,
)


_VODAPPLYUPLOADINFORESULT = _descriptor.Descriptor(
  name='VodApplyUploadInfoResult',
  full_name='Volcengine.Models.Vod.Business.VodApplyUploadInfoResult',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='Data', full_name='Volcengine.Models.Vod.Business.VodApplyUploadInfoResult.Data', index=0,
      number=1, type=11, cpp_type=10, label=1,
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
  serialized_start=1038,
  serialized_end=1134,
)


_VODAPPLYUPLOADINFODATA = _descriptor.Descriptor(
  name='VodApplyUploadInfoData',
  full_name='Volcengine.Models.Vod.Business.VodApplyUploadInfoData',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='UploadAddress', full_name='Volcengine.Models.Vod.Business.VodApplyUploadInfoData.UploadAddress', index=0,
      number=1, type=11, cpp_type=10, label=1,
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
  serialized_start=1136,
  serialized_end=1233,
)


_VODUPLOADADDRESS = _descriptor.Descriptor(
  name='VodUploadAddress',
  full_name='Volcengine.Models.Vod.Business.VodUploadAddress',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='StoreInfos', full_name='Volcengine.Models.Vod.Business.VodUploadAddress.StoreInfos', index=0,
      number=1, type=11, cpp_type=10, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='UploadHosts', full_name='Volcengine.Models.Vod.Business.VodUploadAddress.UploadHosts', index=1,
      number=2, type=9, cpp_type=9, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='UploadHeader', full_name='Volcengine.Models.Vod.Business.VodUploadAddress.UploadHeader', index=2,
      number=3, type=11, cpp_type=10, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='SessionKey', full_name='Volcengine.Models.Vod.Business.VodUploadAddress.SessionKey', index=3,
      number=4, type=9, cpp_type=9, label=1,
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
  serialized_start=1236,
  serialized_end=1430,
)


_VODSTOREINFO = _descriptor.Descriptor(
  name='VodStoreInfo',
  full_name='Volcengine.Models.Vod.Business.VodStoreInfo',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='StoreUri', full_name='Volcengine.Models.Vod.Business.VodStoreInfo.StoreUri', index=0,
      number=1, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='Auth', full_name='Volcengine.Models.Vod.Business.VodStoreInfo.Auth', index=1,
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
  serialized_start=1432,
  serialized_end=1478,
)


_VODHEADERPAIR = _descriptor.Descriptor(
  name='VodHeaderPair',
  full_name='Volcengine.Models.Vod.Business.VodHeaderPair',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='Key', full_name='Volcengine.Models.Vod.Business.VodHeaderPair.Key', index=0,
      number=1, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='Value', full_name='Volcengine.Models.Vod.Business.VodHeaderPair.Value', index=1,
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
  serialized_start=1480,
  serialized_end=1523,
)


_VODCOMMITUPLOADINFORESULT = _descriptor.Descriptor(
  name='VodCommitUploadInfoResult',
  full_name='Volcengine.Models.Vod.Business.VodCommitUploadInfoResult',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='Data', full_name='Volcengine.Models.Vod.Business.VodCommitUploadInfoResult.Data', index=0,
      number=1, type=11, cpp_type=10, label=1,
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
  serialized_start=1525,
  serialized_end=1623,
)


_VODCOMMITUPLOADINFODATA = _descriptor.Descriptor(
  name='VodCommitUploadInfoData',
  full_name='Volcengine.Models.Vod.Business.VodCommitUploadInfoData',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='Vid', full_name='Volcengine.Models.Vod.Business.VodCommitUploadInfoData.Vid', index=0,
      number=1, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='PosterUri', full_name='Volcengine.Models.Vod.Business.VodCommitUploadInfoData.PosterUri', index=1,
      number=2, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='SourceInfo', full_name='Volcengine.Models.Vod.Business.VodCommitUploadInfoData.SourceInfo', index=2,
      number=3, type=11, cpp_type=10, label=1,
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
  serialized_start=1625,
  serialized_end=1749,
)

_VODURLRESPONSEDATA.fields_by_name['Data'].message_type = _VALUEPAIR
_VODQUERYDATA.fields_by_name['Data'].message_type = _VODQUERYUPLOADRESULT
_VODQUERYUPLOADRESULT.fields_by_name['MediaInfoList'].message_type = _VODURLSET
_VODCOMMITDATA.fields_by_name['Data'].message_type = _VODCOMMITUPLOADINFORESPONSEDATA
_VODCOMMITUPLOADINFORESPONSEDATA.fields_by_name['SourceInfo'].message_type = vod_dot_business_dot_vod__common__pb2._VODSOURCEINFO
_VODURLSET.fields_by_name['SourceInfo'].message_type = vod_dot_business_dot_vod__common__pb2._VODSOURCEINFO
_VODAPPLYUPLOADINFORESULT.fields_by_name['Data'].message_type = _VODAPPLYUPLOADINFODATA
_VODAPPLYUPLOADINFODATA.fields_by_name['UploadAddress'].message_type = _VODUPLOADADDRESS
_VODUPLOADADDRESS.fields_by_name['StoreInfos'].message_type = _VODSTOREINFO
_VODUPLOADADDRESS.fields_by_name['UploadHeader'].message_type = _VODHEADERPAIR
_VODCOMMITUPLOADINFORESULT.fields_by_name['Data'].message_type = _VODCOMMITUPLOADINFODATA
_VODCOMMITUPLOADINFODATA.fields_by_name['SourceInfo'].message_type = vod_dot_business_dot_vod__common__pb2._VODSOURCEINFO
DESCRIPTOR.message_types_by_name['VodUrlUploadURLSet'] = _VODURLUPLOADURLSET
DESCRIPTOR.message_types_by_name['VodUrlResponseData'] = _VODURLRESPONSEDATA
DESCRIPTOR.message_types_by_name['ValuePair'] = _VALUEPAIR
DESCRIPTOR.message_types_by_name['VodQueryData'] = _VODQUERYDATA
DESCRIPTOR.message_types_by_name['VodQueryUploadResult'] = _VODQUERYUPLOADRESULT
DESCRIPTOR.message_types_by_name['VodCommitData'] = _VODCOMMITDATA
DESCRIPTOR.message_types_by_name['VodCommitUploadInfoResponseData'] = _VODCOMMITUPLOADINFORESPONSEDATA
DESCRIPTOR.message_types_by_name['VodURLSet'] = _VODURLSET
DESCRIPTOR.message_types_by_name['VodApplyUploadInfoResult'] = _VODAPPLYUPLOADINFORESULT
DESCRIPTOR.message_types_by_name['VodApplyUploadInfoData'] = _VODAPPLYUPLOADINFODATA
DESCRIPTOR.message_types_by_name['VodUploadAddress'] = _VODUPLOADADDRESS
DESCRIPTOR.message_types_by_name['VodStoreInfo'] = _VODSTOREINFO
DESCRIPTOR.message_types_by_name['VodHeaderPair'] = _VODHEADERPAIR
DESCRIPTOR.message_types_by_name['VodCommitUploadInfoResult'] = _VODCOMMITUPLOADINFORESULT
DESCRIPTOR.message_types_by_name['VodCommitUploadInfoData'] = _VODCOMMITUPLOADINFODATA
_sym_db.RegisterFileDescriptor(DESCRIPTOR)

VodUrlUploadURLSet = _reflection.GeneratedProtocolMessageType('VodUrlUploadURLSet', (_message.Message,), {
  'DESCRIPTOR' : _VODURLUPLOADURLSET,
  '__module__' : 'vod.business.vod_upload_pb2'
  # @@protoc_insertion_point(class_scope:Volcengine.Models.Vod.Business.VodUrlUploadURLSet)
  })
_sym_db.RegisterMessage(VodUrlUploadURLSet)

VodUrlResponseData = _reflection.GeneratedProtocolMessageType('VodUrlResponseData', (_message.Message,), {
  'DESCRIPTOR' : _VODURLRESPONSEDATA,
  '__module__' : 'vod.business.vod_upload_pb2'
  # @@protoc_insertion_point(class_scope:Volcengine.Models.Vod.Business.VodUrlResponseData)
  })
_sym_db.RegisterMessage(VodUrlResponseData)

ValuePair = _reflection.GeneratedProtocolMessageType('ValuePair', (_message.Message,), {
  'DESCRIPTOR' : _VALUEPAIR,
  '__module__' : 'vod.business.vod_upload_pb2'
  # @@protoc_insertion_point(class_scope:Volcengine.Models.Vod.Business.ValuePair)
  })
_sym_db.RegisterMessage(ValuePair)

VodQueryData = _reflection.GeneratedProtocolMessageType('VodQueryData', (_message.Message,), {
  'DESCRIPTOR' : _VODQUERYDATA,
  '__module__' : 'vod.business.vod_upload_pb2'
  # @@protoc_insertion_point(class_scope:Volcengine.Models.Vod.Business.VodQueryData)
  })
_sym_db.RegisterMessage(VodQueryData)

VodQueryUploadResult = _reflection.GeneratedProtocolMessageType('VodQueryUploadResult', (_message.Message,), {
  'DESCRIPTOR' : _VODQUERYUPLOADRESULT,
  '__module__' : 'vod.business.vod_upload_pb2'
  # @@protoc_insertion_point(class_scope:Volcengine.Models.Vod.Business.VodQueryUploadResult)
  })
_sym_db.RegisterMessage(VodQueryUploadResult)

VodCommitData = _reflection.GeneratedProtocolMessageType('VodCommitData', (_message.Message,), {
  'DESCRIPTOR' : _VODCOMMITDATA,
  '__module__' : 'vod.business.vod_upload_pb2'
  # @@protoc_insertion_point(class_scope:Volcengine.Models.Vod.Business.VodCommitData)
  })
_sym_db.RegisterMessage(VodCommitData)

VodCommitUploadInfoResponseData = _reflection.GeneratedProtocolMessageType('VodCommitUploadInfoResponseData', (_message.Message,), {
  'DESCRIPTOR' : _VODCOMMITUPLOADINFORESPONSEDATA,
  '__module__' : 'vod.business.vod_upload_pb2'
  # @@protoc_insertion_point(class_scope:Volcengine.Models.Vod.Business.VodCommitUploadInfoResponseData)
  })
_sym_db.RegisterMessage(VodCommitUploadInfoResponseData)

VodURLSet = _reflection.GeneratedProtocolMessageType('VodURLSet', (_message.Message,), {
  'DESCRIPTOR' : _VODURLSET,
  '__module__' : 'vod.business.vod_upload_pb2'
  # @@protoc_insertion_point(class_scope:Volcengine.Models.Vod.Business.VodURLSet)
  })
_sym_db.RegisterMessage(VodURLSet)

VodApplyUploadInfoResult = _reflection.GeneratedProtocolMessageType('VodApplyUploadInfoResult', (_message.Message,), {
  'DESCRIPTOR' : _VODAPPLYUPLOADINFORESULT,
  '__module__' : 'vod.business.vod_upload_pb2'
  # @@protoc_insertion_point(class_scope:Volcengine.Models.Vod.Business.VodApplyUploadInfoResult)
  })
_sym_db.RegisterMessage(VodApplyUploadInfoResult)

VodApplyUploadInfoData = _reflection.GeneratedProtocolMessageType('VodApplyUploadInfoData', (_message.Message,), {
  'DESCRIPTOR' : _VODAPPLYUPLOADINFODATA,
  '__module__' : 'vod.business.vod_upload_pb2'
  # @@protoc_insertion_point(class_scope:Volcengine.Models.Vod.Business.VodApplyUploadInfoData)
  })
_sym_db.RegisterMessage(VodApplyUploadInfoData)

VodUploadAddress = _reflection.GeneratedProtocolMessageType('VodUploadAddress', (_message.Message,), {
  'DESCRIPTOR' : _VODUPLOADADDRESS,
  '__module__' : 'vod.business.vod_upload_pb2'
  # @@protoc_insertion_point(class_scope:Volcengine.Models.Vod.Business.VodUploadAddress)
  })
_sym_db.RegisterMessage(VodUploadAddress)

VodStoreInfo = _reflection.GeneratedProtocolMessageType('VodStoreInfo', (_message.Message,), {
  'DESCRIPTOR' : _VODSTOREINFO,
  '__module__' : 'vod.business.vod_upload_pb2'
  # @@protoc_insertion_point(class_scope:Volcengine.Models.Vod.Business.VodStoreInfo)
  })
_sym_db.RegisterMessage(VodStoreInfo)

VodHeaderPair = _reflection.GeneratedProtocolMessageType('VodHeaderPair', (_message.Message,), {
  'DESCRIPTOR' : _VODHEADERPAIR,
  '__module__' : 'vod.business.vod_upload_pb2'
  # @@protoc_insertion_point(class_scope:Volcengine.Models.Vod.Business.VodHeaderPair)
  })
_sym_db.RegisterMessage(VodHeaderPair)

VodCommitUploadInfoResult = _reflection.GeneratedProtocolMessageType('VodCommitUploadInfoResult', (_message.Message,), {
  'DESCRIPTOR' : _VODCOMMITUPLOADINFORESULT,
  '__module__' : 'vod.business.vod_upload_pb2'
  # @@protoc_insertion_point(class_scope:Volcengine.Models.Vod.Business.VodCommitUploadInfoResult)
  })
_sym_db.RegisterMessage(VodCommitUploadInfoResult)

VodCommitUploadInfoData = _reflection.GeneratedProtocolMessageType('VodCommitUploadInfoData', (_message.Message,), {
  'DESCRIPTOR' : _VODCOMMITUPLOADINFODATA,
  '__module__' : 'vod.business.vod_upload_pb2'
  # @@protoc_insertion_point(class_scope:Volcengine.Models.Vod.Business.VodCommitUploadInfoData)
  })
_sym_db.RegisterMessage(VodCommitUploadInfoData)


DESCRIPTOR._options = None
# @@protoc_insertion_point(module_scope)
