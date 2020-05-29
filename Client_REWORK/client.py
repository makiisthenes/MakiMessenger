import datetime, transaction, os, pickle, socket, hashlib, requests, socket, json
import tkinter as tk
from PIL import ImageTk, Image
from connect import server_connect
from tk_starter import tk_init, getwindow
from ping import check_status
from threading import Thread


if __name__ == '__main__':
	# Initation of Program
	server_connect()
	# Starting Ping
	Thread(target=check_status, args=()).start()
	root = tk_init()
	window_height, window_width = getwindow(root)
	# Main Page  - Make this an Class Object
	class MakiSession:
		def __init__(self, root):
			self.root = root
		def login_page(self):
			self.main_canvas = tk.Canvas(self.root, width=750, height=500)
			self.main_canvas.pack()
			maki_mail_img = ImageTk.PhotoImage(file=r'..\Resources\makimessenger.png')
			self.main_canvas.create_image(675, 200, image=maki_mail_img)
			self.title = tk.Label(self.root, text='Maki Messenger')
			self.title.place(relx=0, rely=0)
			self.title.config(font=('helvetica', int(window_height/40)))
			login = tk.Label(self.main_canvas, text='Login to Network', font=('helvetica', 10, 'bold'))
			login.place(x=int(window_width / 100 * 10), y=int(window_height / 100 * 20))


			self.root.mainloop()

		def clear_page(self):
			self.main_canvas.delete('all')  # Everything should be build on the main_canvas.
			self.main_canvas.destroy()
			self.title.destroy()

	MakiSession(root=root).login_page()
