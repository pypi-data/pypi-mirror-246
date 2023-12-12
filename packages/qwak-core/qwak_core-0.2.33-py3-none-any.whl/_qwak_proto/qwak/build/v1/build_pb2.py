# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: qwak/build/v1/build.proto
"""Generated protocol buffer code."""
from google.protobuf.internal import enum_type_wrapper
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import message as _message
from google.protobuf import reflection as _reflection
from google.protobuf import symbol_database as _symbol_database
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()


from google.protobuf import timestamp_pb2 as google_dot_protobuf_dot_timestamp__pb2
from _qwak_proto.qwak.builds import build_pb2 as qwak_dot_builds_dot_build__pb2


DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n\x19qwak/build/v1/build.proto\x12\x11\x63om.qwak.build.v1\x1a\x1fgoogle/protobuf/timestamp.proto\x1a\x17qwak/builds/build.proto\"\xda\x01\n\x0bModelSchema\x12+\n\x08\x65ntities\x18\x01 \x03(\x0b\x32\x19.com.qwak.build.v1.Entity\x12,\n\x08\x66\x65\x61tures\x18\x02 \x03(\x0b\x32\x1a.com.qwak.build.v1.Feature\x12\x32\n\x0bpredictions\x18\x03 \x03(\x0b\x32\x1d.com.qwak.build.v1.Prediction\x12<\n\x10inference_output\x18\x04 \x03(\x0b\x32\".com.qwak.build.v1.InferenceOutput\"B\n\x06\x45ntity\x12\x0c\n\x04name\x18\x01 \x01(\t\x12*\n\x04type\x18\x02 \x01(\x0b\x32\x1c.com.qwak.build.v1.ValueType\"\xa8\x04\n\x07\x46\x65\x61ture\x12\x38\n\rbatch_feature\x18\x01 \x01(\x0b\x32\x1f.com.qwak.build.v1.BatchFeatureH\x00\x12>\n\x10\x65xplicit_feature\x18\x02 \x01(\x0b\x32\".com.qwak.build.v1.ExplicitFeatureH\x00\x12@\n\x12on_the_fly_feature\x18\x03 \x01(\x0b\x32\".com.qwak.build.v1.OnTheFlyFeatureH\x00\x12@\n\x11streaming_feature\x18\x04 \x01(\x0b\x32#.com.qwak.build.v1.StreamingFeatureH\x00\x12\x38\n\rrequest_input\x18\x05 \x01(\x0b\x32\x1f.com.qwak.build.v1.RequestInputH\x00\x12W\n\x1dstreaming_aggregation_feature\x18\x06 \x01(\x0b\x32..com.qwak.build.v1.StreamingAggregationFeatureH\x00\x12=\n\x10\x62\x61tch_feature_v1\x18\x07 \x01(\x0b\x32!.com.qwak.build.v1.BatchFeatureV1H\x00\x12\x45\n\x14streaming_feature_v1\x18\x08 \x01(\x0b\x32%.com.qwak.build.v1.StreamingFeatureV1H\x00\x42\x06\n\x04type\"\x85\x01\n\x0fOnTheFlyFeature\x12)\n\x06\x65ntity\x18\x01 \x01(\x0b\x32\x19.com.qwak.build.v1.Entity\x12\x0c\n\x04name\x18\x02 \x01(\t\x12\x39\n\x0fsource_features\x18\x03 \x03(\x0b\x32 .com.qwak.build.v1.SourceFeature\"I\n\x0e\x42\x61tchFeatureV1\x12)\n\x06\x65ntity\x18\x01 \x01(\x0b\x32\x19.com.qwak.build.v1.Entity\x12\x0c\n\x04name\x18\x02 \x01(\t\"M\n\x12StreamingFeatureV1\x12)\n\x06\x65ntity\x18\x01 \x01(\x0b\x32\x19.com.qwak.build.v1.Entity\x12\x0c\n\x04name\x18\x02 \x01(\t\"G\n\x0c\x42\x61tchFeature\x12)\n\x06\x65ntity\x18\x01 \x01(\x0b\x32\x19.com.qwak.build.v1.Entity\x12\x0c\n\x04name\x18\x02 \x01(\t\"K\n\x10StreamingFeature\x12)\n\x06\x65ntity\x18\x01 \x01(\x0b\x32\x19.com.qwak.build.v1.Entity\x12\x0c\n\x04name\x18\x02 \x01(\t\"V\n\x1bStreamingAggregationFeature\x12)\n\x06\x65ntity\x18\x01 \x01(\x0b\x32\x19.com.qwak.build.v1.Entity\x12\x0c\n\x04name\x18\x02 \x01(\t\"K\n\x0f\x45xplicitFeature\x12\x0c\n\x04name\x18\x01 \x01(\t\x12*\n\x04type\x18\x02 \x01(\x0b\x32\x1c.com.qwak.build.v1.ValueType\"H\n\x0cRequestInput\x12\x0c\n\x04name\x18\x01 \x01(\t\x12*\n\x04type\x18\x02 \x01(\x0b\x32\x1c.com.qwak.build.v1.ValueType\"\x91\x01\n\rSourceFeature\x12>\n\x10\x65xplicit_feature\x18\x01 \x01(\x0b\x32\".com.qwak.build.v1.ExplicitFeatureH\x00\x12\x38\n\rrequest_input\x18\x02 \x01(\x0b\x32\x1f.com.qwak.build.v1.RequestInputH\x00\x42\x06\n\x04type\"F\n\nPrediction\x12\x0c\n\x04name\x18\x01 \x01(\t\x12*\n\x04type\x18\x02 \x01(\x0b\x32\x1c.com.qwak.build.v1.ValueType\"K\n\x0fInferenceOutput\x12\x0c\n\x04name\x18\x01 \x01(\t\x12*\n\x04type\x18\x02 \x01(\x0b\x32\x1c.com.qwak.build.v1.ValueType\"\xa1\x01\n\tValueType\x12\x30\n\x04type\x18\x01 \x01(\x0e\x32\".com.qwak.build.v1.ValueType.Types\"b\n\x05Types\x12\x0b\n\x07INVALID\x10\x00\x12\t\n\x05\x42YTES\x10\x01\x12\n\n\x06STRING\x10\x02\x12\t\n\x05INT32\x10\x03\x12\t\n\x05INT64\x10\x04\x12\n\n\x06\x44OUBLE\x10\x05\x12\t\n\x05\x46LOAT\x10\x06\x12\x08\n\x04\x42OOL\x10\x07\"j\n\x11ParameterCategory\"U\n\x08\x43\x61tegory\x12\x0b\n\x07INVALID\x10\x00\x12\n\n\x06\x45NTITY\x10\x01\x12\x0b\n\x07\x46\x45\x41TURE\x10\x02\x12\x0e\n\nPREDICTION\x10\x03\x12\x13\n\x0fINFERENCEOUTPUT\x10\x04\"\xc1\x05\n\x05\x42uild\x12\x0f\n\x07\x62uildId\x18\x01 \x01(\t\x12\x10\n\x08\x63ommitId\x18\x02 \x01(\t\x12\x10\n\x08\x62ranchId\x18\x03 \x01(\t\x12\x13\n\x0b\x62uildConfig\x18\x04 \x01(\t\x12\x34\n\x0c\x62uild_status\x18\x05 \x01(\x0e\x32\x1e.com.qwak.build.v1.BuildStatus\x12\x0c\n\x04tags\x18\x06 \x03(\t\x12\r\n\x05steps\x18\x07 \x03(\t\x12\x34\n\x06params\x18\x08 \x03(\x0b\x32$.com.qwak.build.v1.Build.ParamsEntry\x12\x36\n\x07metrics\x18\t \x03(\x0b\x32%.com.qwak.build.v1.Build.MetricsEntry\x12\x34\n\x0cmodel_schema\x18\n \x01(\x0b\x32\x1e.com.qwak.build.v1.ModelSchema\x12\'\n\x05\x61udit\x18\x0b \x01(\x0b\x32\x18.com.qwak.build.v1.Audit\x12\x12\n\nmodel_uuid\x18\x0c \x01(\t\x12\x13\n\x0bsdk_version\x18\r \x01(\t\x12\x16\n\x0eimage_name_tag\x18\x0e \x01(\t\x12J\n\x1b\x62uild_configuration_message\x18\x0f \x01(\x0b\x32%.com.qwak.build.v1.BuildConfiguration\x12,\n\x08\x65nd_date\x18\x10 \x01(\x0b\x32\x1a.google.protobuf.Timestamp\x12\x16\n\x0e\x65nvironment_id\x18\x11 \x01(\t\x12\x1c\n\x14\x62uild_destined_image\x18\x12 \x01(\t\x1a-\n\x0bParamsEntry\x12\x0b\n\x03key\x18\x01 \x01(\t\x12\r\n\x05value\x18\x02 \x01(\t:\x02\x38\x01\x1a.\n\x0cMetricsEntry\x12\x0b\n\x03key\x18\x01 \x01(\t\x12\r\n\x05value\x18\x02 \x01(\x02:\x02\x38\x01\"\x9b\x01\n\x05\x41udit\x12\x12\n\ncreated_by\x18\x01 \x01(\t\x12.\n\ncreated_at\x18\x02 \x01(\x0b\x32\x1a.google.protobuf.Timestamp\x12\x18\n\x10last_modified_by\x18\x03 \x01(\t\x12\x34\n\x10last_modified_at\x18\x04 \x01(\x0b\x32\x1a.google.protobuf.Timestamp\"\xb3\x02\n\x12\x42uildConfiguration\x12<\n\x10\x62uild_properties\x18\x01 \x01(\x0b\x32\".com.qwak.build.v1.BuildProperties\x12\x36\n\tbuild_env\x18\x02 \x01(\x0b\x32#.com.qwak.build.v1.BuildEnvironment\x12\x36\n\tpre_build\x18\x03 \x01(\x0b\x32#.com.qwak.build.v1.BuildEnvironment\x12\x37\n\npost_build\x18\x04 \x01(\x0b\x32#.com.qwak.build.v1.BuildEnvironment\x12%\n\x04step\x18\x05 \x01(\x0b\x32\x17.com.qwak.build.v1.Step\x12\x0f\n\x07verbose\x18\x06 \x01(\x05\"\xba\x01\n\x0f\x42uildProperties\x12\x10\n\x08model_id\x18\x01 \x01(\t\x12\x33\n\tmodel_uri\x18\x02 \x01(\x0b\x32 .com.qwak.build.v1.BuildModelUri\x12\x0c\n\x04tags\x18\x03 \x03(\t\x12\x10\n\x08\x62uild_id\x18\x04 \x01(\t\x12\x0e\n\x06\x62ranch\x18\x05 \x01(\t\x12\x18\n\x10\x65nvironment_name\x18\x06 \x01(\t\x12\x16\n\x0egpu_compatible\x18\x07 \x01(\x08\"B\n\rBuildModelUri\x12\x0b\n\x03uri\x18\x01 \x01(\t\x12\x12\n\ngit_branch\x18\x02 \x01(\t\x12\x10\n\x08main_dir\x18\x03 \x01(\t\"\xd4\x01\n\x10\x42uildEnvironment\x12.\n\x06\x64ocker\x18\x01 \x01(\x0b\x32\x1e.com.qwak.build.v1.DockerBuild\x12,\n\x05local\x18\x02 \x01(\x0b\x32\x1d.com.qwak.build.v1.LocalBuild\x12\x32\n\npython_env\x18\x03 \x01(\x0b\x32\x1e.com.qwak.build.v1.PythonBuild\x12.\n\x06remote\x18\x04 \x01(\x0b\x32\x1e.com.qwak.build.v1.RemoteBuild\"\x85\x02\n\x0b\x44ockerBuild\x12\x12\n\nbase_image\x18\x01 \x01(\t\x12\x41\n\nbuild_args\x18\x02 \x03(\x0b\x32-.com.qwak.build.v1.DockerBuild.BuildArgsEntry\x12\x10\n\x08\x65nv_vars\x18\x03 \x03(\t\x12\x10\n\x08no_cache\x18\x04 \x01(\x08\x12\x0e\n\x06params\x18\x05 \x03(\t\x12\x1c\n\x14\x61ssumed_iam_role_arn\x18\x06 \x01(\t\x12\r\n\x05\x63\x61\x63he\x18\x07 \x01(\x08\x12\x0c\n\x04push\x18\x08 \x01(\x08\x1a\x30\n\x0e\x42uildArgsEntry\x12\x0b\n\x03key\x18\x01 \x01(\t\x12\r\n\x05value\x18\x02 \x01(\t:\x02\x38\x01\"2\n\nLocalBuild\x12\x13\n\x0b\x61ws_profile\x18\x01 \x01(\t\x12\x0f\n\x07no_push\x18\x02 \x01(\x08\"\x8c\x02\n\x0bPythonBuild\x12 \n\x18qwak_sdk_extra_index_url\x18\x01 \x01(\t\x12>\n\nvirtualenv\x18\x02 \x01(\x0b\x32*.com.qwak.build.v1.VirtualEnvironmentBuild\x12,\n\x05\x63onda\x18\x03 \x01(\x0b\x32\x1d.com.qwak.build.v1.CondaBuild\x12.\n\x06poetry\x18\x04 \x01(\x0b\x32\x1e.com.qwak.build.v1.PoetryBuild\x12\x1c\n\x14\x64\x65pendency_file_path\x18\x05 \x01(\t\x12\x1f\n\x17use_deprecated_resolver\x18\x06 \x01(\x08\" \n\nCondaBuild\x12\x12\n\nconda_file\x18\x01 \x01(\t\"8\n\x0bPoetryBuild\x12\x16\n\x0epython_version\x18\x01 \x01(\t\x12\x11\n\tlock_file\x18\x02 \x01(\t\"K\n\x17VirtualEnvironmentBuild\x12\x16\n\x0epython_version\x18\x01 \x01(\t\x12\x18\n\x10requirements_txt\x18\x02 \x01(\t\"\\\n\x0bRemoteBuild\x12\x11\n\tis_remote\x18\x01 \x01(\x08\x12:\n\tresources\x18\x02 \x01(\x0b\x32\'.com.qwak.build.v1.RemoteBuildResources\"\x8f\x01\n\x14RemoteBuildResources\x12\x0c\n\x04\x63pus\x18\x01 \x01(\x02\x12\x0e\n\x06memory\x18\x02 \x01(\t\x12\x33\n\x08gpu_type\x18\x03 \x01(\x0e\x32!.qwak.builds.orchestrator.GpuType\x12\x12\n\ngpu_amount\x18\x04 \x01(\x05\x12\x10\n\x08instance\x18\x05 \x01(\t\"_\n\x04Step\x12\r\n\x05tests\x18\x01 \x01(\x08\x12\x1f\n\x17validate_build_artifact\x18\x02 \x01(\x08\x12\'\n\x1fvalidate_build_artifact_timeout\x18\x03 \x01(\x05\"\xdc\x01\n\x0b\x42uildFilter\x12\x0c\n\x04tags\x18\x01 \x03(\t\x12\x37\n\x0emetric_filters\x18\x02 \x03(\x0b\x32\x1f.com.qwak.build.v1.MetricFilter\x12=\n\x11parameter_filters\x18\x03 \x03(\x0b\x32\".com.qwak.build.v1.ParameterFilter\x12\x18\n\x10require_all_tags\x18\x04 \x01(\x08\x12\x1a\n\x12include_extra_tags\x18\x05 \x01(\x08\x12\x11\n\tbuild_ids\x18\x06 \x03(\t\"r\n\x0cMetricFilter\x12\x13\n\x0bmetric_name\x18\x01 \x01(\t\x12\x14\n\x0cmetric_value\x18\x02 \x01(\x02\x12\x37\n\x08operator\x18\x03 \x01(\x0e\x32%.com.qwak.build.v1.MetricOperatorType\"~\n\x0fParameterFilter\x12\x16\n\x0eparameter_name\x18\x01 \x01(\t\x12\x17\n\x0fparameter_value\x18\x02 \x01(\t\x12:\n\x08operator\x18\x03 \x01(\x0e\x32(.com.qwak.build.v1.ParameterOperatorType*\xe8\x01\n\x0b\x42uildStatus\x12\x0b\n\x07INVALID\x10\x00\x12\x0f\n\x0bIN_PROGRESS\x10\x01\x12\x0e\n\nSUCCESSFUL\x10\x02\x12\n\n\x06\x46\x41ILED\x10\x03\x12\x1d\n\x19REMOTE_BUILD_INITIALIZING\x10\x04\x12\x1a\n\x16REMOTE_BUILD_CANCELLED\x10\x05\x12\x1a\n\x16REMOTE_BUILD_TIMED_OUT\x10\x06\x12\x18\n\x14REMOTE_BUILD_UNKNOWN\x10\x07\x12\x18\n\x14SYNCING_ENVIRONMENTS\x10\x08\x12\x14\n\x10\x46INISHED_SYNCING\x10\t*\xa0\x02\n\x12MetricOperatorType\x12 \n\x1cMETRIC_OPERATOR_TYPE_INVALID\x10\x00\x12\x1f\n\x1bMETRIC_OPERATOR_TYPE_EQUALS\x10\x01\x12#\n\x1fMETRIC_OPERATOR_TYPE_NOT_EQUALS\x10\x02\x12\"\n\x1eMETRIC_OPERATOR_TYPE_LESS_THAN\x10\x03\x12)\n%METRIC_OPERATOR_TYPE_LESS_THAN_EQUALS\x10\x04\x12%\n!METRIC_OPERATOR_TYPE_GREATER_THAN\x10\x05\x12,\n(METRIC_OPERATOR_TYPE_GREATER_THAN_EQUALS\x10\x06*\x88\x01\n\x15ParameterOperatorType\x12#\n\x1fPARAMETER_OPERATOR_TYPE_INVALID\x10\x00\x12\"\n\x1ePARAMETER_OPERATOR_TYPE_EQUALS\x10\x01\x12&\n\"PARAMETER_OPERATOR_TYPE_NOT_EQUALS\x10\x02\x42!\n\x11\x63om.qwak.build.v1B\nBuildProtoP\x01\x62\x06proto3')

