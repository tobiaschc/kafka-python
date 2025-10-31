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

        message_size = struct.unpack(">i", request[0:4])[0]
        print(f"Unpacked message_size: {message_size}")

        request_api_key = struct.unpack(">h", request[4:6])[0]
        print(f"Unpacked request_api_key: {request_api_key}")

        request_api_version = struct.unpack(">h", request[6:8])[0]
        print(f"Unpacked request_api_version: {request_api_version}")

        correlation_id = struct.unpack(">i", request[8:12])[0]
        print(f"Unpacked correlation_id: {correlation_id}")

        # Send back the correlation ID as a 4-byte big-endian integer
        correlation_id_int32 = (correlation_id).to_bytes(
            4, byteorder="big", signed=True
        )
        print(f"Sending back correlation_id: {correlation_id_int32}")

        # Create the response
        # message_size: 4 bytes (just the correlation_id field)
        # correlation_id: 4 bytes with the value from the request
        response_message_size = 4
        response = struct.pack(">ii", response_message_size, correlation_id)

        print(f"Response message: {response}")

        conn.sendall(response)


if __name__ == "__main__":
    main()
