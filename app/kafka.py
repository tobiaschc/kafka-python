import struct
from dataclasses import dataclass


@dataclass
class Message:
    message_size: int
    header: "Header"
    body: str = ""

    @classmethod
    def from_bytes(cls, data: bytes) -> "Message":
        """Parses bytes into a Message object."""
        message_size, request_api_key, request_api_version, correlation_id = (
            struct.unpack(">ihhi", data[:12])
        )
        HeaderObj = Header(
            request_api_key=request_api_key,
            request_api_version=request_api_version,
            correlation_id=correlation_id,
            client_id="",
        )

        return cls(message_size=message_size, header=HeaderObj)


@dataclass
class Header:
    """Kafka Request Header v2"""

    request_api_key: int
    request_api_version: int
    correlation_id: int
    client_id: str


@dataclass
class ResponseHeader:
    """Kafka Response Header v0"""

    correlation_id: int


@dataclass
class ApiVersionResponse:
    header: "ResponseHeader"
    error_code: int
    api_versions: "ApiVersionArray"
    throttle_time_ms: int
    TAG_BUFFER: int


@dataclass
class ApiVersionArray:
    array_length: int
    api_versions: list["ApiVersion"]


@dataclass
class ApiVersion:
    api_key: int
    min_version: int
    max_version: int
