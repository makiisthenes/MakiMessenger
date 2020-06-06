import pickle, os, shutil


def server_ip_reader():
    current_path = os.getcwd()
    server_pickle_path = os.path.join(current_path, r'..\ProgramData\server_ip.txt')
    print(server_pickle_path)
    # with open(r"..\ProgramData\server.pickle") as
    exists = os.path.exists(server_pickle_path)
    print(exists)
    if not exists:
        with open(server_pickle_path, 'w') as file:
            return False
    else:
        print("Server IP text file exists")
        with open(server_pickle_path, 'r') as file:
            row = file.readline()
            print(row)
            return row

def server_ip_writer(ip):
    current_path = os.getcwd()
    server_pickle_path = os.path.join(current_path, r'..\ProgramData\server_ip.txt')
    exists = os.path.exists(server_pickle_path)
    # print(exists)
    if not exists:
        with open(server_pickle_path, 'w') as file:
            return False
    else:
        # print("Server IP text file exists")
        with open(server_pickle_path, 'w+') as file:
            file.write(ip)