_BUILDSTATUS = DESCRIPTOR.enum_types_by_name['BuildStatus']
BuildStatus = enum_type_wrapper.EnumTypeWrapper(_BUILDSTATUS)
_METRICOPERATORTYPE = DESCRIPTOR.enum_types_by_name['MetricOperatorType']
MetricOperatorType = enum_type_wrapper.EnumTypeWrapper(_METRICOPERATORTYPE)
_PARAMETEROPERATORTYPE = DESCRIPTOR.enum_types_by_name['ParameterOperatorType']
ParameterOperatorType = enum_type_wrapper.EnumTypeWrapper(_PARAMETEROPERATORTYPE)
INVALID = 0
IN_PROGRESS = 1
SUCCESSFUL = 2
FAILED = 3
REMOTE_BUILD_INITIALIZING = 4
REMOTE_BUILD_CANCELLED = 5
REMOTE_BUILD_TIMED_OUT = 6
REMOTE_BUILD_UNKNOWN = 7
SYNCING_ENVIRONMENTS = 8
FINISHED_SYNCING = 9
METRIC_OPERATOR_TYPE_INVALID = 0
METRIC_OPERATOR_TYPE_EQUALS = 1
METRIC_OPERATOR_TYPE_NOT_EQUALS = 2
METRIC_OPERATOR_TYPE_LESS_THAN = 3
METRIC_OPERATOR_TYPE_LESS_THAN_EQUALS = 4
METRIC_OPERATOR_TYPE_GREATER_THAN = 5
METRIC_OPERATOR_TYPE_GREATER_THAN_EQUALS = 6
PARAMETER_OPERATOR_TYPE_INVALID = 0
PARAMETER_OPERATOR_TYPE_EQUALS = 1
PARAMETER_OPERATOR_TYPE_NOT_EQUALS = 2


