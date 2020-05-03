import threading
import socket
from csv import reader
import pickle

HEADER = 64
PORT = 5050
SERVER = socket.gethostbyname(socket.gethostname())
print(f'Finds the hostname of system: {socket.gethostname()}')
ADDR = (SERVER, PORT)
FORMAT = 'utf-8'
DISCONNECT_MESSAGE = "!DISCONNECT"


class LiveObject:
    def __init__(self, liveconnections, ip2username):
        self.liveconnections = liveconnections
        self.ip2username = ip2username


# Links the server socket settings with the ip and port
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(ADDR)
live_connections = []
ip2username = {}  # {'ip':'username'}
def handle_client(conn, addr):  # this is the handle client function which deals with the client that has connected, it contains its ip and connections information...
    print(f'New Connection at {addr}')  # the client has send the argument addr which is its IP address...
    connected = True
    while connected:
        try:
            msg_length = conn.recv(HEADER).decode(FORMAT)  # this will tell us what information is going to be send in the header... so we can get ready to get it.. we need to decode it as its send in byte form, so decode utf-8
            if msg_length is not None:  # this is just to make sure the thing send is actually the header and not a None.
                msg_length = int(msg_length)  # now we have the expected length of the message, we can now receive this message with a function
                msg = conn.recv(msg_length).decode(FORMAT)
                if 'CREATE USER' in msg:
                    signup = msg.split(' ')
                    db_string = f'{signup[2]}, {signup[3]}' + '\n'
                    print(db_string)
                    with open('database.csv', 'r') as checker:
                        usernametaken = False
                        csv_reader = reader(checker)
                        for row in csv_reader:
                            print(row)
                            if row[0].strip() == signup[2].strip():
                                usernametaken = True
                    if not usernametaken:
                        with open('database.csv', 'a') as register:
                            register.write(db_string)
                        conn.send("REGISTRATION-SUCCESSFUL".encode(FORMAT))
                    elif usernametaken:
                        conn.send("USERNAME-TAKEN".encode(FORMAT))
                        print('Username is taken')
                elif 'SIGNIN REQ' in msg:
                    signin = msg.split(' ')
                    accountfound = False
                    with open('database.csv', 'r') as checker:
                        csv_reader = reader(checker)
                        for row in csv_reader:
                            if row[0].strip() == signin[2].strip():
                                if row[1].strip() == signin[3].strip():
                                    accountfound = True
                    if accountfound:
                        conn.send("SIGNIN-SUCCESSFUL".encode(FORMAT))
                        ip2username[addr[0]] = signin[2].strip()  # added to ip2username db
                        # ip2username[row[0].strip()]==str(addr)
                    elif not accountfound:
                        conn.send("SIGNIN-UNSUCCESSFUL".encode(FORMAT))
                elif 'PING LIVE' in msg:
                    string = ''
                    # for x in range(len(live_connections)):
                    #     string += str(live_connections[x]) + ' '
                    live = LiveObject(live_connections, ip2username)
                    live_pickle = pickle.dumps(live)
                    # print(live_pickle)
                    conn.send(live_pickle)  # no header, not sure how to use it...
                    # conn.send(string.encode(FORMAT))

                elif msg == DISCONNECT_MESSAGE:
                    connected = False
                    live_connections.remove(addr)
                    try:
                        del ip2username[addr[0]]
                    except KeyError:
                        print('[ERROR]: User has all ready disconnected')
                    print(f"[DISCONNECTED]: [{addr}] {msg}")
                    print(f"[ACTIVE CONNECTIONS] {threading.activeCount()-2}")
        except ConnectionResetError:
            connected = False
            live_connections.remove(addr)
            try:
                del ip2username[addr[0]]
            except KeyError:
                print('[ERROR]: User has all ready disconnected')
            print(f"[DISCONNECTED]: [{addr}]")
            print(f"[ACTIVE CONNECTIONS] {threading.activeCount()-2}")
            # conn.send("Msg received".encode(FORMAT))  # send to user when it has been send...
    conn.close()

def start():  # start function is initiated
    server.listen(10)  # socket that has ip, port and config is set to listen for connections on this port., set to listen to 10 people at a time...
    while True:  # loop this information
        conn, addr = server.accept()  # block, where we wait for connections, in which an ip address and connection info is gained
        thread = threading.Thread(target=handle_client, args=(conn, addr)) # we will hand this to another 'thread' or process in which we will handle this client seperately
        thread.start()  # initiating this thread and keeping this start function running without this process.
        print(f"[ACTIVE CONNECTIONS] {threading.activeCount() - 1}")  # a thread can be seen as a process, we can allow another process to start when we get another connection.
        live_connections.append(addr)
        # Ideally the number of threads is equal to the number of connections present in this server minus the thread process of the servers start process itself...


print(f'[STARTING] Starting Server @ {SERVER}...')
start()
print(f'[STARTED] Starting Server @ {SERVER}...')
