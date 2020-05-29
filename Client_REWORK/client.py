import datetime, transaction, os, pickle, socket, hashlib, requests, socket, json
import tkinter as tk
from PIL import ImageTk, Image
from connect import server_connect, get_private_ip
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
	class MakiSession:
		def __init__(self, root):
			self.root = root
			self.ip = get_private_ip()
			self.registered_user = True  # Crosscheck with Server for IP registered.
			if self.registered_user:
				self.login_message = 'Back, '
			else:
				self.login_message = 'Newbie, '
			self.password_cover = ['♦', '♣', '♠', '♥']

		def login_page(self):
			self.main_canvas = tk.Canvas(self.root, width=750, height=500, highlightthickness=5, highlightbackground="black")
			self.main_canvas.pack()
			maki_mail_img = ImageTk.PhotoImage(file=r'..\Resources\makimessenger.png')
			self.main_canvas.create_image(650, 200, image=maki_mail_img)
			self.title = tk.Label(self.main_canvas, text='Maki Messenger')
			self.title.place(relx=0.010, rely=0.010)
			self.title.config(font=('helvetica', int(window_height/40)))
			self.ip_title = tk.Label(self.main_canvas, text=f'Welcome {self.login_message}[{self.ip}]', font=('helvetica', 12, 'bold'))
			self.ip_title.place(x=int(window_width / 100 * 7.5), y=int(window_height / 100 * 14))
			if self.registered_user:
				self.login_title = tk.Label(self.main_canvas, text='Login to Network', font=('helvetica', 10, 'bold'))
				self.login_title.place(x=int(window_width / 100 * 10), y=int(window_height / 100 * 20))
				self.passphrase = tk.Entry(self.main_canvas, relief='solid', show=self.password_cover)
				self.passphrase.insert(0, 'Passphrase')
				self.passphrase.place(x=int(window_width / 100 * 11), y=int(window_height / 100 * 25), width=int(window_width / 4))
				self.login_btn = tk.Button(self.main_canvas)
				self.login_btn.bind('<Return>', None)
				self.login_btn.config(text='Sign In', bg='#377Ef0', fg='#F0F0F0', font=('sans', 9, 'bold'), relief = 'groove', command=None)
				self.login_btn.place(x=int(window_width / 100 * 11), y=int(window_height / 100 * 29.5))
			else:
				pass
			self.root.mainloop()


		def f2a_page(self):
			pass

		def clear_page(self):
			self.main_canvas.delete('all')  # Everything should be build on the main_canvas.
			self.main_canvas.destroy()
			self.title.destroy()

		def network_error_page(self):
			pass

		def settings_page(self):
			pass

	MakiSession(root=root).login_page()
	# MakiSession.clear_page()
