"""
Generated from SaslHandshakeRequest.json.

https://github.com/apache/kafka/tree/3.6.0/clients/src/main/resources/common/message/SaslHandshakeRequest.json
"""

from dataclasses import dataclass
from dataclasses import field
from typing import ClassVar

from kio.schema.request_header.v1.header import RequestHeader
from kio.static.primitive import i16
from kio.static.protocol import ApiMessage


@dataclass(frozen=True, slots=True, kw_only=True)
class SaslHandshakeRequest(ApiMessage):
    __version__: ClassVar[i16] = i16(1)
    __flexible__: ClassVar[bool] = False
    __api_key__: ClassVar[i16] = i16(17)
    __header_schema__: ClassVar[type[RequestHeader]] = RequestHeader
    mechanism: str = field(metadata={"kafka_type": "string"})
    """The SASL mechanism chosen by the client."""