_MODELSCHEMA = DESCRIPTOR.message_types_by_name['ModelSchema']
_ENTITY = DESCRIPTOR.message_types_by_name['Entity']
_FEATURE = DESCRIPTOR.message_types_by_name['Feature']
_ONTHEFLYFEATURE = DESCRIPTOR.message_types_by_name['OnTheFlyFeature']
_BATCHFEATUREV1 = DESCRIPTOR.message_types_by_name['BatchFeatureV1']
_STREAMINGFEATUREV1 = DESCRIPTOR.message_types_by_name['StreamingFeatureV1']
_BATCHFEATURE = DESCRIPTOR.message_types_by_name['BatchFeature']
_STREAMINGFEATURE = DESCRIPTOR.message_types_by_name['StreamingFeature']
_STREAMINGAGGREGATIONFEATURE = DESCRIPTOR.message_types_by_name['StreamingAggregationFeature']
_EXPLICITFEATURE = DESCRIPTOR.message_types_by_name['ExplicitFeature']
_REQUESTINPUT = DESCRIPTOR.message_types_by_name['RequestInput']
_SOURCEFEATURE = DESCRIPTOR.message_types_by_name['SourceFeature']
_PREDICTION = DESCRIPTOR.message_types_by_name['Prediction']
_INFERENCEOUTPUT = DESCRIPTOR.message_types_by_name['InferenceOutput']
_VALUETYPE = DESCRIPTOR.message_types_by_name['ValueType']
_PARAMETERCATEGORY = DESCRIPTOR.message_types_by_name['ParameterCategory']
_BUILD = DESCRIPTOR.message_types_by_name['Build']
_BUILD_PARAMSENTRY = _BUILD.nested_types_by_name['ParamsEntry']
_BUILD_METRICSENTRY = _BUILD.nested_types_by_name['MetricsEntry']
_AUDIT = DESCRIPTOR.message_types_by_name['Audit']
_BUILDCONFIGURATION = DESCRIPTOR.message_types_by_name['BuildConfiguration']
_BUILDPROPERTIES = DESCRIPTOR.message_types_by_name['BuildProperties']
_BUILDMODELURI = DESCRIPTOR.message_types_by_name['BuildModelUri']
_BUILDENVIRONMENT = DESCRIPTOR.message_types_by_name['BuildEnvironment']
_DOCKERBUILD = DESCRIPTOR.message_types_by_name['DockerBuild']
_DOCKERBUILD_BUILDARGSENTRY = _DOCKERBUILD.nested_types_by_name['BuildArgsEntry']
_LOCALBUILD = DESCRIPTOR.message_types_by_name['LocalBuild']
_PYTHONBUILD = DESCRIPTOR.message_types_by_name['PythonBuild']
_CONDABUILD = DESCRIPTOR.message_types_by_name['CondaBuild']
_POETRYBUILD = DESCRIPTOR.message_types_by_name['PoetryBuild']
_VIRTUALENVIRONMENTBUILD = DESCRIPTOR.message_types_by_name['VirtualEnvironmentBuild']
_REMOTEBUILD = DESCRIPTOR.message_types_by_name['RemoteBuild']
_REMOTEBUILDRESOURCES = DESCRIPTOR.message_types_by_name['RemoteBuildResources']
_STEP = DESCRIPTOR.message_types_by_name['Step']
_BUILDFILTER = DESCRIPTOR.message_types_by_name['BuildFilter']
_METRICFILTER = DESCRIPTOR.message_types_by_name['MetricFilter']
_PARAMETERFILTER = DESCRIPTOR.message_types_by_name['ParameterFilter']
_VALUETYPE_TYPES = _VALUETYPE.enum_types_by_name['Types']
_PARAMETERCATEGORY_CATEGORY = _PARAMETERCATEGORY.enum_types_by_name['Category']
ModelSchema = _reflection.GeneratedProtocolMessageType('ModelSchema', (_message.Message,), {
  'DESCRIPTOR' : _MODELSCHEMA,
  '__module__' : 'qwak.build.v1.build_pb2'
  # @@protoc_insertion_point(class_scope:com.qwak.build.v1.ModelSchema)
  })
