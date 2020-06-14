# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: object_detection/protos/eval.proto

from google.protobuf import (
	descriptor as _descriptor,
	message as _message,
	reflection as _reflection,
	symbol_database as _symbol_database,
)

# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()

DESCRIPTOR = _descriptor.FileDescriptor(
	name='object_detection/protos/eval.proto',
	package='object_detection.protos',
	syntax='proto2',
	serialized_options=None,
	create_key=_descriptor._internal_create_key,
	serialized_pb=
	b'\n\"object_detection/protos/eval.proto\x12\x17object_detection.protos\"\xc0\x08\n\nEvalConfig\x12\x15\n\nbatch_size\x18\x19 \x01(\r:\x01\x31\x12\x1e\n\x12num_visualizations\x18\x01 \x01(\r:\x02\x31\x30\x12\x1e\n\x0cnum_examples\x18\x02 \x01(\r:\x04\x35\x30\x30\x30\x42\x02\x18\x01\x12\x1f\n\x12\x65val_interval_secs\x18\x03 \x01(\r:\x03\x33\x30\x30\x12\x18\n\tmax_evals\x18\x04 \x01(\r:\x01\x30\x42\x02\x18\x01\x12\x19\n\nsave_graph\x18\x05 \x01(\x08:\x05\x66\x61lse\x12\"\n\x18visualization_export_dir\x18\x06 \x01(\t:\x00\x12\x15\n\x0b\x65val_master\x18\x07 \x01(\t:\x00\x12\x13\n\x0bmetrics_set\x18\x08 \x03(\t\x12J\n\x14parameterized_metric\x18\x1f \x03(\x0b\x32,.object_detection.protos.ParameterizedMetric\x12\x15\n\x0b\x65xport_path\x18\t \x01(\t:\x00\x12!\n\x12ignore_groundtruth\x18\n \x01(\x08:\x05\x66\x61lse\x12\"\n\x13use_moving_averages\x18\x0b \x01(\x08:\x05\x66\x61lse\x12\"\n\x13\x65val_instance_masks\x18\x0c \x01(\x08:\x05\x66\x61lse\x12 \n\x13min_score_threshold\x18\r \x01(\x02:\x03\x30.5\x12&\n\x1amax_num_boxes_to_visualize\x18\x0e \x01(\x05:\x02\x32\x30\x12\x1a\n\x0bskip_scores\x18\x0f \x01(\x08:\x05\x66\x61lse\x12\x1a\n\x0bskip_labels\x18\x10 \x01(\x08:\x05\x66\x61lse\x12*\n\x1bvisualize_groundtruth_boxes\x18\x11 \x01(\x08:\x05\x66\x61lse\x12\x32\n#groundtruth_box_visualization_color\x18\x12 \x01(\t:\x05\x62lack\x12\x35\n&keep_image_id_for_visualization_export\x18\x13 \x01(\x08:\x05\x66\x61lse\x12$\n\x16retain_original_images\x18\x17 \x01(\x08:\x04true\x12+\n\x1cinclude_metrics_per_category\x18\x18 \x01(\x08:\x05\x66\x61lse\x12\x1d\n\x12recall_lower_bound\x18\x1a \x01(\x02:\x01\x30\x12\x1d\n\x12recall_upper_bound\x18\x1b \x01(\x02:\x01\x31\x12\x38\n)retain_original_image_additional_channels\x18\x1c \x01(\x08:\x05\x66\x61lse\x12\x1e\n\x0f\x66orce_no_resize\x18\x1d \x01(\x08:\x05\x66\x61lse\x12%\n\x16use_dummy_loss_in_eval\x18\x1e \x01(\x08:\x05\x66\x61lse\x12<\n\rkeypoint_edge\x18  \x03(\x0b\x32%.object_detection.protos.KeypointEdge\"|\n\x13ParameterizedMetric\x12M\n\x15\x63oco_keypoint_metrics\x18\x01 \x01(\x0b\x32,.object_detection.protos.CocoKeypointMetricsH\x00\x42\x16\n\x14parameterized_metric\"\xd3\x01\n\x13\x43ocoKeypointMetrics\x12\x13\n\x0b\x63lass_label\x18\x01 \x01(\t\x12i\n\x18keypoint_label_to_sigmas\x18\x02 \x03(\x0b\x32G.object_detection.protos.CocoKeypointMetrics.KeypointLabelToSigmasEntry\x1a<\n\x1aKeypointLabelToSigmasEntry\x12\x0b\n\x03key\x18\x01 \x01(\t\x12\r\n\x05value\x18\x02 \x01(\x02:\x02\x38\x01\"*\n\x0cKeypointEdge\x12\r\n\x05start\x18\x01 \x01(\x05\x12\x0b\n\x03\x65nd\x18\x02 \x01(\x05'
)

