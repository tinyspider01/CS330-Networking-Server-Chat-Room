import socket
# 10.240.10.113 iwu network
# 10.0.0.99 isu network
HOST = "10.240.10.113"  # The server's hostname or IP address
PORT = 80  # The port used by the server

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.connect((HOST, PORT))
    s.sendall(b"Hello, world")
    data = s.recv(1024)

print(f"Received {data!r}")