_sym_db.RegisterMessage(ModelSchema)

Entity = _reflection.GeneratedProtocolMessageType('Entity', (_message.Message,), {
  'DESCRIPTOR' : _ENTITY,
  '__module__' : 'qwak.build.v1.build_pb2'
  # @@protoc_insertion_point(class_scope:com.qwak.build.v1.Entity)
  })
_sym_db.RegisterMessage(Entity)

Feature = _reflection.GeneratedProtocolMessageType('Feature', (_message.Message,), {
  'DESCRIPTOR' : _FEATURE,
  '__module__' : 'qwak.build.v1.build_pb2'
  # @@protoc_insertion_point(class_scope:com.qwak.build.v1.Feature)
  })
_sym_db.RegisterMessage(Feature)

OnTheFlyFeature = _reflection.GeneratedProtocolMessageType('OnTheFlyFeature', (_message.Message,), {
  'DESCRIPTOR' : _ONTHEFLYFEATURE,
  '__module__' : 'qwak.build.v1.build_pb2'
  # @@protoc_insertion_point(class_scope:com.qwak.build.v1.OnTheFlyFeature)
  })
_sym_db.RegisterMessage(OnTheFlyFeature)

BatchFeatureV1 = _reflection.GeneratedProtocolMessageType('BatchFeatureV1', (_message.Message,), {
  'DESCRIPTOR' : _BATCHFEATUREV1,
  '__module__' : 'qwak.build.v1.build_pb2'
  # @@protoc_insertion_point(class_scope:com.qwak.build.v1.BatchFeatureV1)
  })
