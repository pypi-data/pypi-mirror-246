"""
Generated from ApiVersionsRequest.json.

https://github.com/apache/kafka/tree/3.6.0/clients/src/main/resources/common/message/ApiVersionsRequest.json
"""

from dataclasses import dataclass
from typing import ClassVar

from kio.schema.request_header.v1.header import RequestHeader
from kio.static.primitive import i16
from kio.static.protocol import ApiMessage


@dataclass(frozen=True, slots=True, kw_only=True)
class ApiVersionsRequest(ApiMessage):
    __version__: ClassVar[i16] = i16(1)
    __flexible__: ClassVar[bool] = False
    __api_key__: ClassVar[i16] = i16(18)
    __header_schema__: ClassVar[type[RequestHeader]] = RequestHeader
