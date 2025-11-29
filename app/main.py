import socket
import threading

from app.client import handle

HOST = "localhost"
PORT = 9092


def main():
    print(f"Server starting on {HOST}:{PORT}")

    try:
        with socket.create_server((HOST, PORT), reuse_port=True) as server:
            print(f"Server listening on {HOST}:{PORT}")

            while True:
                client, addr = server.accept()
                print(f"Connection established with {addr}")
                threading.Thread(target=handle, args=(client,)).start()

    except Exception as e:
        print(f"Server error: {e}")


if __name__ == "__main__":
    main()
