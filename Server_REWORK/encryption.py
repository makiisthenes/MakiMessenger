from cryptography.hazmat.backends import default_backend  # used for backend of key creation
from cryptography.hazmat.primitives.asymmetric import rsa  # used to create key pairs
from cryptography.hazmat.primitives import serialization  # serialization to save keys.
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import padding


def generate_key_pair(KEY_PASSWORD='Gong4231'):
    private_key = rsa.generate_private_key(
        public_exponent=65537,  # If in doubt you should use 65537.
        key_size=2048,
        # keys generated in 2015 it is strongly recommended to be at least 2048 , https://en.wikipedia.org/wiki/Key_size, 2^2048 possible keys available.
        backend=default_backend())
    public_key = private_key.public_key()
    pem = public_key.public_bytes(encoding=serialization.Encoding.PEM,
                                  format=serialization.PublicFormat.SubjectPublicKeyInfo)
    with open('public_key.pem', 'wb') as f:
        f.write(pem)
    print(public_key)
    print(pem.decode("utf-8"))
    pvem = private_key.private_bytes(encoding=serialization.Encoding.PEM,
                                     format=serialization.PrivateFormat.TraditionalOpenSSL,
                                     encryption_algorithm=serialization.NoEncryption())
    print(pvem.decode("utf-8"))
    # encryption_algorithm = serialization.BestAvailableEncryption(password=KEY_PASSWORD.encode('utf-8'))
    # Obtaining Private Key
    return (pem, pvem)

generate_key_pair()



# Another Option to Use.
from Crypto import Random
from Crypto.PublicKey import RSA
import base64

def generate_keys():
    # RSA modulus length must be a multiple of 256 and >= 1024
    modulus_length = 256 * 4  # use larger value in production
    privatekey = RSA.generate(modulus_length, Random.new().read)
    publickey = privatekey.publickey()
    return privatekey, publickey


def encrypt_message(a_message, publickey):
    encrypted_msg = publickey.encrypt(a_message, 32)[0]
    encoded_encrypted_msg = base64.b64encode(encrypted_msg)  # base64 encoded strings are database friendly
    return encoded_encrypted_msg


def decrypt_message(encoded_encrypted_msg, privatekey):
    decoded_encrypted_msg = base64.b64decode(encoded_encrypted_msg)
    decoded_decrypted_msg = privatekey.decrypt(decoded_encrypted_msg)
    return decoded_decrypted_msg