_EVALCONFIG = _descriptor.Descriptor(
	name='EvalConfig',
	full_name='object_detection.protos.EvalConfig',
	filename=None,
	file=DESCRIPTOR,
	containing_type=None,
	create_key=_descriptor._internal_create_key,
	fields=[
	_descriptor.FieldDescriptor(
	name='batch_size',
	full_name='object_detection.protos.EvalConfig.batch_size',
	index=0,
	number=25,
	type=13,
	cpp_type=3,
	label=1,
	has_default_value=True,
	default_value=1,
	message_type=None,
	enum_type=None,
	containing_type=None,
	is_extension=False,
	extension_scope=None,
	serialized_options=None,
	file=DESCRIPTOR,
	create_key=_descriptor._internal_create_key
	),
	_descriptor.FieldDescriptor(
	name='num_visualizations',
	full_name='object_detection.protos.EvalConfig.num_visualizations',
	index=1,
	number=1,
	type=13,
	cpp_type=3,
	label=1,
	has_default_value=True,
	default_value=10,
	message_type=None,
	enum_type=None,
	containing_type=None,
	is_extension=False,
	extension_scope=None,
	serialized_options=None,
	file=DESCRIPTOR,
	create_key=_descriptor._internal_create_key
	),
	_descriptor.FieldDescriptor(
	name='num_examples',
	full_name='object_detection.protos.EvalConfig.num_examples',
	index=2,
	number=2,
	type=13,
	cpp_type=3,
	label=1,
	has_default_value=True,
	default_value=5000,
	message_type=None,
	enum_type=None,
	containing_type=None,
	is_extension=False,
	extension_scope=None,
	serialized_options=b'\030\001',
	file=DESCRIPTOR,
	create_key=_descriptor._internal_create_key
	),
	_descriptor.FieldDescriptor(
	name='eval_interval_secs',
	full_name='object_detection.protos.EvalConfig.eval_interval_secs',
	index=3,
	number=3,
	type=13,
	cpp_type=3,
	label=1,
	has_default_value=True,
	default_value=300,
	message_type=None,
	enum_type=None,
	containing_type=None,
	is_extension=False,
	extension_scope=None,
	serialized_options=None,
	file=DESCRIPTOR,
	create_key=_descriptor._internal_create_key
	),
	_descriptor.FieldDescriptor(
	name='max_evals',
	full_name='object_detection.protos.EvalConfig.max_evals',
	index=4,
	number=4,
	type=13,
	cpp_type=3,
	label=1,
	has_default_value=True,
	default_value=0,
	message_type=None,
	enum_type=None,
	containing_type=None,
	is_extension=False,
	extension_scope=None,
	serialized_options=b'\030\001',
	file=DESCRIPTOR,
	create_key=_descriptor._internal_create_key
	),
	_descriptor.FieldDescriptor(
	name='save_graph',
	full_name='object_detection.protos.EvalConfig.save_graph',
	index=5,
	number=5,
	type=8,
	cpp_type=7,
	label=1,
	has_default_value=True,
	default_value=False,
	message_type=None,
	enum_type=None,
	containing_type=None,
	is_extension=False,
	extension_scope=None,
	serialized_options=None,
	file=DESCRIPTOR,
	create_key=_descriptor._internal_create_key
	),
	_descriptor.FieldDescriptor(
	name='visualization_export_dir',
	full_name='object_detection.protos.EvalConfig.visualization_export_dir',
	index=6,
	number=6,
	type=9,
	cpp_type=9,
	label=1,
	has_default_value=True,
	default_value=b"".decode('utf-8'),
	message_type=None,
	enum_type=None,
	containing_type=None,
	is_extension=False,
	extension_scope=None,
	serialized_options=None,
	file=DESCRIPTOR,
	create_key=_descriptor._internal_create_key
	),
	_descriptor.FieldDescriptor(
	name='eval_master',
	full_name='object_detection.protos.EvalConfig.eval_master',
	index=7,
	number=7,
	type=9,
	cpp_type=9,
	label=1,
	has_default_value=True,
	default_value=b"".decode('utf-8'),
	message_type=None,
	enum_type=None,
	containing_type=None,
	is_extension=False,
	extension_scope=None,
	serialized_options=None,
	file=DESCRIPTOR,
	create_key=_descriptor._internal_create_key
	),
	_descriptor.FieldDescriptor(
	name='metrics_set',
	full_name='object_detection.protos.EvalConfig.metrics_set',
	index=8,
	number=8,
	type=9,
	cpp_type=9,
	label=3,
	has_default_value=False,
	default_value=[],
	message_type=None,
	enum_type=None,
	containing_type=None,
	is_extension=False,
	extension_scope=None,
	serialized_options=None,
	file=DESCRIPTOR,
	create_key=_descriptor._internal_create_key
	),
	_descriptor.FieldDescriptor(
	name='parameterized_metric',
	full_name='object_detection.protos.EvalConfig.parameterized_metric',
	index=9,
	number=31,
	type=11,
	cpp_type=10,
	label=3,
	has_default_value=False,
	default_value=[],
	message_type=None,
	enum_type=None,
	containing_type=None,
	is_extension=False,
	extension_scope=None,
	serialized_options=None,
	file=DESCRIPTOR,
	create_key=_descriptor._internal_create_key
	),
	_descriptor.FieldDescriptor(
	name='export_path',
	full_name='object_detection.protos.EvalConfig.export_path',
	index=10,
	number=9,
	type=9,
	cpp_type=9,
	label=1,
	has_default_value=True,
	default_value=b"".decode('utf-8'),
	message_type=None,
	enum_type=None,
	containing_type=None,
	is_extension=False,
	extension_scope=None,
	serialized_options=None,
	file=DESCRIPTOR,
	create_key=_descriptor._internal_create_key
	),
	_descriptor.FieldDescriptor(
	name='ignore_groundtruth',
	full_name='object_detection.protos.EvalConfig.ignore_groundtruth',
	index=11,
	number=10,
	type=8,
	cpp_type=7,
	label=1,
	has_default_value=True,
	default_value=False,
	message_type=None,
	enum_type=None,
	containing_type=None,
	is_extension=False,
	extension_scope=None,
	serialized_options=None,
	file=DESCRIPTOR,
	create_key=_descriptor._internal_create_key
	),
	_descriptor.FieldDescriptor(
	name='use_moving_averages',
	full_name='object_detection.protos.EvalConfig.use_moving_averages',
	index=12,
	number=11,
	type=8,
	cpp_type=7,
	label=1,
	has_default_value=True,
	default_value=False,
	message_type=None,
	enum_type=None,
	containing_type=None,
	is_extension=False,
	extension_scope=None,
	serialized_options=None,
	file=DESCRIPTOR,
	create_key=_descriptor._internal_create_key
	),
	_descriptor.FieldDescriptor(
	name='eval_instance_masks',
	full_name='object_detection.protos.EvalConfig.eval_instance_masks',
	index=13,
	number=12,
	type=8,
	cpp_type=7,
	label=1,
	has_default_value=True,
	default_value=False,
	message_type=None,
	enum_type=None,
	containing_type=None,
	is_extension=False,
	extension_scope=None,
	serialized_options=None,
	file=DESCRIPTOR,
	create_key=_descriptor._internal_create_key
	),
	_descriptor.FieldDescriptor(
	name='min_score_threshold',
	full_name='object_detection.protos.EvalConfig.min_score_threshold',
	index=14,
	number=13,
	type=2,
	cpp_type=6,
	label=1,
	has_default_value=True,
	default_value=float(0.5),
	message_type=None,
	enum_type=None,
	containing_type=None,
	is_extension=False,
	extension_scope=None,
	serialized_options=None,
	file=DESCRIPTOR,
	create_key=_descriptor._internal_create_key
	),
	_descriptor.FieldDescriptor(
	name='max_num_boxes_to_visualize',
	full_name='object_detection.protos.EvalConfig.max_num_boxes_to_visualize',
	index=15,
	number=14,
	type=5,
	cpp_type=1,
	label=1,
	has_default_value=True,
	default_value=20,
	message_type=None,
	enum_type=None,
	containing_type=None,
	is_extension=False,
	extension_scope=None,
	serialized_options=None,
	file=DESCRIPTOR,
	create_key=_descriptor._internal_create_key
	),
	_descriptor.FieldDescriptor(
	name='skip_scores',
	full_name='object_detection.protos.EvalConfig.skip_scores',
	index=16,
	number=15,
	type=8,
	cpp_type=7,
	label=1,
	has_default_value=True,
	default_value=False,
	message_type=None,
	enum_type=None,
	containing_type=None,
	is_extension=False,
	extension_scope=None,
	serialized_options=None,
	file=DESCRIPTOR,
	create_key=_descriptor._internal_create_key
	),
	_descriptor.FieldDescriptor(
	name='skip_labels',
	full_name='object_detection.protos.EvalConfig.skip_labels',
	index=17,
	number=16,
	type=8,
	cpp_type=7,
	label=1,
	has_default_value=True,
	default_value=False,
	message_type=None,
	enum_type=None,
	containing_type=None,
	is_extension=False,
	extension_scope=None,
	serialized_options=None,
	file=DESCRIPTOR,
	create_key=_descriptor._internal_create_key
	),
	_descriptor.FieldDescriptor(
	name='visualize_groundtruth_boxes',
	full_name='object_detection.protos.EvalConfig.visualize_groundtruth_boxes',
	index=18,
	number=17,
	type=8,
	cpp_type=7,
	label=1,
	has_default_value=True,
	default_value=False,
	message_type=None,
	enum_type=None,
	containing_type=None,
	is_extension=False,
	extension_scope=None,
	serialized_options=None,
	file=DESCRIPTOR,
	create_key=_descriptor._internal_create_key
	),
	_descriptor.FieldDescriptor(
	name='groundtruth_box_visualization_color',
	full_name='object_detection.protos.EvalConfig.groundtruth_box_visualization_color',
	index=19,
	number=18,
	type=9,
	cpp_type=9,
	label=1,
	has_default_value=True,
	default_value=b"black".decode('utf-8'),
	message_type=None,
	enum_type=None,
	containing_type=None,
	is_extension=False,
	extension_scope=None,
	serialized_options=None,
	file=DESCRIPTOR,
	create_key=_descriptor._internal_create_key
	),
	_descriptor.FieldDescriptor(
	name='keep_image_id_for_visualization_export',
	full_name='object_detection.protos.EvalConfig.keep_image_id_for_visualization_export',
	index=20,
	number=19,
	type=8,
	cpp_type=7,
	label=1,
	has_default_value=True,
	default_value=False,
	message_type=None,
	enum_type=None,
	containing_type=None,
	is_extension=False,
	extension_scope=None,
	serialized_options=None,
	file=DESCRIPTOR,
	create_key=_descriptor._internal_create_key
	),
	_descriptor.FieldDescriptor(
	name='retain_original_images',
	full_name='object_detection.protos.EvalConfig.retain_original_images',
	index=21,
	number=23,
	type=8,
	cpp_type=7,
	label=1,
	has_default_value=True,
	default_value=True,
	message_type=None,
	enum_type=None,
	containing_type=None,
	is_extension=False,
	extension_scope=None,
	serialized_options=None,
	file=DESCRIPTOR,
	create_key=_descriptor._internal_create_key
	),
	_descriptor.FieldDescriptor(
	name='include_metrics_per_category',
	full_name='object_detection.protos.EvalConfig.include_metrics_per_category',
	index=22,
	number=24,
	type=8,
	cpp_type=7,
	label=1,
	has_default_value=True,
	default_value=False,
	message_type=None,
	enum_type=None,
	containing_type=None,
	is_extension=False,
	extension_scope=None,
	serialized_options=None,
	file=DESCRIPTOR,
	create_key=_descriptor._internal_create_key
	),
	_descriptor.FieldDescriptor(
	name='recall_lower_bound',
	full_name='object_detection.protos.EvalConfig.recall_lower_bound',
	index=23,
	number=26,
	type=2,
	cpp_type=6,
	label=1,
	has_default_value=True,
	default_value=float(0),
	message_type=None,
	enum_type=None,
	containing_type=None,
	is_extension=False,
	extension_scope=None,
	serialized_options=None,
	file=DESCRIPTOR,
	create_key=_descriptor._internal_create_key
	),
	_descriptor.FieldDescriptor(
	name='recall_upper_bound',
	full_name='object_detection.protos.EvalConfig.recall_upper_bound',
	index=24,
	number=27,
	type=2,
	cpp_type=6,
	label=1,
	has_default_value=True,
	default_value=float(1),
	message_type=None,
	enum_type=None,
	containing_type=None,
	is_extension=False,
	extension_scope=None,
	serialized_options=None,
	file=DESCRIPTOR,
	create_key=_descriptor._internal_create_key
	),
	_descriptor.FieldDescriptor(
	name='retain_original_image_additional_channels',
	full_name='object_detection.protos.EvalConfig.retain_original_image_additional_channels',
	index=25,
	number=28,
	type=8,
	cpp_type=7,
	label=1,
	has_default_value=True,
	default_value=False,
	message_type=None,
	enum_type=None,
	containing_type=None,
	is_extension=False,
	extension_scope=None,
	serialized_options=None,
	file=DESCRIPTOR,
	create_key=_descriptor._internal_create_key
	),
	_descriptor.FieldDescriptor(
	name='force_no_resize',
	full_name='object_detection.protos.EvalConfig.force_no_resize',
	index=26,
	number=29,
	type=8,
	cpp_type=7,
	label=1,
	has_default_value=True,
	default_value=False,
	message_type=None,
	enum_type=None,
	containing_type=None,
	is_extension=False,
	extension_scope=None,
	serialized_options=None,
	file=DESCRIPTOR,
	create_key=_descriptor._internal_create_key
	),
	_descriptor.FieldDescriptor(
	name='use_dummy_loss_in_eval',
	full_name='object_detection.protos.EvalConfig.use_dummy_loss_in_eval',
	index=27,
	number=30,
	type=8,
	cpp_type=7,
	label=1,
	has_default_value=True,
	default_value=False,
	message_type=None,
	enum_type=None,
	containing_type=None,
	is_extension=False,
	extension_scope=None,
	serialized_options=None,
	file=DESCRIPTOR,
	create_key=_descriptor._internal_create_key
	),
	_descriptor.FieldDescriptor(
	name='keypoint_edge',
	full_name='object_detection.protos.EvalConfig.keypoint_edge',
	index=28,
	number=32,
	type=11,
	cpp_type=10,
	label=3,
	has_default_value=False,
	default_value=[],
	message_type=None,
	enum_type=None,
	containing_type=None,
	is_extension=False,
	extension_scope=None,
	serialized_options=None,
	file=DESCRIPTOR,
	create_key=_descriptor._internal_create_key
	),
	],
	extensions=[],
	nested_types=[],
	enum_types=[],
	serialized_options=None,
	is_extendable=False,
	syntax='proto2',
	extension_ranges=[],
	oneofs=[],
	serialized_start=64,
	serialized_end=1152,
)

