# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: volcengine/vod/business/vod_reporter.proto
"""Generated protocol buffer code."""
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import message as _message
from google.protobuf import reflection as _reflection
from google.protobuf import symbol_database as _symbol_database
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()




DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n*volcengine/vod/business/vod_reporter.proto\x12\x1eVolcengine.Vod.Models.Business\"X\n\x14VodReportEventResult\x12@\n\x04\x44\x61ta\x18\x01 \x01(\x0b\x32\x32.Volcengine.Vod.Models.Business.VodReportEventData\"\x14\n\x12VodReportEventDataB\xcf\x01\n)com.volcengine.service.vod.model.businessB\x0bVodReporterP\x01ZAgithub.com/volcengine/volc-sdk-golang/service/vod/models/business\xa0\x01\x01\xd8\x01\x01\xc2\x02\x00\xca\x02 Volc\\Service\\Vod\\Models\\Business\xe2\x02#Volc\\Service\\Vod\\Models\\GPBMetadatab\x06proto3')



_VODREPORTEVENTRESULT = DESCRIPTOR.message_types_by_name['VodReportEventResult']
_VODREPORTEVENTDATA = DESCRIPTOR.message_types_by_name['VodReportEventData']
VodReportEventResult = _reflection.GeneratedProtocolMessageType('VodReportEventResult', (_message.Message,), {
  'DESCRIPTOR' : _VODREPORTEVENTRESULT,
  '__module__' : 'volcengine.vod.business.vod_reporter_pb2'
  # @@protoc_insertion_point(class_scope:Volcengine.Vod.Models.Business.VodReportEventResult)
  })
_sym_db.RegisterMessage(VodReportEventResult)

VodReportEventData = _reflection.GeneratedProtocolMessageType('VodReportEventData', (_message.Message,), {
  'DESCRIPTOR' : _VODREPORTEVENTDATA,
  '__module__' : 'volcengine.vod.business.vod_reporter_pb2'
  # @@protoc_insertion_point(class_scope:Volcengine.Vod.Models.Business.VodReportEventData)
  })
_sym_db.RegisterMessage(VodReportEventData)

if _descriptor._USE_C_DESCRIPTORS == False:

  DESCRIPTOR._options = None
  DESCRIPTOR._serialized_options = b'\n)com.volcengine.service.vod.model.businessB\013VodReporterP\001ZAgithub.com/volcengine/volc-sdk-golang/service/vod/models/business\240\001\001\330\001\001\302\002\000\312\002 Volc\\Service\\Vod\\Models\\Business\342\002#Volc\\Service\\Vod\\Models\\GPBMetadata'
  _VODREPORTEVENTRESULT._serialized_start=78
  _VODREPORTEVENTRESULT._serialized_end=166
  _VODREPORTEVENTDATA._serialized_start=168
  _VODREPORTEVENTDATA._serialized_end=188
# @@protoc_insertion_point(module_scope)
