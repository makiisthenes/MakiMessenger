import datetime, transaction, os, pickle, socket, hashlib, requests, socket, json, random, time
import tkinter as tk
from easygui import *
from PIL import ImageTk, Image
from connect import server_connect, get_private_ip, get_public_ip, server_disconnect
from tk_starter import tk_init, getwindow
from ping import check_status
from threading import Thread
from config import PORT, HEADER_LENGTH
from user_object_PC import create_user_object
from file_sorter import server_ip_reader, server_ip_writer

if __name__ == '__main__':


    # Starting Session
    class Splash(tk.Toplevel):
        def __init__(self, parent):
            tk.Toplevel.__init__(self, parent)
            self.title("Maki Loading Page")
            screen_width = self.winfo_screenwidth()
            screen_height = self.winfo_screenheight()
            self.iconbitmap(r'..\Resources\makimessenger.ico')
            self.minsize(window_width, window_height)
            size = f'{window_width}x{window_height}+{int(screen_width / 2 - (window_width / 2))}+{int(screen_height / 2 - (window_height / 2))}'
            current_path = os.getcwd()
            server_pickle_path = os.path.join(current_path, r'..\Resources\loading.png')
            self.gambar = Image.open(server_pickle_path)
            self.imgSplash = ImageTk.PhotoImage(self.gambar)
            self.main_canvas = tk.Canvas(self, width=750, height=500, highlightthickness=5, highlightbackground="black")
            self.main_canvas.pack()
            self.main_canvas.create_image(375, 250, image=self.imgSplash)
            self.update()
            self.geometry(size)


    class MakiSession:
        def __init__(self, root, server_ip):
            root.withdraw()
            splash = Splash(root)
            self.root = root
            self.ip = get_private_ip()
            self.pub_ip = get_public_ip()
            self.server_ip = server_ip
            self.registered_user = False  # Crosscheck with Server for IP registered. function()
            if self.registered_user:
                self.login_message = 'Back, '
            else:
                self.login_message = 'Newbie, '
            self.password_cover = random.choice(['♦', '♣', '♠', '♥'])
            splash.destroy()
            self.root.deiconify()

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
                                         font=('helvetica', 15, 'bold'))
            self.server_title = tk.Label(self.main_canvas, text=f"Server IP: {self.server_ip}",
                                         font=('helvetica', 11, 'bold'))
            self.server_title.place(x=int(window_width / 100 * 75), y=int(window_height / 100 * 90))
            self.pub_ip_title.place(x=int(window_width / 100 * 7.5), y=int(window_height / 100 * 8))
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
                self.email_tag = tk.Label(self.main_canvas, text='Email:: ',
                                          font=('helvetica', 9, 'bold'))
                self.email_tag.place(x=int(window_width / 100 * 9), y=int(window_height / 100 * 25),
                                     width=int(window_width / 4))
                self.email_entry = tk.Entry(self.main_canvas, relief='solid')
                self.email_entry.insert(0, 'email@domain.com')
                self.email_entry.place(x=int(window_width / 100 * 16), y=int(window_height / 100 * 25),
                                       width=int(window_width / 4))
                self.passphrase = tk.Entry(self.main_canvas, relief='solid', show=self.password_cover)
                self.passphrase.insert(0, 'Pass-phrase')
                self.passphrase.place(x=int(window_width / 100 * 16), y=int(window_height / 100 * 30),
                                      width=int(window_width / 4))
                self.register_btn = tk.Button(self.main_canvas)
                self.register_btn.bind('<Return>', None)
                self.register_btn.config(text='Register', bg='#377Ef0', fg='#F0F0F0', font=('sans', 9, 'bold'),
                                         relief='groove', command=None)
                self.register_btn.place(x=int(window_width / 100 * 11), y=int(window_height / 100 * 39.5))
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

    # File Maker
    # this is the file directories needed for this program to run...
    path = os.path.join(os.getcwd(), 'ProgramData')
    if not os.path.exists(path):
        os.makedirs(path)
    chat_path = os.path.join(path, 'Chats')
    if not os.path.exists(chat_path):
        os.makedirs(chat_path)


    # Client starts here -->
    SERVER = server_ip_reader()
    if not SERVER:
        SERVER = "169.254.54.35"
    msg = f"Please type your Server's IP to use; if [current: {SERVER}] click OK"
    title = "Server IP Configure"
    SERVER = enterbox(msg, title)
    if len(SERVER) < 1:
        SERVER = server_ip_reader()
    else:
        server_ip_writer(SERVER)
        print(f"{SERVER}")

    # GUI telling User of connection
    """
    Thread(target=loading_gui, args=()).start()
    def loading_gui():
        current_path = os.getcwd()
        server_pickle_path = os.path.join(current_path, r'..\Resources\loader.gif')
        image = server_pickle_path
        msg = "Messenger is loading..."
        msgbox(msg, title="Loading")
    """
    # Connecting to Server
    server_connect(SERVER)

    # Starting Ping
    Thread(target=check_status, args=(SERVER,)).start()

    # Creating User Object
    user_obj = create_user_object()
    Thread(target=connection_terminal, args=(SERVER, PORT)).start()

    # Initiation of Program
    root = tk_init()
    window_height, window_width = getwindow(root)
    maki = MakiSession(root=root, server_ip=SERVER)
    maki.login_page()
# print('Window has been closed')
