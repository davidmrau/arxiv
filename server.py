import socket
import sys
from _thread import start_new_thread
import time 
import signal
import logging
import json 
import random

HOST = '192.168.178.178' # all availabe interfaces
PORT = 9090 # arbitrary non privileged port 

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((HOST, PORT))
server.listen(2)

print("Listening...")

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
img, img2 = 'img', 'img2'
start_new_thread(wait_for_connections, ())
clients = list()
queue = list()
while True:
    print(clients)
    clients = check_clients(clients)
    if len(clients) < 2:
        if len(queue) > 0:
            clients.append(queue.pop(0))
    img, img2 = img2, img
    img_list = [img, img2]
    for i, client in enumerate(clients):
        img_ = img_list[i]
        data = json.dumps({'name': 'David Rau', 'image_path' : f'{img_}.jpeg', 'window_name' : str(i)})
        send_message(client, data)
    time.sleep(5)
server.close()



