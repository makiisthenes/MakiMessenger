import datetime, transaction, os, pickle, socket, hashlib, requests, socket, json, random
import tkinter as tk
from easygui import *
from PIL import ImageTk, Image
from connect import server_connect, get_private_ip, get_public_ip, server_disconnect, encrypt_msg, decrypt_msg
from tk_starter import tk_init, getwindow
from ping import check_status
from threading import Thread
from config import PORT, HEADER_LENGTH
from user_object_PC import create_user_object
from file_sorter import server_ip_reader, server_ip_writer, file_manager

if __name__ == '__main__':
    version = "Alpha v1.0.1"
    # Starting Session

    class Splash(tk.Toplevel):
        def __init__(self, parent):
            tk.Toplevel.__init__(self, parent)
            self.title("Maki Loading Page")
            screen_width = self.winfo_screenwidth()
            screen_height = self.winfo_screenheight()
            self.iconbitmap(r'..\Resources\makimessenger.ico')
            window_height, window_width = 500, 750
            self.minsize(window_width, window_height)
            size = f'{window_width}x{window_height}+{int(screen_width / 2 - (window_width / 2))}+{int(screen_height / 2 - (window_height / 2))}'
            current_path = os.getcwd()
            server_pickle_path = os.path.join(current_path, r'..\Resources\loading.png')
            self.image = Image.open(server_pickle_path)
            self.imgSplash = ImageTk.PhotoImage(self.image)
            self.main_canvas = tk.Canvas(self, width=750, height=500, highlightthickness=5, highlightbackground="black")
            self.main_canvas.pack()
            self.main_canvas.create_image(375, 250, image=self.imgSplash)
            size = f'{window_width}x{window_height}+{int(screen_width / 2 - (window_width / 2))}+{int(screen_height / 2 - (window_height / 2))}'
            self.geometry(size)
            self.update()


    class MakiSession:
        def __init__(self, root, server_ip):
            # Request Encryption Key Pair
            self.pub_key = ''
            root.withdraw()
            splash = Splash(root)
            self.root = root
            self.ip = get_private_ip()
            self.pub_ip = get_public_ip()
            self.server_ip = server_ip
            self.password_cover = random.choice(['♦', '♣', '♠', '♥'])
            splash.destroy()
            self.root.deiconify()

        def login_page(self):
            self.main_canvas = tk.Canvas(self.root, width=750, height=500, highlightthickness=5, highlightbackground="black")
            self.main_canvas.pack()
            # maki_mail_img = ImageTk.PhotoImage(file=r'..\Resources\makimessenger.png')
            # self.main_canvas.create_image(650, 200, image=maki_mail_img)
            photo = ImageTk.PhotoImage(file=r'..\Resources\makimessenger.png')
            label = tk.Label(self.main_canvas, image=photo)
            label.image = photo
            label.place(x=int(window_width/100*55), y=int(window_height/100*-10))
            self.title = tk.Label(self.main_canvas, text='Maki Messenger')
            self.title.place(relx=0.010, rely=0.010)
            self.title.config(font=('helvetica', int(window_height / 40)))
            self.version_tag = tk.Label(self.main_canvas, text=version)
            self.version_tag.place(x=int(window_width / 100 * 2.5), y=int(window_height / 100 * 92.5))
            self.ip_title = tk.Label(self.main_canvas, text=f'Welcome Makier [{self.ip}]', font=('helvetica', 12, 'bold'))
            self.ip_title.place(x=int(window_width / 100 * 7.5), y=int(window_height / 100 * 14))
            self.pub_ip_title = tk.Label(self.main_canvas, text=f'Public IP: [{self.pub_ip}] ', font=('helvetica', 15, 'bold'))
            self.server_title = tk.Label(self.main_canvas, text=f"Server IP: {self.server_ip}", font=('helvetica', 11, 'bold'))
            self.server_title.place(x=int(window_width / 100 * 75), y=int(window_height / 100 * 92.5))
            self.pub_ip_title.place(x=int(window_width / 100 * 7.5), y=int(window_height / 100 * 8))
            self.login_title = tk.Label(self.main_canvas, text='Login to Network', font=('helvetica', 10, 'bold'))
            self.login_title.place(x=int(window_width / 100 * 10), y=int(window_height / 100 * 20))
            self.login_email_tag = tk.Label(self.main_canvas, text='Email: ', font=('helvetica', 9, 'bold'))
            self.login_email_tag.place(x=int(window_width / 100 * 10.5), y=int(window_height / 100 * 25), width=int(window_width / 100 * 5))
            self.login_email_entry = tk.Entry(self.main_canvas, relief='solid')
            self.login_email_entry.insert(0, '')
            self.login_email_entry.place(x=int(window_width / 100 * 16), y=int(window_height / 100 * 25), width=int(window_width / 4))
            self.passphrase = tk.Entry(self.main_canvas, relief='solid', show=self.password_cover)
            self.passphrase.insert(0, '')
            self.passphrase.place(x=int(window_width / 100 * 16), y=int(window_height / 100 * 30), width=int(window_width / 4))
            self.login_pass_tag = tk.Label(self.main_canvas, text='Pass: ', font=('helvetica', 9, 'bold'))
            self.login_pass_tag.place(x=int(window_width / 100 * 10.5), y=int(window_height / 100 * 30), width=int(window_width / 100 * 5))
            self.login_btn = tk.Button(self.main_canvas)
            self.login_btn.bind('<Return>', None)
            def login_query():
                pass
            self.login_btn.config(text='Sign In', bg='#377Ef0', fg='#F0F0F0', font=('sans', 9, 'bold'), relief='groove', command=lambda: login_query(self))
            self.login_btn.place(x=int(window_width / 100 * 16), y=int(window_height / 100 * 34.5))
            self.register_title = tk.Label(self.main_canvas, text='Make an Account on this Network', font=('helvetica', 10, 'bold'))
            self.register_title.place(x=int(window_width / 100 * 10), y=int(window_height / 100 * 40))
            self.email_tag = tk.Label(self.main_canvas, text='Email: ', font=('helvetica', 9, 'bold'))
            self.email_tag.place(x=int(window_width / 100 * 10.5), y=int(window_height / 100 * 45), width=int(window_width / 100 * 5))
            self.email_entry = tk.Entry(self.main_canvas, relief='solid')
            self.email_entry.insert(0, 'email@domain.com')
            self.email_entry.place(x=int(window_width / 100 * 16), y=int(window_height / 100 * 45), width=int(window_width / 4))
            self.regist_passphrase = tk.Entry(self.main_canvas, relief='solid', show=self.password_cover)
            self.regist_passphrase.insert(0, 'Pass-phrase')
            self.regist_passphrase.place(x=int(window_width / 100 * 16), y=int(window_height / 100 * 50), width=int(window_width / 4))
            self.register_pass_tag = tk.Label(self.main_canvas, text='Pass: ', font=('helvetica', 9, 'bold'))
            self.register_pass_tag.place(x=int(window_width / 100 * 10.5), y=int(window_height / 100 * 50), width=int(window_width / 100 * 5))
            def send_query():
                pass
            self.register_btn = tk.Button(self.main_canvas)
            self.register_btn.bind('<Return>', None)
            self.register_btn.config(text='Register', bg='#377Ef0', fg='#F0F0F0', font=('sans', 9, 'bold'), relief='groove', command=lambda: send_query())
            self.register_btn.place(x=int(window_width / 100 * 16), y=int(window_height / 100 * 55))


        # self.root.quit() break mainloop

        def f2a_page(self):
            # Make 8 code for authentication.
            pass

        def clear_page(self):
            self.main_canvas.delete('all')  # Everything should be build on the main_canvas.
            self.main_canvas.destroy()
            self.title.destroy()
            self.root.quit()

        def maingui(self):  # root == self of session
            window_width = self.root.winfo_width()
            window_height = self.root.winfo_height()
            print(window_height)
            print(window_width)

            top_frameuser = tk.Frame(self.root, width=round(window_width / 100 * 30), height=round(window_height / 100 * 10))
            top_framemsg = tk.Frame(self.root, width=round(window_width / 100 * 70), height=round(window_height / 100 * 10))  # background='yellow'
            message_frame = tk.Frame(self.root, width=round(window_width / 100 * 70), height=round(window_height / 100 * 90))  # background='green'
            container = tk.Frame(self.root, width=round(window_width / 100 * 30), height=round(window_height / 100 * 90), background='orange')
            message_content = tk.Frame(message_frame, width=round(window_width / 100 * 70), height=round(window_height / 100 * 80))  # background='green'
            message_config = tk.Frame(message_frame, width=round(window_width / 100 * 70), height=round(window_height / 100 * 10), highlightbackground="black",highlightthickness=1)  # background='red'
            message_canvas = tk.Canvas(message_content, height=round(window_height / 100 * 80))  # background='green'
            message_canvas.pack(fill=tk.BOTH, expand=1, side='top')
            message_content_scrollbar = tk.Scrollbar(message_canvas, orient="vertical")  # need to add scrollbar for message content frame...
            message_content_scrollbar.pack(fill=tk.Y, side=tk.RIGHT)  # need to add scrollbar for message content frame...
            live_contacts = tk.Frame(container, width=round(window_width / 100 * 30), height=round(window_height / 100 * 45), background='orange')
            live_contacts_canvas = tk.Canvas(live_contacts, width=round(window_width / 100 * 30), height=round(window_height / 100 * 45))  # , bg ='green'
            live_contacts_canvas.pack(fill=tk.BOTH, expand=1, side='top')
            live_contacts_content_scrollbar = tk.Scrollbar(live_contacts_canvas, orient="vertical")  # need to add scrollbar for message content frame...
            live_contacts_content_scrollbar.pack(fill=tk.Y, side=tk.RIGHT)
            my_contacts = tk.Frame(container, width=round(window_width / 100 * 30), height=round(window_height / 100 * 45))  # background='purple'
            my_contacts_canvas = tk.Canvas(my_contacts, width=round(window_width / 100 * 30), height=round(window_height / 100 * 45))  # , bg ='green'
            my_contacts_canvas.pack(fill=tk.BOTH, expand=True, side='bottom')
            my_contacts_scrollbar = tk.Scrollbar(my_contacts_canvas, orient="vertical")
            my_contacts_scrollbar.pack(fill=tk.Y, side=tk.RIGHT)

            # --> Part of message content frame
            send_config = tk.Frame(message_config, width=round(window_width / 100 * 10), height=round(window_height / 100 * 10), background='blue')
            input_config = tk.Frame(message_config, width=round(window_width / 100 * 60), height=round(window_height / 100 * 10), background='orange')

            # Threads that need to be running are here.
            # message_canvas_thread = threading.Thread(target=message_listener, args=(message_canvas, recieved_message)).start()
            # thread = threading.Thread(target=ping, args=(live_contacts_canvas, username, my_contacts_canvas)).start()
            # print('Ping has started.')

            # Essential Widgets
            live_chat = tk.Label(top_framemsg, text='[Select a User to Start Chat.]', pady=round(window_height / 100 * 4.3), padx=10)  # dynamic widget here..
            # live_chat_name_changer(live_chat)
            live_chat.pack(side='top', expand=tk.YES, fill=tk.Y, anchor=tk.W)
            f = tk.Frame(top_framemsg, height=1, width=round(window_width / 100 * 70), bg="black")
            f.pack(side='top', expand=tk.YES, fill=tk.X, anchor=tk.W)

            # this is for the extended layout of the page...
            root.grid_rowconfigure(0, weight=0)
            root.grid_rowconfigure(1, weight=1)
            root.grid_columnconfigure(0, weight=0)
            root.grid_columnconfigure(1, weight=1)

            top_frameuser.grid_configure(sticky="nsew")  # no child elements
            top_frameuser.grid(row=0, column=0)

            top_framemsg.grid_configure(sticky="nsew")  # 2 child elements
            top_framemsg.grid(row=0, column=1)
            # top_framemsg.grid_rowconfigure(0, weight=1)
            # top_framemsg.grid_rowconfigure(1, weight=1)
            # top_framemsg.grid_columnconfigure(0, weight=0)
            # live_chat.grid_configure(sticky="nsew")
            # f.grid_configure(sticky="nsew")

            container.grid_configure(sticky="nsew")  # 2 child
            container.grid(row=1, column=0)
            container.grid_rowconfigure(0, weight=1)
            live_contacts.grid_configure(sticky='nsew')
            live_contacts.grid(row=0, column=0)

            container.grid_rowconfigure(1, weight=1)
            container.grid_columnconfigure(0, weight=0)
            my_contacts.grid_configure(sticky='nsew')
            my_contacts.grid(row=1, column=0)

            message_frame.grid_configure(sticky="nsew")  # 2 child --> 2 child
            # message_canvas.grid_configure(sticky='nsew')
            message_frame.grid(row=1, column=1)
            message_frame.grid_columnconfigure(0, weight=1)
            message_frame.grid_rowconfigure(0, weight=1000)  # this makes message content box fully extend.
            message_content.grid(row=0, column=0)  # no child elements
            message_content.grid_configure(sticky="new")
            message_frame.grid_rowconfigure(1, weight=1)
            message_config.grid(row=1, column=0)  # 2 child elements
            message_config.grid_configure(sticky="sew")
            message_config.grid_rowconfigure(0,
                                             weight=0)  # doesnt allow the message box to expand more than necesary, but leave empty space
            message_config.grid_columnconfigure(0, weight=1)
            input_config.grid(row=0, column=0)
            input_config.grid_configure(sticky='ew')
            message_config.grid_columnconfigure(1, weight=0)
            send_config.grid(row=0, column=1)
            send_config.grid_configure(sticky='ew')
            # added logo to program -- DONE
            logocanvas = tk.Canvas(top_frameuser, width=round(window_width / 100 * 30),
                                   height=round(window_height / 100 * 10))
            logocanvas.pack()
            img = Image.open('../Resources/logo.png')
            img = img.resize((round(window_width / 100 * 25), round(window_height / 100 * 10)), Image.ANTIALIAS)
            logo = ImageTk.PhotoImage(img)  # .convert('RGB') this mess' up with PNG files
            label = tk.Label(logocanvas, width=round(window_width / 100 * 24), height=round(window_height / 100 * 10),
                             image=logo)
            label.image = logo
            label.pack()
            logo_underline = tk.Frame(top_frameuser, height=1, width=round(window_width / 100 * 25), bg="black")
            logo_underline.pack()

            # child widgets in parent frames
            large_font = ('Verdana', 12)
            send_input = tk.Entry(input_config, font=large_font, border=0)
            send_input.insert(0, 'Enter Message Here...')
            send_input.pack(expand=True, fill='x')
            # send_input.grid(row=0, column=0)
            # send_input.grid_configure(sticky='nsew')

            # my_contacts_listbox_creator(my_contacts_canvas)

            # The above code will add all known contacts onto the contacts window in which it can be accessed.

            def targetsend():
                message = send_input.get()
                if len(message) > 0:
                    print(message)
                    # message_saver()
                    message_widget_creator(message, message_canvas)  # function creates a message on the screen...
                    messagetime = datetime.datetime.now().strftime("%H:%M")
                    # message = {'type':'send', 'ip': target_ip, 'time': str(messagetime), 'message': str(message)}
                    send_input.delete(0, len(message))

                # need to check message format and determine header and person this is being send to...
                # make sure it doesnt include any code that can be used to break program
                # record time and person send to, and save in new database for person, with text file that is parsed and then used to display on screen...

            send_btn = tk.Button(send_config, text='Send',
                                 command=targetsend)  # want to use different channel for this, than communicating with server.
            send_btn.place(relx=0.5, rely=0.5, anchor=tk.CENTER)
            send_btn.config(width=round(window_width / 100 * 10), height=round(window_height / 100 * 10))
            contacts_underline = tk.Frame(my_contacts, height=1, width=round(window_width / 100 * 25), bg="black")
            contacts_underline.pack()
            contacts = tk.Label(my_contacts, text='My Contacts')  # dynamic widget here..
            contacts.pack()
            live_contacts_canvas.pack(expand=True, fill='both')

        def network_error_page(self):
            pass

        def settings_page(self):
            pass


    def enc(string):
        string = string.encode('utf-8')
        return string

    def onclose():
        pass

    # this makes sure the file directories needed for this program to run are present...
    file_manager()

    # Client starts here -->
    SERVER = server_ip_reader()
    if not SERVER:
        SERVER = "169.254.54.35"
        server_ip_writer(SERVER)
    msg = f"Please type your Server's IP to use; if [current: {SERVER}] click OK"
    title = "Server IP Configure"
    SERVER = enterbox(msg, title)
    try:    
        if len(SERVER) < 1:
            SERVER = server_ip_reader()
        else:
            server_ip_writer(SERVER)
            print(f"{SERVER}")
    except TypeError:
        print('User has cancelled operation!')
        exit(-1)
    # Connecting to Server
    shared_sym_key = server_connect(SERVER)

    # Starting Ping
    Thread(target=check_status, args=(SERVER,)).start()

    # Creating User Object
    user_obj = Thread(target=create_user_object, args=()).start()

    # Initiation of Program Loading
    root = tk_init()
    root.protocol("WM_DELETE_WINDOW", lambda arg=0: onclose())
    window_height, window_width = getwindow(root)
    maki = MakiSession(root=root, server_ip=SERVER)
    maki.login_page()
    #maki.maingui()
    # maki.root.update()
    maki.root.mainloop()
    print('Screen has changed, out of main loop')

