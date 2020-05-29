import socket
from config import SERVER, PORT

def server_connect(SERVER=SERVER, PORT=PORT):
	ADDR = (SERVER, PORT)
	client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	client.connect(ADDR)