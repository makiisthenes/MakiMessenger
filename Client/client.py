# Currently working on creating persistent friend list and chat path logs. [02/05/2020]
# Currently working on merging the object, friends lists together for GUI. [03/05/2020]
# Make the listbox fit into the contacts window box. [03/05/2020]


import datetime, transaction, os, pickle, socket, threading, time, ZODB.FileStorage, hashlib
import tkinter as tk
from PIL import ImageTk, Image

# this is the file directories needed for this program to run...
path = os.path.join(os.getcwd(), 'ProgramData')
if not os.path.exists(path):
    os.makedirs(path)
chat_path = os.path.join(path, 'Chats')
if not os.path.exists(chat_path):
    os.makedirs(chat_path)

# this is for persistent storing of friends list in local files
pickle_friends_file = 'friends.pickle'
pickle_friends_path = os.path.join(chat_path, pickle_friends_file)
try:
    with open(pickle_friends_path, 'rb') as f:
        friends_added = pickle.load(f)
except:
    friends_added = []
pickle_object_file = 'friends_object.pickle'
pickle_object_path = os.path.join(chat_path, pickle_object_file)
try:
    with open(pickle_object_path, 'rb') as f:
        friend_object = pickle.load(f)
        print(f'Friend Object Pickle List {friend_object}')  # [<__main__.addFriend object at 0x0666E810>]
except:
    friend_object = []

# Use of ZODB FileStorage
mydata_path = os.path.join(chat_path, 'mydata.fs')
storage = ZODB.FileStorage.FileStorage(mydata_path)
db = ZODB.DB(storage)
connection = db.open()
db_root = connection.root()
db_root['conn'] = 999
db_root['live'] = []
transaction.get().commit()
unique_ip = []


class LiveObject:
    def __init__(self, liveconnections, ip2username):
        self.liveconnections = liveconnections  # list --> tuple
        self.ip2username = ip2username  # dictionary
    def parseinfo(self, live_contacts_content, username, my_contacts_canvas):
        isOnline = False
        no_conn = len(self.liveconnections)
        db_root = connection.root()
        if db_root['conn'] == 999:
            db_root['conn'] = no_conn
            # print(f'Connections: {db_root["conn"]}')
            transaction.get().commit()
        else:
            if db_root['conn'] > no_conn:  # when previous connection is more than current, connections have been lost.
                pass
            elif db_root['conn'] == no_conn: # when previous connection is the same as current, connections are constant.
                pass
            elif db_root['conn'] < no_conn:  # when previous connection is less than current, connections have been gained.
                pass
        string = ''
        for x in range(len(self.liveconnections)):
            isUser = False
            # isOnline = False
            addr = self.liveconnections[x]  # a tuple value here...
            ip, port = addr
            string += f',{ip}'
            string = string.replace(string[0], '')
            # print(f'String: {string}')
            try:
                name = self.ip2username.get(ip)
                # print(f'Name: {name}')
                if name == username:
                    isUser = True
                    # isUser = False  # DEBUGGING TOGGLE.
                if len(db_root['live']) < 1:
                    db_root['live'] = string
                if len(db_root['live']) > 0:
                    list = db_root['live']
                    list = list.split(',')
                    # print(f'List: {list}')
                    for x in range(len(list)):
                        if len(list[x]) != 0:
                            print(f'IP: {list[x]}')
                            print(f'Unqiue IPs:')
                            if str(list[x]) not in unique_ip:
                                unique_ip.append(str(list[x]))  # these are the ip's that are in connection with server.
                                isOnline = True
                                liveuserbox_creator(ip, name, isOnline, live_contacts_content, isUser, my_contacts_canvas)  # this creates the live listbox on app...
                                # print(f'Unqiue IP {str(unique_ip)}')
                            elif str(list[x]) in unique_ip:
                                for x in range(len(self.liveconnections)):
                                    ip, conn = self.liveconnections[x]
                                    if ip == str(list[x]):
                                        print(f'Conn of this IP is: {conn}')
            except Exception as e:
                print(f'[Error HERE]: {e}')
                db_root['live'] = unique_ip
                transaction.get().commit()
                connection.close()

                # print('Made listbox for live user...')
                # liveuserbox_remover()
                # need to check if ip has different port, whether list has been shortened or extended, for disconnections and connections. For external connections

