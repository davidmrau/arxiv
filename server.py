import socket
import sys
from _thread import start_new_thread
import time 
import signal
import logging
import json 
import random
from utils import git_push
import os
import re
hostname = socket.gethostname()
HOST = socket.gethostbyname(hostname)
#HOST = '192.168.178.100' # all availabe interfaces
PORT = 7777 # arbitrary non privileged port 

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((HOST, PORT))
server.listen(2)

print("Listening...")

def write(text, sleep=0.1):
    for i in text:
        time.sleep(sleep)
        print(i, end='', flush=True)

def client_thread(conn):
    conn.send("Welcome to the Server. Type messages and press enter to send.\n".encode('utf-8'))


def is_socket_closed(sock: socket.socket) -> bool:
    try:
        # this will try to read bytes without blocking and also without removing them from buffer (peek only)
        data = sock.recv(16, socket.MSG_DONTWAIT | socket.MSG_PEEK)
        if len(data) == 0:
            return False
    except BlockingIOError:
        return True  # socket is open and reading from it would block
    except ConnectionResetError:
        return False  # socket was closed for some other reason
    except Exception as e:
        logger.exception("unexpected exception when checking if a socket is closed")
        return True
    return True

def check_clients(clients):
    return list(filter(is_socket_closed, clients))

def wait_for_connections():
    global queue 
    while True:
        # blocking call, waits to accept a connection
        client, addr = server.accept()
        print("[-] Connected to " + addr[0] + ":" + str(addr[1]))
        queue.append(client)

def send_message(client, data):
    client.sendall(bytes(data,encoding="utf-8"))

def get_files(artworks_folder):
    file_list = [ f for f in os.listdir(artworks_folder) if f.endswith('.jpeg')]
    return file_list

def decode_file(file_name):
    pattern = r"((?:[^_]+_)+\d+)_((?:[^_]+_)+\d+)\.jpeg"
    matches = re.match(pattern, file_name)
    name_1 = '_'.join(matches.group(1).split('_')[:-1])
    name_2 = '_'.join(matches.group(2).split('_')[:-1])
    return name_1, name_2

def decode_name(name_sep):
    return name_sep.replace('_', ' ').title()

def write_data(name1, name2, img_path, file):
    with open(file, 'a') as f:
        data = {'name1': name1, 'name2': name2, 'img': img_path}
        data_json = json.dumps(data)
        f.write(data_json + '\n')

start_new_thread(wait_for_connections, ())
clients = list()
queue = list()

data_path = 'data.jsonl'
portraits_folder = 'portraits'
artworks_folder = 'data'

files = get_files(artworks_folder)
random.shuffle(files)
files_iter = iter(files)

while True:
    try:
        #print(clients)
        clients = check_clients(clients)
        if len(clients) < 2:
            if len(queue) > 0:
                clients.append(queue.pop(0))

        # get next file
        try:
            artwork_file = next(files_iter)
        except StopIteration:
            random.shuffle(files)
            files_iter = iter(files)

        artist_1, artist_2 = decode_file(artwork_file)

        portrait_1 = f'{portraits_folder}/{artist_1}_ascii.jpeg-full.png'
        portrait_2 = f'{portraits_folder}/{artist_2}_ascii.jpeg-full.png'
        portraits = [portrait_1, portrait_2]

        names = [decode_name(artist_1), decode_name(artist_2)]

        os.system('clear')
        write(f"Generating new speculative artwork between {names[0]} and {names[1]}...")
        time.sleep(3)
        time.sleep(1)
        for i, client in enumerate(clients):
            img_ = portraits[i]
            name = names[i]
            data = json.dumps({'name': name , 'image_path' : f'{img_}.jpeg', 'window_name' : str(i)})
            send_message(client, data)
        #os.system(f'fbi -t 4.5 -1 {artworks_folder}/{artwork_file}')
        start_new_thread(write_data, (names[0], names[1], f'{artworks_folder}/{artwork_file}', data_path))
        #start_new_thread(git_push, ())
    except KeyboardInterrupt:
        sys.exit(0)
    except Exception as e:
        print(f'Failed: {e}')
        pass
server.close()