_PARAMETERIZEDMETRIC = _descriptor.Descriptor(
	name='ParameterizedMetric',
	full_name='object_detection.protos.ParameterizedMetric',
	filename=None,
	file=DESCRIPTOR,
	containing_type=None,
	create_key=_descriptor._internal_create_key,
	fields=[
	_descriptor.FieldDescriptor(
	name='coco_keypoint_metrics',
	full_name='object_detection.protos.ParameterizedMetric.coco_keypoint_metrics',
	index=0,
	number=1,
	type=11,
	cpp_type=10,
	label=1,
	has_default_value=False,
	default_value=None,
	message_type=None,
	enum_type=None,
	containing_type=None,
	is_extension=False,
	extension_scope=None,
	serialized_options=None,
	file=DESCRIPTOR,
	create_key=_descriptor._internal_create_key
	),
	],
	extensions=[],
	nested_types=[],
	enum_types=[],
	serialized_options=None,
	is_extendable=False,
	syntax='proto2',
	extension_ranges=[],
	oneofs=[
	_descriptor.OneofDescriptor(
	name='parameterized_metric',
	full_name='object_detection.protos.ParameterizedMetric.parameterized_metric',
	index=0,
	containing_type=None,
	create_key=_descriptor._internal_create_key,
	fields=[]
	),
	],
	serialized_start=1154,
	serialized_end=1278,
)

