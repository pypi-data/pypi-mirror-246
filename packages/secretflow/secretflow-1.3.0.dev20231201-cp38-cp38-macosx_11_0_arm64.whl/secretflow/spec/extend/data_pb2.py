# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: secretflow/spec/extend/data.proto
"""Generated protocol buffer code."""
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import message as _message
from google.protobuf import reflection as _reflection
from google.protobuf import symbol_database as _symbol_database
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()




DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n!secretflow/spec/extend/data.proto\x12\x16secretflow.spec.extend\"\xad\x01\n\x16\x44\x65viceObjectCollection\x12I\n\x04objs\x18\x01 \x03(\x0b\x32;.secretflow.spec.extend.DeviceObjectCollection.DeviceObject\x12\x13\n\x0bpublic_info\x18\x02 \x01(\t\x1a\x33\n\x0c\x44\x65viceObject\x12\x0c\n\x04type\x18\x01 \x01(\t\x12\x15\n\rdata_ref_idxs\x18\x02 \x03(\x05\x42\x1c\n\x1aorg.secretflow.spec.extendb\x06proto3')



_DEVICEOBJECTCOLLECTION = DESCRIPTOR.message_types_by_name['DeviceObjectCollection']
_DEVICEOBJECTCOLLECTION_DEVICEOBJECT = _DEVICEOBJECTCOLLECTION.nested_types_by_name['DeviceObject']
DeviceObjectCollection = _reflection.GeneratedProtocolMessageType('DeviceObjectCollection', (_message.Message,), {

  'DeviceObject' : _reflection.GeneratedProtocolMessageType('DeviceObject', (_message.Message,), {
    'DESCRIPTOR' : _DEVICEOBJECTCOLLECTION_DEVICEOBJECT,
    '__module__' : 'secretflow.spec.extend.data_pb2'
    # @@protoc_insertion_point(class_scope:secretflow.spec.extend.DeviceObjectCollection.DeviceObject)
    })
  ,
  'DESCRIPTOR' : _DEVICEOBJECTCOLLECTION,
  '__module__' : 'secretflow.spec.extend.data_pb2'
  # @@protoc_insertion_point(class_scope:secretflow.spec.extend.DeviceObjectCollection)
  })
_sym_db.RegisterMessage(DeviceObjectCollection)
_sym_db.RegisterMessage(DeviceObjectCollection.DeviceObject)

if _descriptor._USE_C_DESCRIPTORS == False:

  DESCRIPTOR._options = None
  DESCRIPTOR._serialized_options = b'\n\032org.secretflow.spec.extend'
  _DEVICEOBJECTCOLLECTION._serialized_start=62
  _DEVICEOBJECTCOLLECTION._serialized_end=235
  _DEVICEOBJECTCOLLECTION_DEVICEOBJECT._serialized_start=184
  _DEVICEOBJECTCOLLECTION_DEVICEOBJECT._serialized_end=235
# @@protoc_insertion_point(module_scope)
