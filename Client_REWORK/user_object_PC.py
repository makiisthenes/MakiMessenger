# This will be used to collect information about the user and validate along side credentials.
import socket
import time
import netifaces  # Cross Platform :)
import platform
from requests import get
import pickle



class UserObject:
    def __init__(self, timestamp, priv_ip, mac, hostname, system, release, version, pub_ip):
        self.timestamp = timestamp
        self.priv_ip = priv_ip
        self.mac = mac
        self.hostname = hostname
        self.system = system
        self.release = release
        self.version = version
        self.pub_ip = pub_ip
    def parser(self, text_file):
        # discontinued currently.
        pass


def create_user_object():
    # Time Created
    timestamp = time.time()  # Epoch Time
    print(f"Timestamp Created: {timestamp}")
    # Private IP
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
    priv_ip = get_ip()
    print(f"Private IP: {get_ip()}")
    # MAC address of Client.
    mac = ''
    for x in netifaces.interfaces():
        if len(netifaces.ifaddresses(x)) > 1:
            # print(netifaces.ifaddresses(x))
            pair = []
            for dict in netifaces.ifaddresses(x):
                item = netifaces.ifaddresses(x)[dict][0]['addr']
                pair.append(item)
            # print(pair)
            if pair[1] == priv_ip:
                mac = pair[0]
                print(f"MAC: {mac}")
            # Check the list for this ip to crosscheck mac address.
    # Screen Size
    print("Cant find useful screensize module for pc, smartphone compatible.")
    # Geo-location
    print("Geolocation cannot be determined")
    # Done on ServerSide with limited API Calls.
    # Device Type/ OS
    hostname0 = socket.gethostname()
    # print(hostname)
    # Option 2
    hostname = platform.node()
    print(f"HostName: {hostname}")
    # OS
    system = platform.system()
    release = platform.release()
    version = platform.version()
    print(f"Platform: {system, release, version}")
    # Public IP
    pub_ip = get('https://api.ipify.org').text
    print(f"Public IP: {pub_ip}")
    user_object = UserObject(timestamp, priv_ip, mac, hostname, system, release, version, pub_ip)
    print("[PICKLED] Users data has been pickled and sent to Server.")
    pickle_object = pickle.dumps(user_object)
    return pickle_object

