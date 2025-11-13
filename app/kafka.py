import struct
from dataclasses import dataclass, field


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
class ApiVersionResponse:
    message_size: int = field(init=False)
    header: "ResponseHeader"
    body: "ApiVersionResponseBody"

    def __post_init__(self):
        self.message_size = self.header.get_size() + self.body.get_size()

    def to_bytes(self) -> bytes:
        _message_size = struct.pack(">i", self.message_size)
        _header = self.header.to_bytes()
        _body = self.body.to_bytes()

        return b"".join([_message_size, _header, _body])


@dataclass
class ResponseHeader:
    """Kafka Response Header v0"""

    correlation_id: int

    def to_bytes(self) -> bytes:
        return struct.pack(">i", self.correlation_id)

    def get_size(self) -> int:
        return len(self.to_bytes())


@dataclass
class ApiVersionResponseBody:
    error_code: int
    api_versions: "ApiVersionArray" = 0
    throttle_time_ms: int = 0
    TAG_BUFFER: int = 0

    def to_bytes(self) -> bytes:
        _error_code = struct.pack(">h", self.error_code)
        _api_versions = self.api_versions.to_bytes()
        _throttle_time_ms = struct.pack(">i", self.throttle_time_ms)
        _TAG_BUFFER = struct.pack("b", self.TAG_BUFFER)

        return b"".join([_error_code, _api_versions, _throttle_time_ms, _TAG_BUFFER])

    def get_size(self) -> int:
        return len(self.to_bytes())


@dataclass
class ApiVersionArray:
    array_length: int = field(init=False)
    api_versions: list["ApiVersion"]

    def __post_init__(self):
        self.array_length = len(self.api_versions) + 1

    def to_bytes(self) -> bytes:
        _array_length = struct.pack("b", self.array_length)
        _api_versions = [_api_version.to_bytes() for _api_version in self.api_versions]

        return b"".join([_array_length] + _api_versions)


@dataclass
class ApiVersion:
    api_key: int
    min_version: int
    max_version: int
    TAG_BUFFER: int = 0

    def to_bytes(self) -> bytes:
        return struct.pack(
            ">hhhb", self.api_key, self.min_version, self.max_version, self.TAG_BUFFER
        )
