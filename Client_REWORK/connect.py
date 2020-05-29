import socket
from config import SERVER, PORT

def server_connect(SERVER=SERVER, PORT=PORT):
	ADDR = (SERVER, PORT)
	client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	client.connect(ADDR)

def get_private_ip():
	private_ip = socket.gethostbyname(socket.gethostname())
	return private_ip 