_sym_db.RegisterMessage(BatchFeatureV1)

StreamingFeatureV1 = _reflection.GeneratedProtocolMessageType('StreamingFeatureV1', (_message.Message,), {
  'DESCRIPTOR' : _STREAMINGFEATUREV1,
  '__module__' : 'qwak.build.v1.build_pb2'
  # @@protoc_insertion_point(class_scope:com.qwak.build.v1.StreamingFeatureV1)
  })
_sym_db.RegisterMessage(StreamingFeatureV1)

BatchFeature = _reflection.GeneratedProtocolMessageType('BatchFeature', (_message.Message,), {
  'DESCRIPTOR' : _BATCHFEATURE,
  '__module__' : 'qwak.build.v1.build_pb2'
  # @@protoc_insertion_point(class_scope:com.qwak.build.v1.BatchFeature)
  })
_sym_db.RegisterMessage(BatchFeature)

StreamingFeature = _reflection.GeneratedProtocolMessageType('StreamingFeature', (_message.Message,), {
  'DESCRIPTOR' : _STREAMINGFEATURE,
  '__module__' : 'qwak.build.v1.build_pb2'
  # @@protoc_insertion_point(class_scope:com.qwak.build.v1.StreamingFeature)
  })
_sym_db.RegisterMessage(StreamingFeature)

StreamingAggregationFeature = _reflection.GeneratedProtocolMessageType('StreamingAggregationFeature', (_message.Message,), {
  'DESCRIPTOR' : _STREAMINGAGGREGATIONFEATURE,
  '__module__' : 'qwak.build.v1.build_pb2'
  # @@protoc_insertion_point(class_scope:com.qwak.build.v1.StreamingAggregationFeature)
  })
