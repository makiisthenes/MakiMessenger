import os, subprocess, time
path = os.getcwd()
client_path = os.path.join(path, 'Client_REWORK')
server_path = os.path.join(path, 'Server_REWORK')

with open("im_a_noob_help_click_me.cmd", "w+") as noob:
    noob.write(f"cd {path} \n")
    noob.write(f"pip install -r requirements.txt")
subprocess.call("im_a_noob_help_click_me.cmd")
time.sleep(0.5)
with open("im_a_noob_help_click_me.cmd", "w+") as noob:
    noob.write("python noob_script.py \n")
print(path)
with open("server_click_here.cmd", 'w+') as noob:
    noob.write(f"cd {server_path} \n")
    noob.write(f"python server.py \n")
with open("client_click_here.cmd", 'w+') as noob:
    noob.write(f"cd {client_path} \n")
    noob.write(f"python client.py \n")
