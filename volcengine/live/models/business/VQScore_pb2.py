# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: live/business/VQScore.proto
"""Generated protocol buffer code."""
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import message as _message
from google.protobuf import reflection as _reflection
from google.protobuf import symbol_database as _symbol_database
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()




DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n\x1blive/business/VQScore.proto\x12\x1fVolcengine.Live.Models.Business\"\x17\n\tVQScoreID\x12\n\n\x02ID\x18\x01 \x01(\t\"-\n\tScoreInfo\x12\x11\n\tPointTime\x18\x01 \x01(\t\x12\r\n\x05Score\x18\x02 \x01(\x02\"d\n\rAddrScoreInfo\x12\x10\n\x08\x41\x64\x64rType\x18\x01 \x01(\x03\x12\x41\n\rScoreInfoList\x18\x02 \x03(\x0b\x32*.Volcengine.Live.Models.Business.ScoreInfo\"\x88\x02\n\x0bVQScoreInfo\x12\x10\n\x08MainAddr\x18\x01 \x01(\t\x12\x14\n\x0c\x43ontrastAddr\x18\x02 \x01(\t\x12\x10\n\x08\x44uration\x18\x03 \x01(\x03\x12\x15\n\rTotalPointNum\x18\x04 \x01(\x03\x12\x18\n\x10MainAverageScore\x18\x05 \x01(\x02\x12\x1c\n\x14\x43ontrastAverageScore\x18\x06 \x01(\x02\x12\x12\n\nDifference\x18\x07 \x01(\x02\x12\x15\n\rDifferencePer\x18\x08 \x01(\x02\x12\x45\n\rAddrScoreList\x18\t \x03(\x0b\x32..Volcengine.Live.Models.Business.AddrScoreInfo\"R\n\x0fVQScoreTaskInfo\x12\n\n\x02ID\x18\x01 \x01(\t\x12\x10\n\x08\x44uration\x18\x02 \x01(\x03\x12\x0e\n\x06Status\x18\x03 \x01(\x03\x12\x11\n\tAccountID\x18\x04 \x01(\t\"\x8c\x01\n\x13VQScoreTaskListInfo\x12\x11\n\tStartTime\x18\x02 \x01(\t\x12\x0f\n\x07\x45ndTime\x18\x03 \x01(\t\x12\r\n\x05Total\x18\x04 \x01(\x03\x12\x42\n\x08TaskList\x18\x05 \x03(\x0b\x32\x30.Volcengine.Live.Models.Business.VQScoreTaskInfoB\xcf\x01\n*com.volcengine.service.live.model.businessB\x07VQScoreP\x01ZBgithub.com/volcengine/volc-sdk-golang/service/live/models/business\xa0\x01\x01\xd8\x01\x01\xc2\x02\x00\xca\x02!Volc\\Service\\Live\\Models\\Business\xe2\x02$Volc\\Service\\Live\\Models\\GPBMetadatab\x06proto3')



_VQSCOREID = DESCRIPTOR.message_types_by_name['VQScoreID']
_SCOREINFO = DESCRIPTOR.message_types_by_name['ScoreInfo']
_ADDRSCOREINFO = DESCRIPTOR.message_types_by_name['AddrScoreInfo']
_VQSCOREINFO = DESCRIPTOR.message_types_by_name['VQScoreInfo']
_VQSCORETASKINFO = DESCRIPTOR.message_types_by_name['VQScoreTaskInfo']
_VQSCORETASKLISTINFO = DESCRIPTOR.message_types_by_name['VQScoreTaskListInfo']
VQScoreID = _reflection.GeneratedProtocolMessageType('VQScoreID', (_message.Message,), {
  'DESCRIPTOR' : _VQSCOREID,
  '__module__' : 'live.business.VQScore_pb2'
  # @@protoc_insertion_point(class_scope:Volcengine.Live.Models.Business.VQScoreID)
  })
_sym_db.RegisterMessage(VQScoreID)

ScoreInfo = _reflection.GeneratedProtocolMessageType('ScoreInfo', (_message.Message,), {
  'DESCRIPTOR' : _SCOREINFO,
  '__module__' : 'live.business.VQScore_pb2'
  # @@protoc_insertion_point(class_scope:Volcengine.Live.Models.Business.ScoreInfo)
  })
_sym_db.RegisterMessage(ScoreInfo)

AddrScoreInfo = _reflection.GeneratedProtocolMessageType('AddrScoreInfo', (_message.Message,), {
  'DESCRIPTOR' : _ADDRSCOREINFO,
  '__module__' : 'live.business.VQScore_pb2'
  # @@protoc_insertion_point(class_scope:Volcengine.Live.Models.Business.AddrScoreInfo)
  })
_sym_db.RegisterMessage(AddrScoreInfo)

VQScoreInfo = _reflection.GeneratedProtocolMessageType('VQScoreInfo', (_message.Message,), {
  'DESCRIPTOR' : _VQSCOREINFO,
  '__module__' : 'live.business.VQScore_pb2'
  # @@protoc_insertion_point(class_scope:Volcengine.Live.Models.Business.VQScoreInfo)
  })
_sym_db.RegisterMessage(VQScoreInfo)

VQScoreTaskInfo = _reflection.GeneratedProtocolMessageType('VQScoreTaskInfo', (_message.Message,), {
  'DESCRIPTOR' : _VQSCORETASKINFO,
  '__module__' : 'live.business.VQScore_pb2'
  # @@protoc_insertion_point(class_scope:Volcengine.Live.Models.Business.VQScoreTaskInfo)
  })
_sym_db.RegisterMessage(VQScoreTaskInfo)

VQScoreTaskListInfo = _reflection.GeneratedProtocolMessageType('VQScoreTaskListInfo', (_message.Message,), {
  'DESCRIPTOR' : _VQSCORETASKLISTINFO,
  '__module__' : 'live.business.VQScore_pb2'
  # @@protoc_insertion_point(class_scope:Volcengine.Live.Models.Business.VQScoreTaskListInfo)
  })
_sym_db.RegisterMessage(VQScoreTaskListInfo)

if _descriptor._USE_C_DESCRIPTORS == False:

  DESCRIPTOR._options = None
  DESCRIPTOR._serialized_options = b'\n*com.volcengine.service.live.model.businessB\007VQScoreP\001ZBgithub.com/volcengine/volc-sdk-golang/service/live/models/business\240\001\001\330\001\001\302\002\000\312\002!Volc\\Service\\Live\\Models\\Business\342\002$Volc\\Service\\Live\\Models\\GPBMetadata'
  _VQSCOREID._serialized_start=64
  _VQSCOREID._serialized_end=87
  _SCOREINFO._serialized_start=89
  _SCOREINFO._serialized_end=134
  _ADDRSCOREINFO._serialized_start=136
  _ADDRSCOREINFO._serialized_end=236
  _VQSCOREINFO._serialized_start=239
  _VQSCOREINFO._serialized_end=503
  _VQSCORETASKINFO._serialized_start=505
  _VQSCORETASKINFO._serialized_end=587
  _VQSCORETASKLISTINFO._serialized_start=590
  _VQSCORETASKLISTINFO._serialized_end=730
# @@protoc_insertion_point(module_scope)
