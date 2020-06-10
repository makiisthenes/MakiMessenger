import os, subprocess, time
path = os.getcwd()
client_path = os.path.join(path, 'Client_REWORK')
server_path = os.path.join(path, 'Server_REWORK')

print(path)
with open("server_click_here.cmd", 'w+') as noob:
    noob.write(f"cd {server_path} \n")
    noob.write(f"python server.py \n")
with open("client_click_here.cmd", 'w+') as noob:
    noob.write(f"cd {client_path} \n")
    noob.write(f"python client.py \n")
