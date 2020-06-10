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
    return pem, pvem






