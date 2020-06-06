import socket, requests, json
from config import PORT

def server_connect(SERVER, PORT=PORT):
	ADDR = (SERVER, PORT)
	print(ADDR)
	client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	try:
		client.connect(ADDR)
	except ConnectionRefusedError:
		print(
			"Sorry but the Server IP specified is not currently accepting connections, are you sure this is the correct IP?")
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


def server_disconnect(SERVER, PORT=PORT):
	pass