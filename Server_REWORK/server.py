import socket, sys, threading, pickle, select, pyDH, os, shutil, hashlib, csv, base64
from pythonping import ping
from encryption import generate_key_pair
from cryptography.fernet import Fernet

def encrypt_msg(message, shared_key):
    encryptor = Fernet(shared_key)
    encrypted_msg = encryptor.encrypt(message)
    return encrypted_msg

def decryptor_msg(message, shared_key):
    decryptor = Fernet(shared_key)
    decrypted_msg = decryptor.decrypt(message)
    return decrypted_msg

# Fernet key must be 32 url-safe base64-encoded bytes [problem]


class Client:
    def __init__(self, ip, d1, d1_pubkey, d2_pubkey, d1_sharedkey):
        self.c_ip = ip
        self.private_key = d1
        self.d1_pubkey = d1_pubkey
        self.d2_pubkey = d2_pubkey
        self.c2csharedkey = d1_sharedkey


def handle_client_recv(conn, addr):
    global recepient_public
    key_good = False
    server_has_key = False
    # Connection has been made with this client.
    print(f'[CONNECTION] Connected at {addr}.')

    # DH Key Exchange between Server and Client
    print("Creating EE2E connection between Server and Client [DH Exchange]")
    # 4096-bit Key Generation
    d2 = pyDH.DiffieHellman(16)
    print(len(str(d2.gen_public_key())))
    print("Created DH Object")
    print("Getting Public Key")
    while not key_good:
        recepient_public = conn.recv(8192)
        recepient_public = int(recepient_public.decode('utf-8'))
        check = d2.check_other_public_key(recepient_public)
        if check:
            conn.send(b"200")
            key_good = True
            print('Checked Public Key [200]')
        else:
            conn.send(b"400")

    private_key = d2.get_private_key()
    print("Generating Private Key")
    print(private_key)
    print("Sending Public Key")
    while not server_has_key:
        public_key = d2.gen_public_key()
        conn.send(str(public_key).encode('utf-8'))
        status = int(conn.recv(3).decode('utf-8'))
        if status == 200:
            server_has_key = True
            print("Key is OK [200]")
            print(public_key)
    shared_sym_key = d2.gen_shared_key(recepient_public)
    print(f"Shared: {shared_sym_key}")
    Connected = True
    print("[LISTENING] Listening for user messages...")
    while Connected:
        pass
    '''
    # Now using connection with both keys.
    full_msg = ''
    new_msg = True
    Connected = True
    msg_len = 0
    while Connected:
        # Makes sure full message is fully processed.
        msg = conn.recv(10)  # 1024 bytes buffer size. // Header Length
        if new_msg:
            msg_len = int(msg[:HEADER_LENGTH])
            new_msg = False
            print(msg_len)
        # print(HEADER_LENGTH)
        full_msg += msg.decode('utf-8')
        if len(full_msg) - HEADER_LENGTH == msg_len:
            # print('[Message Received!]')
            print(full_msg[HEADER_LENGTH:])
            new_msg = True
            full_msg = ''
            if full_msg[HEADER_LENGTH:] == '/disconnect':
                conn.close()
                Connected = False
            elif full_msg[HEADER_LENGTH:] != '/disconnect':
                print(full_msg[HEADER_LENGTH:])
        '''
def send_msg(conn, addr, msg):
    pass


# SOCK_STREAM - tcp connection
def start():  # start function is initiated
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server_address = (server_ip, server_port)
    print(f'[STARTED] Starting Server @ {server_ip}:{server_port}')
    server.bind(server_address)
    server.listen(
        10)  # socket that has ip, port and config is set to listen for connections on this port., set to listen to 10 people at a time...
    while True:  # loop this information
        conn, addr = server.accept()  # block, where we wait for connections, in which an ip address and connection info is gained
        thread = threading.Thread(target=handle_client_recv, args=(
        conn, addr))  # we will hand this to another 'thread' or process in which we will handle this client seperately
        thread.start()  # initiating this thread and keeping this start function running without this process.
        print(
            f"[ACTIVE CONNECTIONS] {threading.activeCount() - 1}")  # a thread can be seen as a process, we can allow another process to start when we get another connection.
    # Ideally the number of threads is equal to the number of connections present in this server minus the thread process of the servers start process itself...

def file_manager():
    current_path = os.getcwd()
    database_path = os.path.join(current_path, 'Database')
    print(database_path)
    if not os.path.exists(database_path):
        os.makedirs(database_path)
        db_csv = os.path.join(database_path, "maki_database.csv")
        print("[CREATED] Database Path has been Created")
        with open(db_csv, 'w+') as csvwriter:
            csvwriter.write("Username, Email, SHA256_password, user_pickle, private_key, epoch_user_created")
            print("[CREATED] Database File has been Created")


HEADER = 2048
FORMAT = "utf-8"
# server_ip = '169.254.54.35'
server_ip = socket.gethostbyname(socket.gethostname())
server_port = 5050
HEADER_LENGTH = 10
print(f'[STARTING] Starting Server @ {server_ip}...')
file_manager()
start()