_COCOKEYPOINTMETRICS_KEYPOINTLABELTOSIGMASENTRY = _descriptor.Descriptor(
	name='KeypointLabelToSigmasEntry',
	full_name='object_detection.protos.CocoKeypointMetrics.KeypointLabelToSigmasEntry',
	filename=None,
	file=DESCRIPTOR,
	containing_type=None,
	create_key=_descriptor._internal_create_key,
	fields=[
	_descriptor.FieldDescriptor(
	name='key',
	full_name='object_detection.protos.CocoKeypointMetrics.KeypointLabelToSigmasEntry.key',
	index=0,
	number=1,
	type=9,
	cpp_type=9,
	label=1,
	has_default_value=False,
	default_value=b"".decode('utf-8'),
	message_type=None,
	enum_type=None,
	containing_type=None,
	is_extension=False,
	extension_scope=None,
	serialized_options=None,
	file=DESCRIPTOR,
	create_key=_descriptor._internal_create_key
	),
	_descriptor.FieldDescriptor(
	name='value',
	full_name='object_detection.protos.CocoKeypointMetrics.KeypointLabelToSigmasEntry.value',
	index=1,
	number=2,
	type=2,
	cpp_type=6,
	label=1,
	has_default_value=False,
	default_value=float(0),
	message_type=None,
	enum_type=None,
	containing_type=None,
	is_extension=False,
	extension_scope=None,
	serialized_options=None,
	file=DESCRIPTOR,
	create_key=_descriptor._internal_create_key
	),
	],
	extensions=[],
	nested_types=[],
	enum_types=[],
	serialized_options=b'8\001',
	is_extendable=False,
	syntax='proto2',
	extension_ranges=[],
	oneofs=[],
	serialized_start=1432,
	serialized_end=1492,
)

