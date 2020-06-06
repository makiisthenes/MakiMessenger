import datetime, transaction, os, pickle, socket, hashlib, requests, socket, json, random, time
import tkinter as tk
from easygui import *
from PIL import ImageTk, Image
from connect import server_connect, get_private_ip, get_public_ip
from tk_starter import tk_init, getwindow
from ping import check_status
from threading import Thread
from config import PORT, HEADER_LENGTH

if __name__ == '__main__':
    SERVER = "169.254.54.35"  # This is the Server IP, please change accordingly.
    msg = "Please type your Servers IP, to use:: "
    title = "Server IP Configure"
    SERVER = enterbox(msg, title)
    if len(SERVER) < 1:
        SERVER = "169.254.54.35"
    print(f"{SERVER}")
    # Initation of Program
    root = tk_init()
    window_height, window_width = getwindow(root)
    server_connect(SERVER)

    # Starting Ping
    Thread(target=check_status, args=(SERVER)).start()


    class MakiSession:
        def __init__(self, root):
            self.root = root
            self.ip = get_private_ip()
            self.pub_ip = get_public_ip()
            self.registered_user = False  # Crosscheck with Server for IP registered.
            if self.registered_user:
                self.login_message = 'Back, '
            else:
                self.login_message = 'Newbie, '
            self.password_cover = random.choice(['♦', '♣', '♠', '♥'])

        def login_page(self):
            self.main_canvas = tk.Canvas(self.root, width=750, height=500, highlightthickness=5,
                                         highlightbackground="black")
            self.main_canvas.pack()
            maki_mail_img = ImageTk.PhotoImage(file=r'..\Resources\makimessenger.png')
            self.main_canvas.create_image(650, 200, image=maki_mail_img)
            self.title = tk.Label(self.main_canvas, text='Maki Messenger')
            self.title.place(relx=0.010, rely=0.010)
            self.title.config(font=('helvetica', int(window_height / 40)))
            self.ip_title = tk.Label(self.main_canvas, text=f'Welcome {self.login_message}[{self.ip}]',
                                     font=('helvetica', 12, 'bold'))
            self.ip_title.place(x=int(window_width / 100 * 7.5), y=int(window_height / 100 * 14))
            self.pub_ip_title = tk.Label(self.main_canvas, text=f'Public IP: [{self.pub_ip}] ',
                                         font=('helvetica', 12, 'bold'))
            self.pub_ip_title.place(x=int(window_width / 100 * 7.5), y=int(window_height / 100 * 10))
            if self.registered_user:
                self.login_title = tk.Label(self.main_canvas, text='Login to Network', font=('helvetica', 10, 'bold'))
                self.login_title.place(x=int(window_width / 100 * 10), y=int(window_height / 100 * 20))
                self.passphrase = tk.Entry(self.main_canvas, relief='solid', show=self.password_cover)
                self.passphrase.insert(0, 'Passphrase')
                self.passphrase.place(x=int(window_width / 100 * 11), y=int(window_height / 100 * 25),
                                      width=int(window_width / 4))
                self.login_btn = tk.Button(self.main_canvas)
                self.login_btn.bind('<Return>', None)
                self.login_btn.config(text='Sign In', bg='#377Ef0', fg='#F0F0F0', font=('sans', 9, 'bold'),
                                      relief='groove', command=None)
                self.login_btn.place(x=int(window_width / 100 * 11), y=int(window_height / 100 * 29.5))
            else:
                self.register_title = tk.Label(self.main_canvas, text='Make an Account on this Network',
                                               font=('helvetica', 10, 'bold'))
                self.register_title.place(x=int(window_width / 100 * 10), y=int(window_height / 100 * 20))
                self.passphrase = tk.Entry(self.main_canvas, relief='solid', show=self.password_cover)
                self.passphrase.insert(0, 'Pass-phrase')
                self.passphrase.place(x=int(window_width / 100 * 11), y=int(window_height / 100 * 25),
                                      width=int(window_width / 4))
                self.register_btn = tk.Button(self.main_canvas)
                self.register_btn.bind('<Return>', None)
                self.register_btn.config(text='Register', bg='#377Ef0', fg='#F0F0F0', font=('sans', 9, 'bold'),
                                         relief='groove', command=None)
                self.register_btn.place(x=int(window_width / 100 * 11), y=int(window_height / 100 * 29.5))
            self.root.mainloop()

        # self.root.quit() break mainloop

        def f2a_page(self):
            # Make 8 code for authentication.
            pass

        def clear_page(self):

            self.main_canvas.delete('all')  # Everything should be build on the main_canvas.
            self.main_canvas.destroy()
            self.title.destroy()

        def network_error_page(self):
            pass

        def settings_page(self):
            pass


    def enc(string):
        string = string.encode('utf-8')
        return string


    def connection_terminal(SERVER, PORT):
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            s.connect((SERVER, PORT))
        except ConnectionRefusedError:
            print(
                "Sorry but the Server IP specified is not currently accepting connections, are you sure this is the conrrect IP?")
            exit(-1)
        message = s.recv(2048)
        print(message.decode("utf-8"))
        generic_data = {1: 'Hey', 2: 'There'}
        while True:
            msg = input("Type message to send to server:: ")
            if not msg:
                pass
            elif msg == '/pickle':
                print('Generic Pickle File is going to be send.')
                data_header = enc(', data:')
                data = pickle.dumps(generic_data)
                header = len(data)
                data_type_header = enc('{data_type:')
                data_type = enc('pickle')
                target_header = enc(', target:')
                target = enc('username')
                timestamp_header = enc(', timestamp:')
                timestamp = enc(str(time.time()))
                msg_end_query = enc('}')
                msg = bytes(f'{header:<{HEADER_LENGTH}}', "utf-8")
                s.send(msg)
                msg = data_type_header + data_type + data_header + data + target_header + target + timestamp_header + timestamp + msg_end_query
            elif msg and msg != '/disconnect':
                msg = f'{len(msg):<{HEADER_LENGTH}}' + msg
                s.send(msg.encode('utf-8'))
            elif msg == '/disconnect':
                msg = f'{len(msg):<{HEADER_LENGTH}}' + msg
                s.send(msg.encode('utf-8'))
                print('Connection has been closed')
                s.close()
                break


    Thread(target=connection_terminal, args=(SERVER, PORT)).start()
    maki = MakiSession(root=root)
    maki.login_page()
# print('Window has been closed')
