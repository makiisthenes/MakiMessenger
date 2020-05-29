import datetime, transaction, os, pickle, socket, threading, time, ZODB.FileStorage, hashlib, requests, socket, json
import tkinter as tk
from PIL import ImageTk, Image
from connect import server_connect
from tk_starter import tk_init, getwindow


if __name__ != '__main__':
	print('Client is not running as main script.')
	exit(0)


# Initation of Program
server_connect()
root = tk_init()
window_height, window_width = getwindow(root)



# Main Page  - Make this an Class Object
main_canvas = tk.Canvas(root, width=750, height=500)
main_canvas.pack()

maki_mail_img = ImageTk.PhotoImage(file=r'..\Resources\makimessenger.png')
main_canvas.create_image(650, 200, image=maki_mail_img, anchor=tk.N)
title = tk.Label(root, text='Maki Messenger')
title.place(relx=0, rely=0)
title.config(font=('helvetica', int(window_height/40)))


root.mainloop()  # Allow Program To Run.