# This will be used to collect information about the user and validate along side credentials.


# Time Created
import time
timestamp = time.time()  # Epoch Time
print(f"Timestamp Created: {timestamp}")


# Private IP
import socket
def get_ip():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        # doesn't even have to be reachable
        s.connect(('10.255.255.255', 1))
        IP = s.getsockname()[0]
    except Exception:
        IP = ''
    finally:
        s.close()
    return IP
IP = get_ip()
print(f"Private IP: {get_ip()}")


# MAC address of Client.
import netifaces  # Cross Platform :)
for x in netifaces.interfaces():
    if len(netifaces.ifaddresses(x)) > 1:
        # print(netifaces.ifaddresses(x))
        pair = []
        for dict in netifaces.ifaddresses(x):
            item = netifaces.ifaddresses(x)[dict][0]['addr']
            pair.append(item)
        # print(pair)
        if pair[1] == IP:
            mac = pair[0]
            print(f"MAC: {mac}")
        # Check the list for this ip to crosscheck mac address.

# Screen Size
print("Cant find useful screensize module for pc, smartphone compatible.")


# Geo-location
# Done on ServerSide with limited API Calls.

# Device Type/ OS
import socket
hostname = socket.gethostname()
# print(hostname)
# Option 2
import platform
print(f"HostName: {platform.node()}")
# OS
system = platform.system()
release = platform.release()
version = platform.version()
print(f"Platform: {system, release, version}")


# Public IP
from requests import get
pub_ip = get('https://api.ipify.org').text
print(f"Public IP: {pub_ip}")