_sym_db.RegisterMessage(StreamingAggregationFeature)

ExplicitFeature = _reflection.GeneratedProtocolMessageType('ExplicitFeature', (_message.Message,), {
  'DESCRIPTOR' : _EXPLICITFEATURE,
  '__module__' : 'qwak.build.v1.build_pb2'
  # @@protoc_insertion_point(class_scope:com.qwak.build.v1.ExplicitFeature)
  })
_sym_db.RegisterMessage(ExplicitFeature)

RequestInput = _reflection.GeneratedProtocolMessageType('RequestInput', (_message.Message,), {
  'DESCRIPTOR' : _REQUESTINPUT,
  '__module__' : 'qwak.build.v1.build_pb2'
  # @@protoc_insertion_point(class_scope:com.qwak.build.v1.RequestInput)
  })
_sym_db.RegisterMessage(RequestInput)

SourceFeature = _reflection.GeneratedProtocolMessageType('SourceFeature', (_message.Message,), {
  'DESCRIPTOR' : _SOURCEFEATURE,
  '__module__' : 'qwak.build.v1.build_pb2'
  # @@protoc_insertion_point(class_scope:com.qwak.build.v1.SourceFeature)
  })
_sym_db.RegisterMessage(SourceFeature)

Prediction = _reflection.GeneratedProtocolMessageType('Prediction', (_message.Message,), {
  'DESCRIPTOR' : _PREDICTION,
  '__module__' : 'qwak.build.v1.build_pb2'
  # @@protoc_insertion_point(class_scope:com.qwak.build.v1.Prediction)
  })
_sym_db.RegisterMessage(Prediction)

InferenceOutput = _reflection.GeneratedProtocolMessageType('InferenceOutput', (_message.Message,), {
  'DESCRIPTOR' : _INFERENCEOUTPUT,
  '__module__' : 'qwak.build.v1.build_pb2'
  # @@protoc_insertion_point(class_scope:com.qwak.build.v1.InferenceOutput)
  })
_sym_db.RegisterMessage(InferenceOutput)

ValueType = _reflection.GeneratedProtocolMessageType('ValueType', (_message.Message,), {
  'DESCRIPTOR' : _VALUETYPE,
  '__module__' : 'qwak.build.v1.build_pb2'
  # @@protoc_insertion_point(class_scope:com.qwak.build.v1.ValueType)
  })
_sym_db.RegisterMessage(ValueType)

ParameterCategory = _reflection.GeneratedProtocolMessageType('ParameterCategory', (_message.Message,), {
  'DESCRIPTOR' : _PARAMETERCATEGORY,
  '__module__' : 'qwak.build.v1.build_pb2'
  # @@protoc_insertion_point(class_scope:com.qwak.build.v1.ParameterCategory)
  })
_sym_db.RegisterMessage(ParameterCategory)

Build = _reflection.GeneratedProtocolMessageType('Build', (_message.Message,), {

  'ParamsEntry' : _reflection.GeneratedProtocolMessageType('ParamsEntry', (_message.Message,), {
    'DESCRIPTOR' : _BUILD_PARAMSENTRY,
    '__module__' : 'qwak.build.v1.build_pb2'
    # @@protoc_insertion_point(class_scope:com.qwak.build.v1.Build.ParamsEntry)
    })
  ,

  'MetricsEntry' : _reflection.GeneratedProtocolMessageType('MetricsEntry', (_message.Message,), {
    'DESCRIPTOR' : _BUILD_METRICSENTRY,
    '__module__' : 'qwak.build.v1.build_pb2'
    # @@protoc_insertion_point(class_scope:com.qwak.build.v1.Build.MetricsEntry)
    })
  ,
  'DESCRIPTOR' : _BUILD,
  '__module__' : 'qwak.build.v1.build_pb2'
  # @@protoc_insertion_point(class_scope:com.qwak.build.v1.Build)
  })
_sym_db.RegisterMessage(Build)
_sym_db.RegisterMessage(Build.ParamsEntry)
_sym_db.RegisterMessage(Build.MetricsEntry)

Audit = _reflection.GeneratedProtocolMessageType('Audit', (_message.Message,), {
  'DESCRIPTOR' : _AUDIT,
  '__module__' : 'qwak.build.v1.build_pb2'
  # @@protoc_insertion_point(class_scope:com.qwak.build.v1.Audit)
  })
_sym_db.RegisterMessage(Audit)

BuildConfiguration = _reflection.GeneratedProtocolMessageType('BuildConfiguration', (_message.Message,), {
  'DESCRIPTOR' : _BUILDCONFIGURATION,
  '__module__' : 'qwak.build.v1.build_pb2'
  # @@protoc_insertion_point(class_scope:com.qwak.build.v1.BuildConfiguration)
  })
_sym_db.RegisterMessage(BuildConfiguration)

BuildProperties = _reflection.GeneratedProtocolMessageType('BuildProperties', (_message.Message,), {
  'DESCRIPTOR' : _BUILDPROPERTIES,
  '__module__' : 'qwak.build.v1.build_pb2'
  # @@protoc_insertion_point(class_scope:com.qwak.build.v1.BuildProperties)
  })
_sym_db.RegisterMessage(BuildProperties)

BuildModelUri = _reflection.GeneratedProtocolMessageType('BuildModelUri', (_message.Message,), {
  'DESCRIPTOR' : _BUILDMODELURI,
  '__module__' : 'qwak.build.v1.build_pb2'
  # @@protoc_insertion_point(class_scope:com.qwak.build.v1.BuildModelUri)
  })
_sym_db.RegisterMessage(BuildModelUri)

