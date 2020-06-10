import json
import pyDH
import socket
import requests
from config import PORT
from cryptography.fernet import Fernet


class Client:
	def __init__(self, ip, d1, d1_pubkey, d2_pubkey, d1_sharedkey):
		self.c_ip = ip  # Users IP
		self.private_key = d1  # Current Private Key
		self.d1_pubkey = d1_pubkey  # My Public Key
		self.d2_pubkey = d2_pubkey  # Their Public Key
		self.c2csharedkey = d1_sharedkey  # Shared Key generated on both sides.


def server_connect(SERVER, PORT=PORT):
	global recepient_public
	ADDR = (SERVER, PORT)
	print(ADDR)
	client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

	try:
		client.connect(ADDR)
		# DH Key Exchange between Server and Client
		key_good = False
		print("Creating EE2E connection between Server and Client [DH Exchange]")
		# 4096-bit Key Generation
		d2 = pyDH.DiffieHellman(16)
		print("[DH Created] DH Object Created Successfully")
		private_key = d2.get_private_key()
		print("[PRIVATE] Private Key Generated Successfully")
		# print(public_key)
		# print(private_key)
		server_has_key = False
		print("[TRANSIT] Public Key is being transferred to Server")
		while not server_has_key:
			public_key = d2.gen_public_key()
			client.send(str(public_key).encode('utf-8'))
			status = int(client.recv(3).decode('utf-8'))
			if status == 200:
				server_has_key = True
				print("Key is OK [200]")
		print("[TRANSIT] Getting Public Key")
		while not key_good:
			recepient_public = client.recv(8192)
			recepient_public = int(recepient_public.decode('utf-8'))
			check = d2.check_other_public_key(recepient_public)
			if not check:
				client.send(b"400")
			else:
				client.send(b"200")
				key_good = True
				print("Key is OK [200]")
		shared_sym_key = d2.gen_shared_key(recepient_public)
		print(f"[GENERATED] Shared Key has been Generated: {shared_sym_key}")
		print("[CONNECTION] Connection has been made securely with 4096-bit EE2Encryption to Server")
		return shared_sym_key

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



def encrypt_msg(message, shared_key):
	encryptor = Fernet(shared_key)
	encrypted_msg = encryptor.encrypt(message)
	return encrypted_msg

def decrypt_msg(message, shared_key):
	decryptor = Fernet(shared_key)
	decrypted_msg = decryptor.decrypt(message)
	return decrypted_msg



# Fernet key must be 32 url-safe base64-encoded bytes [problem]