def ping(live_contacts_content, username, my_contacts_canvas):
    while True:
        try:
            msg = 'PING LIVE'
            print('Thread is working')
            message = msg.encode(FORMAT)
            msg_length = len(message)
            send_length = str(msg_length).encode(FORMAT)
            send_length += b' ' * (HEADER - len(send_length))
            client.send(send_length)
            client.send(message)
            # live_clients = client.recv(2048).decode(FORMAT)
            live_clients = client.recv(2048)
            live_clients = pickle.loads(live_clients)
            # print(type(live_clients))
            print(f'Live connections: {live_clients.liveconnections}')
            print(f' IP2USERNAME: {live_clients.ip2username}')
            live_clients.parseinfo(live_contacts_content, username, my_contacts_canvas)
            time.sleep(10)
        except Exception as e:
            print('Ohh you have disconnected from server, restart app and login to connect again.')
            print(f'[Error]: {e}')
            break
    exit()


def send(msg, username):
    message = msg.encode(FORMAT)
    msg_length = len(message)
    send_length = str(msg_length).encode(FORMAT)
    send_length += b' ' * (HEADER - len(send_length))
    client.send(send_length)
    client.send(message)
    status = client.recv(2048).decode(FORMAT)
    if status == 'REGISTRATION-SUCCESSFUL':
        print('REGISTRATION-SUCCESSFUL')
        thread_error = threading.Thread(target=errorhandler, args=('REGISTRATION-SUCCESSFUL',))
        thread_error.start()
    elif status == 'SIGNIN-SUCCESSFUL':
        print('SIGNIN-SUCCESSFUL')
        refresh(username)
    elif status == 'USERNAME-TAKEN':
        print('USERNAME-TAKEN')
        thread_error = threading.Thread(target=errorhandler, args=('USERNAME-TAKEN',))
        thread_error.start()
    elif status == 'SIGNIN-UNSUCCESSFUL':
        print('SIGNIN-UNSUCCESSFUL')
        thread_error = threading.Thread(target=errorhandler, args=('SIGNIN-UNSUCCESSFUL',))
        thread_error.start()


print('Starting...')
error = None
HEADER = 64
PORT = 5050
FORMAT = 'utf-8'
DISCONNECT_MESSAGE = "!DISCONNECT"
SERVER = "169.254.54.35"  # this is the server of the pc...  # 10.136.149.136
ADDR = (SERVER, PORT)
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(ADDR)
print('Connected to server')
root = tk.Tk()
# root.configure(background='AntiqueWhite1')
root.iconbitmap('Resources/makimessenger.ico')
screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()
window_height = 500
window_width = 750
root.minsize(window_width, window_height)
# root.maxsize(window_width+300, window_height)
size = f'{window_width}x{window_height}+{int(screen_width/2-(window_width/2))}+{int(screen_height/2-(window_height/2))}'
root.geometry(size)
# root.resizable(width=False, height=False)  # this needs to be worked on before hand
root.update()  # update the window for when the canvas was added and then request the width and height
window_width = root.winfo_width()
window_height = root.winfo_height()
print(window_height)
print(window_width)


def refresh(username):
    login.place_forget()
    login_user_input.place_forget()
    login_pass_input.place_forget()
    signup.place_forget()
    register_user_input.place_forget()
    register_pass_input.place_forget()
    login_btn.place_forget()
    register_btn.destroy()
    canvas1.delete('all')
    canvas1.destroy()
    title.destroy()
    loader(username)


def loader(username):
    time.sleep(3)
    maingui(username)


