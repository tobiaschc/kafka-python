import socket

from app.kafka import (
    ApiVersion,
    ApiVersionArray,
    ApiVersionResponse,
    ApiVersionResponseBody,
    Message,
    ResponseHeader,
)


def main():
    server = socket.create_server(("localhost", 9092), reuse_port=True)
    conn, addr = server.accept()
    with conn:
        print(f"Connected by {addr}")

        request = conn.recv(1024)

        print(f"Received request: {request}")

        message = Message.from_bytes(request)
        print(f"Parsed message: {message}")

        request_api_version = message.header.request_api_version
        correlation_id = message.header.correlation_id

        if request_api_version > 4:
            print(f"Unsupported API version: {request_api_version}")
            error_code = 35  # UnsupportedVersion
        else:
            error_code = 0  # No error

        # Create the api version array
        api_version = ApiVersion(
            api_key=message.header.request_api_key, min_version=0, max_version=4
        )
        api_version_array = ApiVersionArray(api_versions=[api_version])

        api_version_response = ApiVersionResponse(
            header=ResponseHeader(correlation_id=correlation_id),
            body=ApiVersionResponseBody(
                error_code=error_code, api_versions=api_version_array
            ),
        )

        response = api_version_response.to_bytes()

        print(f"Response message: {response}")

        conn.sendall(response)


if __name__ == "__main__":
    main()
