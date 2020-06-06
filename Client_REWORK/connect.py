import socket, requests, json
from config import PORT
from client import SERVER

def server_connect(SERVER=SERVER, PORT=PORT):
	ADDR = (SERVER, PORT)
	client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	try:
		client.connect(ADDR)
	except ConnectionRefusedError:
		print(
			"Sorry but the Server IP specified is not currently accepting connections, are you sure this is the conrrect IP?")
		exit(-1)

def get_private_ip():
	private_ip = socket.gethostbyname(socket.gethostname())
	return private_ip

def get_public_ip():
	try:
		public_ip = json.loads(requests.get('https://api.ipify.org?format=json').content.decode('utf-8'))['ip']
	except Exception:
		public_ip = "0.0.0.0"
	return public_ip
