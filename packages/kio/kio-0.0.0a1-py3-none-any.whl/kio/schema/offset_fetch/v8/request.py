"""
Generated from OffsetFetchRequest.json.

https://github.com/apache/kafka/tree/3.6.0/clients/src/main/resources/common/message/OffsetFetchRequest.json
"""

from dataclasses import dataclass
from dataclasses import field
from typing import ClassVar

from kio.schema.request_header.v2.header import RequestHeader
from kio.schema.types import GroupId
from kio.schema.types import TopicName
from kio.static.primitive import i16
from kio.static.primitive import i32
from kio.static.protocol import ApiMessage


@dataclass(frozen=True, slots=True, kw_only=True)
class OffsetFetchRequestTopics:
    __version__: ClassVar[i16] = i16(8)
    __flexible__: ClassVar[bool] = True
    __api_key__: ClassVar[i16] = i16(9)
    __header_schema__: ClassVar[type[RequestHeader]] = RequestHeader
    name: TopicName = field(metadata={"kafka_type": "string"})
    """The topic name."""
    partition_indexes: tuple[i32, ...] = field(
        metadata={"kafka_type": "int32"}, default=()
    )
    """The partition indexes we would like to fetch offsets for."""


@dataclass(frozen=True, slots=True, kw_only=True)
class OffsetFetchRequestGroup:
    __version__: ClassVar[i16] = i16(8)
    __flexible__: ClassVar[bool] = True
    __api_key__: ClassVar[i16] = i16(9)
    __header_schema__: ClassVar[type[RequestHeader]] = RequestHeader
    group_id: GroupId = field(metadata={"kafka_type": "string"})
    """The group ID."""
    topics: tuple[OffsetFetchRequestTopics, ...]
    """Each topic we would like to fetch offsets for, or null to fetch offsets for all topics."""


@dataclass(frozen=True, slots=True, kw_only=True)
class OffsetFetchRequest(ApiMessage):
    __version__: ClassVar[i16] = i16(8)
    __flexible__: ClassVar[bool] = True
    __api_key__: ClassVar[i16] = i16(9)
    __header_schema__: ClassVar[type[RequestHeader]] = RequestHeader
    groups: tuple[OffsetFetchRequestGroup, ...]
    """Each group we would like to fetch offsets for"""
    require_stable: bool = field(metadata={"kafka_type": "bool"}, default=False)
    """Whether broker should hold on returning unstable offsets but set a retriable error code for the partitions."""
