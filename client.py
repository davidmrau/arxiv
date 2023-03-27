
import socket
from _thread import start_new_thread
import json 
import time
import cv2
import threading
def receive(server):
    global data
    while True:
        data = server.recv(1024)
        if not data: 
            break
        # print the received message
        data = json.loads(data.decode('utf-8'))

def receive_message(server):
    global data

host = '192.168.178.178'

# Define the port on which you want to connect
port = 9090

server = socket.socket(socket.AF_INET,socket.SOCK_STREAM)

# connect to server on local computer
server.connect((host,port))

start_new_thread(receive, (server, ))

data = None 
while True:
    if data != None:
        image = cv2.imread(data["image_path"])
        #cv2.namedWindow("window", cv2.WND_PROP_FULLSCREEN)
        #cv2.setWindowProperty("window",cv2.WND_PROP_FULLSCREEN,cv2.WINDOW_FULLSCREEN)
        cv2.imshow(data["window_name"], image)
        if cv2.waitKey(50) == 13:
            break
#  cv2.destroyAllWindows()