_COCOKEYPOINTMETRICS = _descriptor.Descriptor(
	name='CocoKeypointMetrics',
	full_name='object_detection.protos.CocoKeypointMetrics',
	filename=None,
	file=DESCRIPTOR,
	containing_type=None,
	create_key=_descriptor._internal_create_key,
	fields=[
	_descriptor.FieldDescriptor(
	name='class_label',
	full_name='object_detection.protos.CocoKeypointMetrics.class_label',
	index=0,
	number=1,
	type=9,
	cpp_type=9,
	label=1,
	has_default_value=False,
	default_value=b"".decode('utf-8'),
	message_type=None,
	enum_type=None,
	containing_type=None,
	is_extension=False,
	extension_scope=None,
	serialized_options=None,
	file=DESCRIPTOR,
	create_key=_descriptor._internal_create_key
	),
	_descriptor.FieldDescriptor(
	name='keypoint_label_to_sigmas',
	full_name='object_detection.protos.CocoKeypointMetrics.keypoint_label_to_sigmas',
	index=1,
	number=2,
	type=11,
	cpp_type=10,
	label=3,
	has_default_value=False,
	default_value=[],
	message_type=None,
	enum_type=None,
	containing_type=None,
	is_extension=False,
	extension_scope=None,
	serialized_options=None,
	file=DESCRIPTOR,
	create_key=_descriptor._internal_create_key
	),
	],
	extensions=[],
	nested_types=[_COCOKEYPOINTMETRICS_KEYPOINTLABELTOSIGMASENTRY, ],
	enum_types=[],
	serialized_options=None,
	is_extendable=False,
	syntax='proto2',
	extension_ranges=[],
	oneofs=[],
	serialized_start=1281,
	serialized_end=1492,
)

