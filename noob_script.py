import os, subprocess, time
path = os.getcwd()
client_path = os.path.join(path, 'Client_REWORK')
server_path = os.path.join(path, 'Server_REWORK')

print(path)
with open("im_a_noob_help.cmd", 'w+') as noob:
    noob.write(f"cd {path} \n")
    noob.write("pip install -r requirements.txt \n")
    noob.write("python noob_script.py")
with open("server_click_here.cmd", 'w+') as noob:
    noob.write(f"cd {server_path} \n")
    noob.write(f"python server.py \n")
with open("client_click_here.cmd", 'w+') as noob:
    noob.write(f"cd {client_path} \n")
    noob.write(f"python client.py \n")

subprocess.call('im_a_noob_help.cmd')
subprocess.call('server_click_here.cmd')
time.sleep(2)
subprocess.call('client_click_here.cmd')
