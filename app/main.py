import socket


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

        # Create response message
        # message_size: 4 bytes (32-bit signed integer) - any value works for this stage
        # correlation_id: 4 bytes (32-bit signed integer) - must be 7
        message_size = (4).to_bytes(4, byteorder="big", signed=True)
        correlation_id = (7).to_bytes(4, byteorder="big", signed=True)

        response_msg = b"".join(
            [
                message_size,
                correlation_id,
            ]
        )

        print(f"Sending response: {response_msg}")

        conn.sendall(response_msg)


if __name__ == "__main__":
    main()
