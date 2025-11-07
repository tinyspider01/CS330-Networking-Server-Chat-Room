import socket

HOST = "0.0.0.0"  # Allows for any/all IP addresses to connect
PORT = 65432  # Using the default port number

# AF_INET is the family address for IPv4 and SOCK_STREAM is the socket type
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    # .bind() is used to associate the socket with a specific network interface and port number
    s.bind((HOST, PORT))
    # .listen() allows the server to accpet connections
    s.listen()
    # .accept() blocks execution and waits for an incoming connection
    conn, addr = s.accept()
    # This reads whatever data the client sends and echoes it back using conn.sendall()
    with conn:
        print(f"Connected by {addr}")
        while True:
            data = conn.recv(1024)
            if not data:
                break
            conn.sendall(data)