def errorhandler(msg):
    if msg == 'input':
        error = tk.Label(root, text='Input cannot be empty', fg='red', font=('helvetica', 10, 'bold'))
        error.place(x=int(window_width / 100 * 25), y=int(window_height / 100 * 56))
        time.sleep(3)
        error.place_forget()
    if msg == 'inputsignin':
        error = tk.Label(root, text='Input cannot be empty', fg='red', font=('helvetica', 10, 'bold'))
        error.place(x=int(window_width / 100 * 25), y=int(window_height / 100 * 35))
        time.sleep(3)
        error.place_forget()
    if msg == 'USERNAME-TAKEN':
        error = tk.Label(root, text='Username has been taken', fg='red', font=('helvetica', 10, 'bold'))
        error.place(x=int(window_width / 100 * 25), y=int(window_height / 100 * 56))
        time.sleep(3)
        error.place_forget()
    if msg == 'SIGNIN-UNSUCCESSFUL':
        error = tk.Label(root, text='Incorrect Username or Password', fg='red', font=('helvetica', 10, 'bold'))
        error.place(x=int(window_width / 100 * 25), y=int(window_height / 100 * 35))
        time.sleep(3)
        error.place_forget()
    if msg == 'REGISTRATION-SUCCESSFUL':
        error = tk.Label(root, text='Registration was successful', fg='green', font=('helvetica', 10, 'bold'))
        error.place(x=int(window_width / 100 * 25), y=int(window_height / 100 * 56))
        time.sleep(5)
        error.place_forget()
    if msg == 'usermax10':
        error = tk.Label(root, text='Max User Length is 10!!', fg='red', font=('helvetica', 10, 'bold'))
        error.place(x=int(window_width / 100 * 25), y=int(window_height / 100 * 56))
        time.sleep(5)
        error.place_forget()

root.protocol("WM_DELETE_WINDOW", lambda arg=0: onclose(arg))
canvas1 = tk.Canvas(root, width=712, height=512)
canvas1.pack()
tk_img = ImageTk.PhotoImage(file='Resources/makimessenger.png')
canvas1.create_image(550, 200, image=tk_img)
root.title('Maki Messenger')
title = tk.Label(root, text='Maki Messenger')
title.place(relx=0, rely=0)
login = tk.Label(root, text='Login to your Account', font=('helvetica', 10, 'bold'))
login.place(x=int(window_width/100*10), y=int(window_height/100*20))
login_user_input = tk.Entry(root)
login_user_input.insert(0, 'Username')
login_user_input.place(x=int(window_width/100*12), y=int(window_height/100*25), width=int(window_width/2))
login_pass_input = tk.Entry(root, show="*")
login_pass_input.insert(0, 'Password')
login_pass_input.place(x=int(window_width/100*12), y=int(window_height/100*30), width=int(window_width/2))
title.config(font=('helvetica', int(window_height/40)))
login_btn = tk.Button(root)


def signinreq(event=None):
    global error
    username = login_user_input.get().strip()
    password = login_pass_input.get().strip()
    password_hash = hashlib.sha256(bytes(password)).hexdigest()  # SHA-256 Hash
    if len(username) and len(password) != 0:
        send(f'SIGNIN REQ {username} {password}', username)

    elif len(username) or len(password) == 0:
        thread_error = threading.Thread(target=errorhandler, args=('inputsignin'))
        thread_error.start()
    login_user_input.delete(0, len(username))
    login_pass_input.delete(0, len(password))

login_btn.bind('<Return>', signinreq)
login_btn.config(text='Sign In', bg='green', fg='white', font=('helvetica', 9, 'bold'), command=signinreq)
login_btn.place(x=int(window_width/100*12), y=int(window_height/100*35))
signup = tk.Label(root, text='Sign Up', font=('helvetica', 10, 'bold'))
signup.place(x=int(window_width/100*10), y=int(window_height/100*41))
register_user_input = tk.Entry(root)
register_user_input.insert(0, 'Username')
register_user_input.place(x=int(window_width/100*12), y=int(window_height/100*46), width=int(window_width/2))
register_pass_input = tk.Entry(root, show="*")
register_pass_input.insert(0, 'Password')
register_pass_input.place(x=int(window_width/100*12), y=int(window_height/100*51), width=int(window_width/2))
register_btn = tk.Button(root)

def registerreq(event=None):
    username = register_user_input.get().strip()
    password = register_pass_input.get().strip()
    password_hash = hashlib.sha256(bytes(password)).hexdigest()  # SHA-256 Hash
    if len(username) < 10:
        if len(username) or len(password) != 0:
            print(f'CREATE USER {username} {password}')
            send(f'CREATE USER {username} {password}', username)
        elif len(username) or len(password) == 0:
            thread_error = threading.Thread(target=errorhandler, args=('input',))
            thread_error.start()
    else:
        thread_error = threading.Thread(target=errorhandler, args=('usermax10',))
        thread_error.start()
    register_user_input.delete(0, len(username))
    register_pass_input.delete(0, len(password))


