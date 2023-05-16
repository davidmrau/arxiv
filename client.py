import socket
from _thread import start_new_thread
import json
import time
import os
def receive(server):
    global data

def receive_message(server):
    global data

host = '192.168.178.108'

# Define the port on which you want to connect
port = 7777

server = socket.socket(socket.AF_INET,socket.SOCK_STREAM)




def connect_to_server():
# connect to server on local computer
    while True:
        try:
            server.connect((host,port))
            print(f'Connected to server: {host}:{port}')
            start_new_thread(receive, (server, ))
            break
        except:
            print(f'Could not connect to server: {host}:{port}')
        time.sleep(3)


connect_to_server()

data = None

while True:
    try:
        data = server.recv(1024)
        if not data:
            connect_to_server()
        data = json.loads(data.decode('utf-8'))
        image_path = data["image_path"]
        os.system('fbi -t 4.5 -1 {image_path}.jpeg')
    except:
        pass
