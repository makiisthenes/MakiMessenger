# This is a sketch I have made of the 2FAuth required for users to login to an specific network.
import os
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.twofactor.hotp import HOTP
from cryptography.hazmat.primitives.hashes import SHA1
from cryptography.hazmat.primitives.twofactor import InvalidToken
from email_send import send_f2a


def verify_user(user):
    notVerified = True
    key = os.urandom(20)
    hotp = HOTP(key, 8, SHA1(), backend=default_backend())
    hotp_value = hotp.generate(0)
    f2a_pin = hotp_value.decode('utf-8')
    print(f"F2A Pin = {f2a_pin}")
    send_f2a(user, f2a_pin)
    print('Since this IP has already been registered and logged on, collect an F2A pin for the admin.')
    x = 3

    # On Server-Side relayed to Front-End
    while notVerified:
        user_input = input('Enter 2FA Pin to unlock this account:: ').replace('/', '').encode()  # Encoding into bytes form.
        try:
            hotp.verify(user_input, 0)  # Verify Code on server-side.
            print('Successful F2A PIN, logging into this account')
            notVerified = False

        except InvalidToken:
            if x < 1:
                print('F2A Account Blocked, Contact System Admin')
                exit(-1)
            else:
                print(f'Invalid PIN [{x} Attempts left]')
                x -= 1
