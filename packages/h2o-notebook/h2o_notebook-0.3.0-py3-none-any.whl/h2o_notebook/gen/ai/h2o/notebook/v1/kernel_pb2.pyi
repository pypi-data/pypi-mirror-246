from google.api import resource_pb2 as _resource_pb2
from google.api import field_behavior_pb2 as _field_behavior_pb2
from google.protobuf import timestamp_pb2 as _timestamp_pb2
from google.protobuf.internal import enum_type_wrapper as _enum_type_wrapper
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class Kernel(_message.Message):
    __slots__ = ("name", "display_name", "type", "image", "cpu_request", "cpu_limit", "gpu_resource_name", "gpu_request", "gpu_limit", "memory_bytes_request", "memory_bytes_limit", "yaml_pod_template_spec", "create_time", "creator", "update_time", "updater")
    class Type(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
        __slots__ = ()
        TYPE_UNSPECIFIED: _ClassVar[Kernel.Type]
        TYPE_PYTHON: _ClassVar[Kernel.Type]
        TYPE_R: _ClassVar[Kernel.Type]
        TYPE_SPARK_PYTHON: _ClassVar[Kernel.Type]
        TYPE_SPARK_R: _ClassVar[Kernel.Type]
    TYPE_UNSPECIFIED: Kernel.Type
    TYPE_PYTHON: Kernel.Type
    TYPE_R: Kernel.Type
    TYPE_SPARK_PYTHON: Kernel.Type
    TYPE_SPARK_R: Kernel.Type
    NAME_FIELD_NUMBER: _ClassVar[int]
    DISPLAY_NAME_FIELD_NUMBER: _ClassVar[int]
    TYPE_FIELD_NUMBER: _ClassVar[int]
    IMAGE_FIELD_NUMBER: _ClassVar[int]
    CPU_REQUEST_FIELD_NUMBER: _ClassVar[int]
    CPU_LIMIT_FIELD_NUMBER: _ClassVar[int]
    GPU_RESOURCE_NAME_FIELD_NUMBER: _ClassVar[int]
    GPU_REQUEST_FIELD_NUMBER: _ClassVar[int]
    GPU_LIMIT_FIELD_NUMBER: _ClassVar[int]
    MEMORY_BYTES_REQUEST_FIELD_NUMBER: _ClassVar[int]
    MEMORY_BYTES_LIMIT_FIELD_NUMBER: _ClassVar[int]
    YAML_POD_TEMPLATE_SPEC_FIELD_NUMBER: _ClassVar[int]
    CREATE_TIME_FIELD_NUMBER: _ClassVar[int]
    CREATOR_FIELD_NUMBER: _ClassVar[int]
    UPDATE_TIME_FIELD_NUMBER: _ClassVar[int]
    UPDATER_FIELD_NUMBER: _ClassVar[int]
    name: str
    display_name: str
    type: Kernel.Type
    image: str
    cpu_request: int
    cpu_limit: int
    gpu_resource_name: str
    gpu_request: int
    gpu_limit: int
    memory_bytes_request: int
    memory_bytes_limit: int
    yaml_pod_template_spec: str
    create_time: _timestamp_pb2.Timestamp
    creator: str
    update_time: _timestamp_pb2.Timestamp
    updater: str
    def __init__(self, name: _Optional[str] = ..., display_name: _Optional[str] = ..., type: _Optional[_Union[Kernel.Type, str]] = ..., image: _Optional[str] = ..., cpu_request: _Optional[int] = ..., cpu_limit: _Optional[int] = ..., gpu_resource_name: _Optional[str] = ..., gpu_request: _Optional[int] = ..., gpu_limit: _Optional[int] = ..., memory_bytes_request: _Optional[int] = ..., memory_bytes_limit: _Optional[int] = ..., yaml_pod_template_spec: _Optional[str] = ..., create_time: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ..., creator: _Optional[str] = ..., update_time: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ..., updater: _Optional[str] = ...) -> None: ...
