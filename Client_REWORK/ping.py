from client import SERVER
import easygui
from pythonping import ping
from time import sleep

def ping_server(SERVER=SERVER):
	pinging = ping(SERVER)
	if pinging.success():
		return True
	else:
		return False


def check_status():
	box_showed = False
	while True:
		status = ping_server()
		if status:
			box_showed = False
			pass
		else:
			if not box_showed:
				print('Connection to Server Failed. Reconnecting...')
				easygui.msgbox("Connection to Server has failed, please reconnect to your network and restart app.", title="Connection Error")
				# Change this to display on main window rather than pop-up box.
				box_showed = True
		sleep(1)
