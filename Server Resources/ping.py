import pyping

ip = '192.168.1.7'
r = pyping.ping(ip)
if r.ret_code == 0:
    print('This IP is online!')
else:
    print('Connection to server has failed, please try to reconnect.')