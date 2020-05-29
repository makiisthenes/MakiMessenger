# Asymmetric Encryption
# This script still needs to be worked on to be a good off standard.


# Getting Key
from cryptography.hazmat.backends import default_backend  # used for backend of key creation
from cryptography.hazmat.primitives.asymmetric import rsa  # used to create key pairs
from cryptography.hazmat.primitives import serialization  # serialization to save keys.
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import padding

private_key = rsa.generate_private_key(
    public_exponent=65537,  # If in doubt you should use 65537.
    key_size=2048,  # keys generated in 2015 it is strongly recommended to be at least 2048 , https://en.wikipedia.org/wiki/Key_size, 2^2048 possible keys available.
    backend=default_backend())
public_key = private_key.public_key()

# Storing Public Keys
KEY_PASSWORD = 'Password'.encode()
pem = public_key.public_bytes(
    encoding=serialization.Encoding.PEM,
    format=serialization.PublicFormat.SubjectPublicKeyInfo)

with open('public_key.pem', 'wb') as f:
    f.write(pem)


# Storing Private Keys
encryption_algorithm = serialization.BestAvailableEncryption(password=KEY_PASSWORD)  # Password Protected Encrypted Key.


# Reading Keys
with open("public_key.pem", "rb") as key_file:
    public_key = serialization.load_pem_public_key(
        key_file.read(),
        backend=default_backend())

# Encrypting
message = b'Encrypt Me!'
# Use one of the methods above to get your public key
encrypted = public_key.encrypt(
    message,
    padding.OAEP(
        mgf=padding.MGF1(algorithm=hashes.SHA256()),
        algorithm=hashes.SHA256(),
        label=None))

# Decrypting
# Variables required: encrypted, private_key
original_message = private_key.decrypt(
    encrypted,
    padding.OAEP(
        mgf=padding.MGF1(algorithm=hashes.SHA256()),
        algorithm=hashes.SHA256(),
        label=None))

# Encrypting and Decrypting Files
f = open('test.txt', 'rb')
message = f.read()
f.close()

encrypted = 'data from encryption'
f = open('test.encrypted', 'wb')
f.write(encrypted)
f.close()

# Site: https://nitratine.net/blog/post/asymmetric-encryption-and-decryption-in-python/


# python -m pip install --upgrade pip --force-reinstall