_KEYPOINTEDGE = _descriptor.Descriptor(
	name='KeypointEdge',
	full_name='object_detection.protos.KeypointEdge',
	filename=None,
	file=DESCRIPTOR,
	containing_type=None,
	create_key=_descriptor._internal_create_key,
	fields=[
	_descriptor.FieldDescriptor(
	name='start',
	full_name='object_detection.protos.KeypointEdge.start',
	index=0,
	number=1,
	type=5,
	cpp_type=1,
	label=1,
	has_default_value=False,
	default_value=0,
	message_type=None,
	enum_type=None,
	containing_type=None,
	is_extension=False,
	extension_scope=None,
	serialized_options=None,
	file=DESCRIPTOR,
	create_key=_descriptor._internal_create_key
	),
	_descriptor.FieldDescriptor(
	name='end',
	full_name='object_detection.protos.KeypointEdge.end',
	index=1,
	number=2,
	type=5,
	cpp_type=1,
	label=1,
	has_default_value=False,
	default_value=0,
	message_type=None,
	enum_type=None,
	containing_type=None,
	is_extension=False,
	extension_scope=None,
	serialized_options=None,
	file=DESCRIPTOR,
	create_key=_descriptor._internal_create_key
	),
	],
	extensions=[],
	nested_types=[],
	enum_types=[],
	serialized_options=None,
	is_extendable=False,
	syntax='proto2',
	extension_ranges=[],
	oneofs=[],
	serialized_start=1494,
	serialized_end=1536,
)