register_btn.bind('<Return>', registerreq)
register_btn.config(text='Sign Up', bg='green', fg='white', font=('helvetica', 9, 'bold'), command=registerreq)
register_btn.place(x=int(window_width/100*12), y=int(window_height/100*56))


def maingui(username):
    root.update()
    window_width = root.winfo_width()
    window_height = root.winfo_height()
    print(window_height)
    print(window_width)

    top_frameuser = tk.Frame(root, width=round(window_width/100*30), height=round(window_height/100*10))
    top_framemsg = tk.Frame(root, width=round(window_width/100*70), height=round(window_height/100*10))  # background='yellow'
    message_frame = tk.Frame(root, width=round(window_width/100*70), height=round(window_height/100*90))  # background='green'
    container = tk.Frame(root, width=round(window_width/100*30), height=round(window_height/100*90), background='orange')
    message_content = tk.Frame(message_frame, width=round(window_width/100*70), height=round(window_height/100*80))  # background='green'
    message_config = tk.Frame(message_frame, width=round(window_width/100*70), height=round(window_height/100*10), highlightbackground="black", highlightthickness=1)  # background='red'
    message_canvas = tk.Canvas(message_content, height=round(window_height/100*80))  # background='green'
    message_canvas.pack(fill=tk.BOTH, expand=1, side='top')
    message_content_scrollbar = tk.Scrollbar(message_canvas, orient="vertical")  # need to add scrollbar for message content frame...
    message_content_scrollbar.pack(fill=tk.Y, side=tk.RIGHT)                     # need to add scrollbar for message content frame...
    live_contacts = tk.Frame(container, width=round(window_width/100*30), height=round(window_height/100*45), background='orange')
    live_contacts_canvas = tk.Canvas(live_contacts, width=round(window_width/100*30), height=round(window_height/100*45))  # , bg ='green'
    live_contacts_canvas.pack(fill=tk.BOTH, expand=1, side='top')
    live_contacts_content_scrollbar = tk.Scrollbar(live_contacts_canvas, orient="vertical")  # need to add scrollbar for message content frame...
    live_contacts_content_scrollbar.pack(fill=tk.Y, side=tk.RIGHT)
    my_contacts = tk.Frame(container, width=round(window_width / 100 * 30), height=round(window_height / 100 * 45))  # background='purple'
    my_contacts_canvas = tk.Canvas(my_contacts, width=round(window_width / 100 * 30), height=round(window_height / 100 * 45), bg='green')  # , bg ='green'
    my_contacts_canvas.pack(fill=tk.BOTH, expand=True, side='bottom')
    my_contacts_scrollbar = tk.Scrollbar(my_contacts_canvas, orient="vertical")
    my_contacts_scrollbar.pack(fill=tk.Y, side=tk.RIGHT)

    # --> Part of message content frame
    send_config = tk.Frame(message_config, width=round(window_width / 100 * 10), height=round(window_height / 100 * 10), background='blue')
    input_config = tk.Frame(message_config, width=round(window_width / 100 * 60), height=round(window_height / 100 * 10), background='orange')

    # Threads that need to be running are here.
    # message_canvas_thread = threading.Thread(target=message_listener, args=(message_canvas, recieved_message)).start()
    thread = threading.Thread(target=ping, args=(live_contacts_canvas, username, my_contacts_canvas)).start()
    print('Ping has started.')

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
    message_config.grid_rowconfigure(0, weight=0)  # doesnt allow the message box to expand more than necesary, but leave empty space
    message_config.grid_columnconfigure(0, weight=1)
    input_config.grid(row=0, column=0)
    input_config.grid_configure(sticky='ew')
    message_config.grid_columnconfigure(1, weight=0)
    send_config.grid(row=0, column=1)
    send_config.grid_configure(sticky='ew')
    # added logo to program ---
    logocanvas = tk.Canvas(top_frameuser, width=round(window_width/100*30), height=round(window_height/100*10))
    logocanvas.pack()
    img = Image.open('Resources/logo.png')
    img = img.resize((round(window_width/100*25), round(window_height/100*10)), Image.ANTIALIAS)
    logo = ImageTk.PhotoImage(img)  # .convert('RGB') this mess' up with PNG files
    label = tk.Label(logocanvas, width=round(window_width/100*24), height=round(window_height/100*10), image=logo)
    label.image = logo
    label.pack()
    logo_underline = tk.Frame(top_frameuser, height=1, width=round(window_width/100*25), bg="black")
    logo_underline.pack()

    # child widgets in parent frames
    large_font = ('Verdana', 12)
    send_input = tk.Entry(input_config, font=large_font, border=0)
    send_input.insert(0, 'Enter Message Here...')
    send_input.pack(expand=True, fill='x')
    # send_input.grid(row=0, column=0)
    # send_input.grid_configure(sticky='nsew')

    my_contacts_listbox_creator(my_contacts_canvas)
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

    send_btn = tk.Button(send_config, text='Send', command=targetsend)  # want to use different channel for this, than communicating with server.
    send_btn.place(relx=0.5, rely=0.5, anchor=tk.CENTER)
    send_btn.config(width=round(window_width/100*10), height=round(window_height/100*10))
    contacts_underline = tk.Frame(my_contacts, height=1, width=round(window_width/100*25), bg="black")
    contacts_underline.pack()
    contacts = tk.Label(my_contacts, text='My Contacts')  # dynamic widget here..
    contacts.pack()
    live_contacts_canvas.pack(expand=True, fill='both')


