import socket, sys, threading, pickle, select
from pythonping import ping


def handle_client_recv(conn, addr):
    print(f'[CONNECTION] Connected at {addr}.')
    conn.send("Welcome to the server.".encode('utf-8'))
    full_msg = ''
    new_msg = True
    Connected = True
    msg_len = 0
    # 10      {data_type:pickle, data:data, target:username, timestamp:time}
    while Connected:
        # Makes sure full message is fully processed.
        msg = conn.recv(10)  # 1024 bytes buffer size. // Header Length
        if new_msg:
            msg_len = int(msg[:HEADER_LENGTH])
            new_msg = False
            print(msg_len)
        # print(HEADER_LENGTH)
        full_msg += msg.decode('utf-8')
        if len(full_msg)-HEADER_LENGTH == msg_len:
            # print('[Message Received!]')
            print(full_msg[HEADER_LENGTH:])
            new_msg = True
            full_msg = ''
            if full_msg[HEADER_LENGTH:] == '/disconnect':
                conn.close()
                Connected = False
            elif full_msg[HEADER_LENGTH:] != '/disconnect':
                print(full_msg[HEADER_LENGTH:])

def send_msg(conn, addr, msg):
    pass


# SOCK_STREAM - tcp connection
server_port = 5050
HEADER_LENGTH = 10
# server_ip = socket.gethostbyname(socket.gethostname())
server_ip = '169.254.54.35'
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
server_address = (server_ip, server_port)
print(f'Starting Server on [{server_ip}]:[{server_port}]')
server.bind(server_address)
server.listen(5)
print("[STARTED] Server has Started...")


while True:
    connection, client_address = server.accept()
    threading.Thread(target=handle_client_recv, args=(connection, client_address)).start()
    print(f"[ACTIVE CONNECTIONS] {threading.activeCount() - 1}")

