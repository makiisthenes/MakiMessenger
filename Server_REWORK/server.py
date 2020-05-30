import socket, sys, threading
from pythonping import ping


def handle_client(conn, addr):
    conn.send("Welcome to the server.".encode('utf-8'))
    full_msg = ''
    new_msg = True
    msg = conn.recv(10)  # 1024 bytes buffer size.
    recieving = True
    while recieving:
        if new_msg:
            msg_len = int(msg[:HEADER_LENGTH].decode('utf-8'))
            new_msg = False
            full_msg += msg.decode('utf-8')
        elif len(full_msg) != msg_len and not new_msg:
            full_msg += msg.decode('utf-8')
            new_msg = False
            if len(full_msg) == msg_len:
                recieving = False
                print('Message Recived')
    print(full_msg[HEADER_LENGTH:])





# SOCK_STREAM - tcp connection
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_port = 5050
HEADER_LENGTH = 10
server_ip = socket.gethostbyname(socket.gethostname())
server_ip = '169.254.54.35'
server_address = (server_ip, server_port)
print(f'Starting Server on [{server_ip}] port [{server_port}]')
server.bind(server_address)
server.listen(5)  # Max Connections Allowed.
print("[STARTED] Server has started.")
print("Looking for clients to join.")
while True:
    connection, client_address = server.accept()
    threading.Thread(target=handle_client, args=(connection, client_address)).start()
    print(f'Connection from {client_address}')
    print(f"[ACTIVE CONNECTIONS] {threading.activeCount() - 1}")