class addFriend:
    def __init__(self, name, ip, livebox, add_friend_canvas, add_friend_button, my_contacts_canvas):
        self.ip = ip['text']
        self.name = name['text']
        self.txt_path = ''
        friend_path = os.path.join(chat_path, self.name)
        if not os.path.exists(friend_path):
            os.makedirs(friend_path)
            chat_log_txt_path = os.path.join(friend_path, name['text'] + '_chat.txt')
            self.txt_path = chat_log_txt_path
            messagetime = datetime.datetime.now().strftime("%H:%M")
            with open(chat_log_txt_path, 'w+') as file_creator:
                file_creator.write(f'Chat has been initaited @ {messagetime}')
        add_friend_button.destroy()
        text = tk.Label(add_friend_canvas, text='Added', font=('helvetica', 9, 'bold'))
        text.pack()
        my_contacts_listbox_creator(my_contacts_canvas)  # creates an additional box for this added user.
        # All users are added to the creator box initially already.

def object_pickler(object, name):
    friend_object.append(object)
    f = open(pickle_object_path, 'w+b')
    pickle.dump(friend_object, f)
    f.close()
    print(f' Friend Object List: {friend_object}')
    friends_added.append(name['text'])
    with open(pickle_friends_path, 'w+b') as f:
        pickle.dump(friends_added, f)
    print(f'Friends List {friends_added}')

def creator(name, ip, livebox, add_friend_canvas, add_friend_button, my_contacts_canvas):
    object_pickler(addFriend(name, ip, livebox, add_friend_canvas, add_friend_button, my_contacts_canvas), name)


def liveuserbox_creator(ip, name, isOnline, live_contacts_content, isUser, my_contacts_canvas):  # listbox creator function, need to find out how i can import live_contacts variable
    # need to add a button that adds this person to their friends list.
    # index checking to make sure we are not displaying same status again
    livebox_instances = len(live_contacts_content.winfo_children())-1  # how many user status boxes currently showing in panel...
    livebox = tk.Frame(live_contacts_content)
    if isOnline and not isUser:  # Will always be the case, useless condition.
        img = Image.open('Resources/online.png')
    elif not isOnline and not isUser:
        img = Image.open('Resources/offline.png')
    elif isOnline and isUser:
        img = Image.open('Resources/main_usr.png')
    ip = tk.Label(livebox, text=ip)
    ip.grid(row=0, column=0)
    name = tk.Label(livebox, text=name.title())
    name.grid(row=0, column=1)
    logocanvas = tk.Canvas(livebox, width=round(window_width / 100 * 5), height=round(window_height / 100 * 5))
    logocanvas.grid(row=0, column=2, padx=(5, 5))
    if not isUser:
        img = img.resize((10, 10), Image.ANTIALIAS)
    else:
        img = img.resize((15, 15), Image.ANTIALIAS)
    logo = ImageTk.PhotoImage(img)  # .convert('RGB') this mess' up with PNG files
    label = tk.Label(logocanvas, image=logo)
    label.image = logo
    label.pack()
    username = name['text']
    add_friend_canvas = tk.Canvas(livebox, width=20, height=20, background='white')
    if username in friends_added and not isUser:
        text = tk.Label(add_friend_canvas, text='Added', font=('helvetica', 9, 'bold'))
        text.pack()
    if not isUser and username not in friends_added:  # and username not in db_root['friends']
        add_friend_button = tk.Button(add_friend_canvas, text='Add', relief='flat', highlightthickness=0, borderwidth=1)
        add_friend_button.config(bg='green', fg='white', font=('helvetica', 9, 'bold'), command=lambda: creator(name, ip, livebox, add_friend_canvas, add_friend_button, my_contacts_canvas))
        add_friend_button.pack()
        add_friend_canvas.grid(row=0, column=3)
    livebox.pack(expand=True, fill='both')
    return live_contacts_content, livebox