_EVALCONFIG.fields_by_name['parameterized_metric'].message_type = _PARAMETERIZEDMETRIC
_EVALCONFIG.fields_by_name['keypoint_edge'].message_type = _KEYPOINTEDGE
_PARAMETERIZEDMETRIC.fields_by_name['coco_keypoint_metrics'].message_type = _COCOKEYPOINTMETRICS
_PARAMETERIZEDMETRIC.oneofs_by_name['parameterized_metric'].fields.append(
	_PARAMETERIZEDMETRIC.fields_by_name['coco_keypoint_metrics']
)
_PARAMETERIZEDMETRIC.fields_by_name['coco_keypoint_metrics'
									].containing_oneof = _PARAMETERIZEDMETRIC.oneofs_by_name[
	'parameterized_metric']
_COCOKEYPOINTMETRICS_KEYPOINTLABELTOSIGMASENTRY.containing_type = _COCOKEYPOINTMETRICS
_COCOKEYPOINTMETRICS.fields_by_name['keypoint_label_to_sigmas'
									].message_type = _COCOKEYPOINTMETRICS_KEYPOINTLABELTOSIGMASENTRY
DESCRIPTOR.message_types_by_name['EvalConfig'] = _EVALCONFIG
DESCRIPTOR.message_types_by_name['ParameterizedMetric'] = _PARAMETERIZEDMETRIC
DESCRIPTOR.message_types_by_name['CocoKeypointMetrics'] = _COCOKEYPOINTMETRICS
DESCRIPTOR.message_types_by_name['KeypointEdge'] = _KEYPOINTEDGE
_sym_db.RegisterFileDescriptor(DESCRIPTOR)

EvalConfig = _reflection.GeneratedProtocolMessageType(
	'EvalConfig', (_message.Message, ),
	{
	'DESCRIPTOR': _EVALCONFIG,
	'__module__': 'object_detection.protos.eval_pb2'
	# @@protoc_insertion_point(class_scope:object_detection.protos.EvalConfig)
	}
)
_sym_db.RegisterMessage(EvalConfig)

ParameterizedMetric = _reflection.GeneratedProtocolMessageType(
	'ParameterizedMetric', (_message.Message, ),
	{
	'DESCRIPTOR': _PARAMETERIZEDMETRIC,
	'__module__': 'object_detection.protos.eval_pb2'
	# @@protoc_insertion_point(class_scope:object_detection.protos.ParameterizedMetric)
	}
)
_sym_db.RegisterMessage(ParameterizedMetric)

CocoKeypointMetrics = _reflection.GeneratedProtocolMessageType(
	'CocoKeypointMetrics', (_message.Message, ),
	{
	'KeypointLabelToSigmasEntry':
	_reflection.GeneratedProtocolMessageType(
	'KeypointLabelToSigmasEntry', (_message.Message, ),
	{
	'DESCRIPTOR': _COCOKEYPOINTMETRICS_KEYPOINTLABELTOSIGMASENTRY,
	'__module__': 'object_detection.protos.eval_pb2'
	# @@protoc_insertion_point(class_scope:object_detection.protos.CocoKeypointMetrics.KeypointLabelToSigmasEntry)
	}
	),
	'DESCRIPTOR':
	_COCOKEYPOINTMETRICS,
	'__module__':
	'object_detection.protos.eval_pb2'
	# @@protoc_insertion_point(class_scope:object_detection.protos.CocoKeypointMetrics)
	}
)
_sym_db.RegisterMessage(CocoKeypointMetrics)
_sym_db.RegisterMessage(CocoKeypointMetrics.KeypointLabelToSigmasEntry)

KeypointEdge = _reflection.GeneratedProtocolMessageType(
	'KeypointEdge', (_message.Message, ),
	{
	'DESCRIPTOR': _KEYPOINTEDGE,
	'__module__': 'object_detection.protos.eval_pb2'
	# @@protoc_insertion_point(class_scope:object_detection.protos.KeypointEdge)
	}
)
_sym_db.RegisterMessage(KeypointEdge)

_EVALCONFIG.fields_by_name['num_examples']._options = None
_EVALCONFIG.fields_by_name['max_evals']._options = None
_COCOKEYPOINTMETRICS_KEYPOINTLABELTOSIGMASENTRY._options = None
# @@protoc_insertion_point(module_scope)