BuildEnvironment = _reflection.GeneratedProtocolMessageType('BuildEnvironment', (_message.Message,), {
  'DESCRIPTOR' : _BUILDENVIRONMENT,
  '__module__' : 'qwak.build.v1.build_pb2'
  # @@protoc_insertion_point(class_scope:com.qwak.build.v1.BuildEnvironment)
  })
_sym_db.RegisterMessage(BuildEnvironment)

DockerBuild = _reflection.GeneratedProtocolMessageType('DockerBuild', (_message.Message,), {

  'BuildArgsEntry' : _reflection.GeneratedProtocolMessageType('BuildArgsEntry', (_message.Message,), {
    'DESCRIPTOR' : _DOCKERBUILD_BUILDARGSENTRY,
    '__module__' : 'qwak.build.v1.build_pb2'
    # @@protoc_insertion_point(class_scope:com.qwak.build.v1.DockerBuild.BuildArgsEntry)
    })
  ,
  'DESCRIPTOR' : _DOCKERBUILD,
  '__module__' : 'qwak.build.v1.build_pb2'
  # @@protoc_insertion_point(class_scope:com.qwak.build.v1.DockerBuild)
  })
_sym_db.RegisterMessage(DockerBuild)
_sym_db.RegisterMessage(DockerBuild.BuildArgsEntry)

LocalBuild = _reflection.GeneratedProtocolMessageType('LocalBuild', (_message.Message,), {
  'DESCRIPTOR' : _LOCALBUILD,
  '__module__' : 'qwak.build.v1.build_pb2'
  # @@protoc_insertion_point(class_scope:com.qwak.build.v1.LocalBuild)
  })
_sym_db.RegisterMessage(LocalBuild)

PythonBuild = _reflection.GeneratedProtocolMessageType('PythonBuild', (_message.Message,), {
  'DESCRIPTOR' : _PYTHONBUILD,
  '__module__' : 'qwak.build.v1.build_pb2'
  # @@protoc_insertion_point(class_scope:com.qwak.build.v1.PythonBuild)
  })
_sym_db.RegisterMessage(PythonBuild)

CondaBuild = _reflection.GeneratedProtocolMessageType('CondaBuild', (_message.Message,), {
  'DESCRIPTOR' : _CONDABUILD,
  '__module__' : 'qwak.build.v1.build_pb2'
  # @@protoc_insertion_point(class_scope:com.qwak.build.v1.CondaBuild)
  })
_sym_db.RegisterMessage(CondaBuild)

PoetryBuild = _reflection.GeneratedProtocolMessageType('PoetryBuild', (_message.Message,), {
  'DESCRIPTOR' : _POETRYBUILD,
  '__module__' : 'qwak.build.v1.build_pb2'
  # @@protoc_insertion_point(class_scope:com.qwak.build.v1.PoetryBuild)
  })
_sym_db.RegisterMessage(PoetryBuild)

VirtualEnvironmentBuild = _reflection.GeneratedProtocolMessageType('VirtualEnvironmentBuild', (_message.Message,), {
  'DESCRIPTOR' : _VIRTUALENVIRONMENTBUILD,
  '__module__' : 'qwak.build.v1.build_pb2'
  # @@protoc_insertion_point(class_scope:com.qwak.build.v1.VirtualEnvironmentBuild)
  })
_sym_db.RegisterMessage(VirtualEnvironmentBuild)

RemoteBuild = _reflection.GeneratedProtocolMessageType('RemoteBuild', (_message.Message,), {
  'DESCRIPTOR' : _REMOTEBUILD,
  '__module__' : 'qwak.build.v1.build_pb2'
  # @@protoc_insertion_point(class_scope:com.qwak.build.v1.RemoteBuild)
  })
_sym_db.RegisterMessage(RemoteBuild)

RemoteBuildResources = _reflection.GeneratedProtocolMessageType('RemoteBuildResources', (_message.Message,), {
  'DESCRIPTOR' : _REMOTEBUILDRESOURCES,
  '__module__' : 'qwak.build.v1.build_pb2'
  # @@protoc_insertion_point(class_scope:com.qwak.build.v1.RemoteBuildResources)
  })
_sym_db.RegisterMessage(RemoteBuildResources)

Step = _reflection.GeneratedProtocolMessageType('Step', (_message.Message,), {
  'DESCRIPTOR' : _STEP,
  '__module__' : 'qwak.build.v1.build_pb2'
  # @@protoc_insertion_point(class_scope:com.qwak.build.v1.Step)
  })
_sym_db.RegisterMessage(Step)

BuildFilter = _reflection.GeneratedProtocolMessageType('BuildFilter', (_message.Message,), {
  'DESCRIPTOR' : _BUILDFILTER,
  '__module__' : 'qwak.build.v1.build_pb2'
  # @@protoc_insertion_point(class_scope:com.qwak.build.v1.BuildFilter)
  })
_sym_db.RegisterMessage(BuildFilter)

MetricFilter = _reflection.GeneratedProtocolMessageType('MetricFilter', (_message.Message,), {
  'DESCRIPTOR' : _METRICFILTER,
  '__module__' : 'qwak.build.v1.build_pb2'
  # @@protoc_insertion_point(class_scope:com.qwak.build.v1.MetricFilter)
  })
_sym_db.RegisterMessage(MetricFilter)

ParameterFilter = _reflection.GeneratedProtocolMessageType('ParameterFilter', (_message.Message,), {
  'DESCRIPTOR' : _PARAMETERFILTER,
  '__module__' : 'qwak.build.v1.build_pb2'
  # @@protoc_insertion_point(class_scope:com.qwak.build.v1.ParameterFilter)
  })