def message_widget_creator(sentmessage, message_canvas):  # need to work on this...
    messagebox = tk.Frame(message_canvas, width=round(window_width / 100 * 70), height=10)
    message = tk.Label(messagebox, text=sentmessage)
    messagetime = datetime.datetime.now().strftime("%H:%M")
    date = tk.Label(messagebox, text=messagetime)
    print(f'Message Time: {messagetime}')
    date.pack(side='right')
    message.pack(side='right')
    messagebox.pack(side='top', anchor=tk.NE, expand=1, pady=5, fill=tk.X, )
    return messagetime, message

def message_listener(message_canvas, recieved_message):
    while True:
        pass
        # if client.recv(2048):  # problem is 2 functions cant intercept this message
            # message_received = client.recv(2048)
            # message will be a dictionary: {'ip':ip, 'time':time, 'message':'bunch of strings'}
            # time = recv_dict['time']
            # message = recv_dict['message']
            # message_handler(message_received, message_canvas, message, time)

def message_handler(message_recieved, message_canvas, message, messagetime):
    messagebox = tk.Frame(message_canvas, width=round(window_width / 100 * 70))
    message = tk.Label(messagebox, text=message_recieved)
    messagetime = datetime.datetime.now().strftime("%H:%M")
    date = tk.Label(messagebox, text=messagetime)
    print(f'Message Time: {messagetime}')
    date.pack(side='right')
    message.pack(side='right')
    messagebox.pack(side='top', anchor=tk.NW, expand=1, pady=5, fill=tk.X)


def merger(friends_added, friend_object, my_contacts_canvas)  # [03/05/2020] my_contacts_canvas needs to be given to this function.
    merged = zip(friends_added, friend_object)
    for x in merged:
        friend_name, friend_object_value = merged[x]
        actual_name = friend_object_value.ip
        actual_object = friend_object_value.name
        actual_path = friend_object_value.txt_path
        if friend_name != actual_name:
            print('There is probleming with syncing lists for merging, delete pickle files located in chat dir.')
            onclose(username=None)
        else:
            my_contacts_listbox_creator(my_contacts_canvas)
            # This needs to be double checked to make sure it is right... function listbox_creator needs to be reviewed.


# This needs to search added friends list automatically and look at objects list for cross reference.
def my_contacts_listbox_creator(my_contacts_canvas):  # Comment for debugging.
    print(friends_added)
    print(friend_object)
    for x in range(len(friend_object)):
        name = friend_object[x].name
        ip = friend_object[x].ip
        object_txt_path = friend_object[x].txt_path
        contactsbox = tk.Frame(my_contacts_canvas)
        if name in friends_added:
            ip = tk.Label(contactsbox, text=ip)
            ip.grid(row=0, column=0)
            name = tk.Label(contactsbox, text=name.title())
            name.grid(row=0, column=1)
            logocanvas = tk.Canvas(contactsbox, width=round(window_width / 100 * 5), height=round(window_height / 100 * 5))
            logocanvas.grid(row=0, column=2, padx=(5, 5))
            contactsbox.pack(expand=True, fill='both')

            # Want this function to be called at the start with known friends and then again when a friend is added...
# need to find out, how scrollbars and hidden widgets work
root.mainloop()

def onclose(username):
    print('Closing Program')
    root.destroy()
    print('Closing Connection')
    send(DISCONNECT_MESSAGE, username)
    client.close()
    exit(-1)
