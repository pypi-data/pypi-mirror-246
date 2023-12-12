"""
Generated from LeaveGroupRequest.json.

https://github.com/apache/kafka/tree/3.6.0/clients/src/main/resources/common/message/LeaveGroupRequest.json
"""

from dataclasses import dataclass
from dataclasses import field
from typing import ClassVar

from kio.schema.request_header.v2.header import RequestHeader
from kio.schema.types import GroupId
from kio.static.primitive import i16
from kio.static.protocol import ApiMessage


@dataclass(frozen=True, slots=True, kw_only=True)
class MemberIdentity:
    __version__: ClassVar[i16] = i16(5)
    __flexible__: ClassVar[bool] = True
    __api_key__: ClassVar[i16] = i16(13)
    __header_schema__: ClassVar[type[RequestHeader]] = RequestHeader
    member_id: str = field(metadata={"kafka_type": "string"})
    """The member ID to remove from the group."""
    group_instance_id: str | None = field(
        metadata={"kafka_type": "string"}, default=None
    )
    """The group instance ID to remove from the group."""
    reason: str | None = field(metadata={"kafka_type": "string"}, default=None)
    """The reason why the member left the group."""


@dataclass(frozen=True, slots=True, kw_only=True)
class LeaveGroupRequest(ApiMessage):
    __version__: ClassVar[i16] = i16(5)
    __flexible__: ClassVar[bool] = True
    __api_key__: ClassVar[i16] = i16(13)
    __header_schema__: ClassVar[type[RequestHeader]] = RequestHeader
    group_id: GroupId = field(metadata={"kafka_type": "string"})
    """The ID of the group to leave."""
    members: tuple[MemberIdentity, ...]
    """List of leaving member identities."""
