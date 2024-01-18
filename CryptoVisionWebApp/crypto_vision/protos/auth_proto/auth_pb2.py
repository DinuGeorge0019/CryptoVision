# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: protos/auth_proto/auth.proto
# Protobuf Python Version: 4.25.0
"""Generated protocol buffer code."""
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import symbol_database as _symbol_database
from google.protobuf.internal import builder as _builder
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()




DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n\x1cprotos/auth_proto/auth.proto\x12\x0e\x61uthentication\"J\n\x1bUpdateProfilePictureRequest\x12\n\n\x02id\x18\x01 \x01(\x05\x12\x1f\n\x17\x65ncoded_profile_picture\x18\x02 \x01(\t\"/\n\x1cUpdateProfilePictureResponse\x12\x0f\n\x07message\x18\x01 \x01(\t\"_\n\x11UpdateUserRequest\x12\n\n\x02id\x18\x01 \x01(\x05\x12\x10\n\x08username\x18\x02 \x01(\t\x12\r\n\x05\x65mail\x18\x03 \x01(\t\x12\x1d\n\x15wallet_security_stamp\x18\x04 \x01(\t\"%\n\x12UpdateUserResponse\x12\x0f\n\x07message\x18\x01 \x01(\t\"\x1c\n\x0eGetUserRequest\x12\n\n\x02id\x18\x01 \x01(\x05\"r\n\x0fGetUserResponse\x12\x10\n\x08username\x18\x01 \x01(\t\x12\r\n\x05\x65mail\x18\x02 \x01(\t\x12\x1f\n\x17\x65ncoded_profile_picture\x18\x03 \x01(\t\x12\x1d\n\x15wallet_security_stamp\x18\x04 \x01(\t\"2\n\x0cLoginRequest\x12\x10\n\x08username\x18\x01 \x01(\t\x12\x10\n\x08password\x18\x02 \x01(\t\"\x1e\n\rLoginResponse\x12\r\n\x05token\x18\x01 \x01(\t\"X\n\x0fRegisterRequest\x12\x10\n\x08username\x18\x01 \x01(\t\x12\r\n\x05\x65mail\x18\x02 \x01(\t\x12\x11\n\tpassword1\x18\x03 \x01(\t\x12\x11\n\tpassword2\x18\x04 \x01(\t\"#\n\x10RegisterResponse\x12\x0f\n\x07message\x18\x01 \x01(\t\",\n\x1bRequestPasswordResetRequest\x12\r\n\x05\x65mail\x18\x01 \x01(\t\"/\n\x1cRequestPasswordResetResponse\x12\x0f\n\x07message\x18\x01 \x01(\t\";\n\x14ResetPasswordRequest\x12\r\n\x05token\x18\x01 \x01(\t\x12\x14\n\x0cnew_password\x18\x02 \x01(\t\"(\n\x15ResetPasswordResponse\x12\x0f\n\x07message\x18\x01 \x01(\t2\x8e\x05\n\x0e\x41uthentication\x12\x44\n\x05Login\x12\x1c.authentication.LoginRequest\x1a\x1d.authentication.LoginResponse\x12M\n\x08Register\x12\x1f.authentication.RegisterRequest\x1a .authentication.RegisterResponse\x12s\n\x14RequestPasswordReset\x12+.authentication.RequestPasswordResetRequest\x1a,.authentication.RequestPasswordResetResponse\"\x00\x12^\n\rResetPassword\x12$.authentication.ResetPasswordRequest\x1a%.authentication.ResetPasswordResponse\"\x00\x12J\n\x07GetUser\x12\x1e.authentication.GetUserRequest\x1a\x1f.authentication.GetUserResponse\x12S\n\nUpdateUser\x12!.authentication.UpdateUserRequest\x1a\".authentication.UpdateUserResponse\x12q\n\x14UpdateProfilePicture\x12+.authentication.UpdateProfilePictureRequest\x1a,.authentication.UpdateProfilePictureResponseb\x06proto3')

_globals = globals()
_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, _globals)
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'protos.auth_proto.auth_pb2', _globals)
if _descriptor._USE_C_DESCRIPTORS == False:
  DESCRIPTOR._options = None
  _globals['_UPDATEPROFILEPICTUREREQUEST']._serialized_start=48
  _globals['_UPDATEPROFILEPICTUREREQUEST']._serialized_end=122
  _globals['_UPDATEPROFILEPICTURERESPONSE']._serialized_start=124
  _globals['_UPDATEPROFILEPICTURERESPONSE']._serialized_end=171
  _globals['_UPDATEUSERREQUEST']._serialized_start=173
  _globals['_UPDATEUSERREQUEST']._serialized_end=268
  _globals['_UPDATEUSERRESPONSE']._serialized_start=270
  _globals['_UPDATEUSERRESPONSE']._serialized_end=307
  _globals['_GETUSERREQUEST']._serialized_start=309
  _globals['_GETUSERREQUEST']._serialized_end=337
  _globals['_GETUSERRESPONSE']._serialized_start=339
  _globals['_GETUSERRESPONSE']._serialized_end=453
  _globals['_LOGINREQUEST']._serialized_start=455
  _globals['_LOGINREQUEST']._serialized_end=505
  _globals['_LOGINRESPONSE']._serialized_start=507
  _globals['_LOGINRESPONSE']._serialized_end=537
  _globals['_REGISTERREQUEST']._serialized_start=539
  _globals['_REGISTERREQUEST']._serialized_end=627
  _globals['_REGISTERRESPONSE']._serialized_start=629
  _globals['_REGISTERRESPONSE']._serialized_end=664
  _globals['_REQUESTPASSWORDRESETREQUEST']._serialized_start=666
  _globals['_REQUESTPASSWORDRESETREQUEST']._serialized_end=710
  _globals['_REQUESTPASSWORDRESETRESPONSE']._serialized_start=712
  _globals['_REQUESTPASSWORDRESETRESPONSE']._serialized_end=759
  _globals['_RESETPASSWORDREQUEST']._serialized_start=761
  _globals['_RESETPASSWORDREQUEST']._serialized_end=820
  _globals['_RESETPASSWORDRESPONSE']._serialized_start=822
  _globals['_RESETPASSWORDRESPONSE']._serialized_end=862
  _globals['_AUTHENTICATION']._serialized_start=865
  _globals['_AUTHENTICATION']._serialized_end=1519
# @@protoc_insertion_point(module_scope)