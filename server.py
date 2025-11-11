import socket
import threading

HOST = "0.0.0.0"  # Allows for any/all IP addresses to connect
PORT = 80  # Using the default port number

socket_list = []

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
            try:
                for client in socket_list:
                    if client != client_socket:
                        client.send(data)
                    else:
                        continue
            except BrokenPipeError:
                socket_list.remove(client_socket)
            except ConnectionResetError:
                socket_list.remove(client_socket)

    except Exception as e:
        print(f"Error with {address}: {e}")
        socket_list.remove(client_socket)

    finally:
        print(f"Connection closed from {address}")
        socket_list.remove(client_socket)
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
            socket_list.append(client_socket)

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