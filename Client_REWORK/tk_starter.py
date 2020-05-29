from config import PATH_TO_MAKI_ICON, window_width, window_height
import tkinter as tk

def tk_init():
	root = tk.Tk()
	root.title('Maki Messenger')
	screen_width = root.winfo_screenwidth()
	screen_height = root.winfo_screenheight()
	root.iconbitmap(r'..\Resources\makimessenger.ico')
	root.minsize(window_width, window_height)
	size = f'{window_width}x{window_height}+{int(screen_width/2-(window_width/2))}+{int(screen_height/2-(window_height/2))}'
	root.geometry(size)
	root.update()
	return root

def getwindow(root):
	window_width = root.winfo_width()
	window_height = root.winfo_height()
	return window_height, window_width

