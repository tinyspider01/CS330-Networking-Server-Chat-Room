import socket
import threading

HOST = "0.0.0.0"  # Allows for any/all IP addresses to connect
PORT = 80  # Using the default port number

def handle_client(client_socket: socket.socket, address: tuple[str, int]) -> None:
    """Handle a single client connection"""
    try:
        while True:
            # Receive data from client
            data = client_socket.recv(1024)

            # If no data, client disconnected
            if not data:
                break

            # Echo the data back
            print(f"Received from {address}: {data}")
            client_socket.send(data)

    except Exception as e:
        print(f"Error with {address}: {e}")

    finally:
        print(f"Connection closed from {address}")
        client_socket.close()


def main() -> None:
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((HOST, PORT))
    server.listen()

    print(f"Server listening on {HOST}:{PORT}")

    try:
        while True:
            # Accept new connection
            client_socket, address = server.accept()
            print(f"New connection from {address}")

            # Create new thread for this client, passing in the connection's socket
            thread = threading.Thread(target=handle_client, args=(client_socket, address))
            thread.daemon = True  # don't let this thread keep the process alive on its own
            thread.start()

    except KeyboardInterrupt:
        print("\nShutting down server...")

    finally:
        server.close()


if __name__ == "__main__":
    main()