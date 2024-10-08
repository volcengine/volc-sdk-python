# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: volcengine/vod/business/vod_object.proto
"""Generated protocol buffer code."""
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import message as _message
from google.protobuf import reflection as _reflection
from google.protobuf import symbol_database as _symbol_database
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()




DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n(volcengine/vod/business/vod_object.proto\x12\x1eVolcengine.Vod.Models.Business\"\x80\x01\n\x1fVodSubmitBlockObjectTasksResult\x12\x11\n\tOperation\x18\x01 \x01(\t\x12J\n\x10OperateFileNames\x18\x02 \x01(\x0b\x32\x30.Volcengine.Vod.Models.Business.OperateFileNames\"\xa9\x01\n\x10OperateFileNames\x12J\n\x10SuccessFileNames\x18\x01 \x03(\x0b\x32\x30.Volcengine.Vod.Models.Business.FileNameTaskInfo\x12I\n\x0f\x46\x61iledFileNames\x18\x02 \x03(\x0b\x32\x30.Volcengine.Vod.Models.Business.FileNameTaskInfo\"E\n\x10\x46ileNameTaskInfo\x12\x10\n\x08\x46ileName\x18\x01 \x01(\t\x12\x0f\n\x07Message\x18\x02 \x01(\t\x12\x0e\n\x06TaskId\x18\x03 \x01(\t\"r\n\x1dVodListBlockObjectTasksResult\x12Q\n\x14ObjectBlockTaskInfos\x18\x01 \x03(\x0b\x32\x33.Volcengine.Vod.Models.Business.ObjectBlockTaskInfo\"\xcb\x01\n\x13ObjectBlockTaskInfo\x12\x0e\n\x06Status\x18\x01 \x01(\t\x12\x0e\n\x06TaskId\x18\x02 \x01(\t\x12\x10\n\x08\x46ileName\x18\x03 \x01(\t\x12\x15\n\rRefreshStatus\x18\x04 \x01(\t\x12\x11\n\tOperation\x18\x05 \x01(\t\x12\x15\n\rRefreshTaskId\x18\x06 \x01(\t\x12\x41\n\x0cRefreshInfos\x18\x07 \x03(\x0b\x32+.Volcengine.Vod.Models.Business.RefreshInfo\";\n\x0bRefreshInfo\x12\x0b\n\x03Url\x18\x01 \x01(\t\x12\x0e\n\x06Status\x18\x02 \x01(\t\x12\x0f\n\x07Process\x18\x03 \x01(\tB\xcd\x01\n)com.volcengine.service.vod.model.businessB\tVodObjectP\x01ZAgithub.com/volcengine/volc-sdk-golang/service/vod/models/business\xa0\x01\x01\xd8\x01\x01\xc2\x02\x00\xca\x02 Volc\\Service\\Vod\\Models\\Business\xe2\x02#Volc\\Service\\Vod\\Models\\GPBMetadatab\x06proto3')



_VODSUBMITBLOCKOBJECTTASKSRESULT = DESCRIPTOR.message_types_by_name['VodSubmitBlockObjectTasksResult']
_OPERATEFILENAMES = DESCRIPTOR.message_types_by_name['OperateFileNames']
_FILENAMETASKINFO = DESCRIPTOR.message_types_by_name['FileNameTaskInfo']
_VODLISTBLOCKOBJECTTASKSRESULT = DESCRIPTOR.message_types_by_name['VodListBlockObjectTasksResult']
_OBJECTBLOCKTASKINFO = DESCRIPTOR.message_types_by_name['ObjectBlockTaskInfo']
_REFRESHINFO = DESCRIPTOR.message_types_by_name['RefreshInfo']
VodSubmitBlockObjectTasksResult = _reflection.GeneratedProtocolMessageType('VodSubmitBlockObjectTasksResult', (_message.Message,), {
  'DESCRIPTOR' : _VODSUBMITBLOCKOBJECTTASKSRESULT,
  '__module__' : 'volcengine.vod.business.vod_object_pb2'
  # @@protoc_insertion_point(class_scope:Volcengine.Vod.Models.Business.VodSubmitBlockObjectTasksResult)
  })
_sym_db.RegisterMessage(VodSubmitBlockObjectTasksResult)

OperateFileNames = _reflection.GeneratedProtocolMessageType('OperateFileNames', (_message.Message,), {
  'DESCRIPTOR' : _OPERATEFILENAMES,
  '__module__' : 'volcengine.vod.business.vod_object_pb2'
  # @@protoc_insertion_point(class_scope:Volcengine.Vod.Models.Business.OperateFileNames)
  })
_sym_db.RegisterMessage(OperateFileNames)

FileNameTaskInfo = _reflection.GeneratedProtocolMessageType('FileNameTaskInfo', (_message.Message,), {
  'DESCRIPTOR' : _FILENAMETASKINFO,
  '__module__' : 'volcengine.vod.business.vod_object_pb2'
  # @@protoc_insertion_point(class_scope:Volcengine.Vod.Models.Business.FileNameTaskInfo)
  })
_sym_db.RegisterMessage(FileNameTaskInfo)

VodListBlockObjectTasksResult = _reflection.GeneratedProtocolMessageType('VodListBlockObjectTasksResult', (_message.Message,), {
  'DESCRIPTOR' : _VODLISTBLOCKOBJECTTASKSRESULT,
  '__module__' : 'volcengine.vod.business.vod_object_pb2'
  # @@protoc_insertion_point(class_scope:Volcengine.Vod.Models.Business.VodListBlockObjectTasksResult)
  })
_sym_db.RegisterMessage(VodListBlockObjectTasksResult)

ObjectBlockTaskInfo = _reflection.GeneratedProtocolMessageType('ObjectBlockTaskInfo', (_message.Message,), {
  'DESCRIPTOR' : _OBJECTBLOCKTASKINFO,
  '__module__' : 'volcengine.vod.business.vod_object_pb2'
  # @@protoc_insertion_point(class_scope:Volcengine.Vod.Models.Business.ObjectBlockTaskInfo)
  })
_sym_db.RegisterMessage(ObjectBlockTaskInfo)

RefreshInfo = _reflection.GeneratedProtocolMessageType('RefreshInfo', (_message.Message,), {
  'DESCRIPTOR' : _REFRESHINFO,
  '__module__' : 'volcengine.vod.business.vod_object_pb2'
  # @@protoc_insertion_point(class_scope:Volcengine.Vod.Models.Business.RefreshInfo)
  })
_sym_db.RegisterMessage(RefreshInfo)

if _descriptor._USE_C_DESCRIPTORS == False:

  DESCRIPTOR._options = None
  DESCRIPTOR._serialized_options = b'\n)com.volcengine.service.vod.model.businessB\tVodObjectP\001ZAgithub.com/volcengine/volc-sdk-golang/service/vod/models/business\240\001\001\330\001\001\302\002\000\312\002 Volc\\Service\\Vod\\Models\\Business\342\002#Volc\\Service\\Vod\\Models\\GPBMetadata'
  _VODSUBMITBLOCKOBJECTTASKSRESULT._serialized_start=77
  _VODSUBMITBLOCKOBJECTTASKSRESULT._serialized_end=205
  _OPERATEFILENAMES._serialized_start=208
  _OPERATEFILENAMES._serialized_end=377
  _FILENAMETASKINFO._serialized_start=379
  _FILENAMETASKINFO._serialized_end=448
  _VODLISTBLOCKOBJECTTASKSRESULT._serialized_start=450
  _VODLISTBLOCKOBJECTTASKSRESULT._serialized_end=564
  _OBJECTBLOCKTASKINFO._serialized_start=567
  _OBJECTBLOCKTASKINFO._serialized_end=770
  _REFRESHINFO._serialized_start=772
  _REFRESHINFO._serialized_end=831
# @@protoc_insertion_point(module_scope)