_sym_db.RegisterMessage(ParameterFilter)

if _descriptor._USE_C_DESCRIPTORS == False:

  DESCRIPTOR._options = None
  DESCRIPTOR._serialized_options = b'\n\021com.qwak.build.v1B\nBuildProtoP\001'
  _BUILD_PARAMSENTRY._options = None
  _BUILD_PARAMSENTRY._serialized_options = b'8\001'
  _BUILD_METRICSENTRY._options = None
  _BUILD_METRICSENTRY._serialized_options = b'8\001'
  _DOCKERBUILD_BUILDARGSENTRY._options = None
  _DOCKERBUILD_BUILDARGSENTRY._serialized_options = b'8\001'
  _BUILDSTATUS._serialized_start=5407
  _BUILDSTATUS._serialized_end=5639
  _METRICOPERATORTYPE._serialized_start=5642
  _METRICOPERATORTYPE._serialized_end=5930
  _PARAMETEROPERATORTYPE._serialized_start=5933
  _PARAMETEROPERATORTYPE._serialized_end=6069
  _MODELSCHEMA._serialized_start=107
  _MODELSCHEMA._serialized_end=325
  _ENTITY._serialized_start=327
  _ENTITY._serialized_end=393
  _FEATURE._serialized_start=396
  _FEATURE._serialized_end=948
  _ONTHEFLYFEATURE._serialized_start=951
  _ONTHEFLYFEATURE._serialized_end=1084
  _BATCHFEATUREV1._serialized_start=1086
  _BATCHFEATUREV1._serialized_end=1159
  _STREAMINGFEATUREV1._serialized_start=1161
  _STREAMINGFEATUREV1._serialized_end=1238
  _BATCHFEATURE._serialized_start=1240
  _BATCHFEATURE._serialized_end=1311
  _STREAMINGFEATURE._serialized_start=1313
  _STREAMINGFEATURE._serialized_end=1388
  _STREAMINGAGGREGATIONFEATURE._serialized_start=1390
  _STREAMINGAGGREGATIONFEATURE._serialized_end=1476
  _EXPLICITFEATURE._serialized_start=1478
  _EXPLICITFEATURE._serialized_end=1553
  _REQUESTINPUT._serialized_start=1555
  _REQUESTINPUT._serialized_end=1627
  _SOURCEFEATURE._serialized_start=1630
  _SOURCEFEATURE._serialized_end=1775
  _PREDICTION._serialized_start=1777
  _PREDICTION._serialized_end=1847
  _INFERENCEOUTPUT._serialized_start=1849
  _INFERENCEOUTPUT._serialized_end=1924
  _VALUETYPE._serialized_start=1927
  _VALUETYPE._serialized_end=2088
  _VALUETYPE_TYPES._serialized_start=1990
  _VALUETYPE_TYPES._serialized_end=2088
  _PARAMETERCATEGORY._serialized_start=2090
  _PARAMETERCATEGORY._serialized_end=2196
  _PARAMETERCATEGORY_CATEGORY._serialized_start=2111
  _PARAMETERCATEGORY_CATEGORY._serialized_end=2196
  _BUILD._serialized_start=2199
  _BUILD._serialized_end=2904
  _BUILD_PARAMSENTRY._serialized_start=2811
  _BUILD_PARAMSENTRY._serialized_end=2856
  _BUILD_METRICSENTRY._serialized_start=2858
  _BUILD_METRICSENTRY._serialized_end=2904
  _AUDIT._serialized_start=2907
  _AUDIT._serialized_end=3062
  _BUILDCONFIGURATION._serialized_start=3065
  _BUILDCONFIGURATION._serialized_end=3372
  _BUILDPROPERTIES._serialized_start=3375
  _BUILDPROPERTIES._serialized_end=3561
  _BUILDMODELURI._serialized_start=3563
  _BUILDMODELURI._serialized_end=3629
  _BUILDENVIRONMENT._serialized_start=3632
  _BUILDENVIRONMENT._serialized_end=3844
  _DOCKERBUILD._serialized_start=3847
  _DOCKERBUILD._serialized_end=4108
  _DOCKERBUILD_BUILDARGSENTRY._serialized_start=4060
  _DOCKERBUILD_BUILDARGSENTRY._serialized_end=4108
  _LOCALBUILD._serialized_start=4110
  _LOCALBUILD._serialized_end=4160
  _PYTHONBUILD._serialized_start=4163
  _PYTHONBUILD._serialized_end=4431
  _CONDABUILD._serialized_start=4433
  _CONDABUILD._serialized_end=4465
  _POETRYBUILD._serialized_start=4467
  _POETRYBUILD._serialized_end=4523
  _VIRTUALENVIRONMENTBUILD._serialized_start=4525
  _VIRTUALENVIRONMENTBUILD._serialized_end=4600
  _REMOTEBUILD._serialized_start=4602
  _REMOTEBUILD._serialized_end=4694
  _REMOTEBUILDRESOURCES._serialized_start=4697
  _REMOTEBUILDRESOURCES._serialized_end=4840
  _STEP._serialized_start=4842
  _STEP._serialized_end=4937
  _BUILDFILTER._serialized_start=4940
  _BUILDFILTER._serialized_end=5160
  _METRICFILTER._serialized_start=5162
  _METRICFILTER._serialized_end=5276
  _PARAMETERFILTER._serialized_start=5278
  _PARAMETERFILTER._serialized_end=5404
# @@protoc_insertion_point(module_scope)
