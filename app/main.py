import socket
import struct


def main():
    # You can use print statements as follows for debugging,
    # they'll be visible when running tests.
    print("Logs from your program will appear here!")

    server = socket.create_server(("localhost", 9092), reuse_port=True)
    conn, addr = server.accept()
    with conn:
        print(f"Connected by {addr}")

        request = conn.recv(1024)

        print(f"Received request: {request}")

        message_size, request_api_key, request_api_version, correlation_id = (
            struct.unpack(">ihhi", request[:12])
        )

        if request_api_version > 4:
            print(f"Unsupported API version: {request_api_version}")
            error_code = 35  # UnsupportedVersion
        else:
            error_code = 0  # No error

        response_message_size = 4 + 2  # correlation_id (4 bytes) + error_code (2 bytes)
        response = struct.pack(
            ">iih", response_message_size, correlation_id, error_code
        )

        print(f"Response message: {response}")

        conn.sendall(response)


if __name__ == "__main__":
    main()
