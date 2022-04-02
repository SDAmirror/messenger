import socket
import random
import sys
from threading import Thread
from datetime import datetime
from colorama import Fore, init
import json

# init colors
init()
# set the available colors
colors = [Fore.BLUE, Fore.CYAN, Fore.GREEN, Fore.LIGHTBLACK_EX,
          Fore.LIGHTBLUE_EX, Fore.LIGHTCYAN_EX, Fore.LIGHTGREEN_EX,
          Fore.LIGHTMAGENTA_EX, Fore.LIGHTRED_EX, Fore.LIGHTWHITE_EX,
          Fore.LIGHTYELLOW_EX, Fore.MAGENTA, Fore.RED, Fore.WHITE, Fore.YELLOW
          ]

# choose a random color for the client
client_color = random.choice(colors)

# server's IP address
# if the server is not on this machine, 
# put the private (network) IP address (e.g 192.168.1.2)
SERVER_HOST = "localhost"
SERVER_PORT = 8888  # server's port
separator_token = "<SEP>"  # we will use this to separate the client name & message

# initialize TCP socket
s = socket.socket()
print(f"[*] Connecting to {SERVER_HOST}:{SERVER_PORT}...")
# connect to the server
s.connect((SERVER_HOST, SERVER_PORT))
print("[+] Connected.")

# prompt the client for a name

s.send(json.dumps({
    "connection_case": "registration",
    "authentification_check": False,
    # "authentification_token": "7498317b-5fea-4692-b74c-d64a7b0d4861",
    "authorization_check": True,
    "authorization_data": ["user1", "password1"],
    "registration_data": {
        "username": "useryw",
        "password": "password3",
        "first_name": "first_name3",
        "last_name": "last_name3",
        "email": "flamehst@mail.ru"
    }
}).encode())
print("sent")
m = s.recv(1024).decode()

print(m, 'recived')
mess = json.loads(str(m))
print(mess)
if mess['auth_success']:
    print(mess['AuthenticationUser'])
else:
    print("failed")

def listen_for_messages():
    while True:
        message = s.recv(1024).decode()
        if not message:
            print("closed")
            break
        print("\n" + message)


# make a thread that listens for messages to this client & print them
t = Thread(target=listen_for_messages)
# make the thread daemon so it ends whenever the main thread ends
t.daemon = True
# start the thread
t.start()

while True:
    # input message we want to send to the server
    to_send = input()
    if to_send.lower() == 'q':
        break
    # try:
    #     to_send = int(to_send)
    #     if to_send == 1:
    #         s.send("dawdaw daw")
    #     elif to_send == 2:
    #         with open("C:/Users/flame/Desktop/students/",'rb') as f:
    #
    #
    #     elif to_send == 3:
    #         pass
    #     else:
    #         pass
    #
    # except Exception as e:
    #     print(to_send)
    #     # a way to exit the program
    #     # add the datetime, name & the color of the sender
    #     date_now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    #     to_send = f"{client_color}[{date_now}]{separator_token}{to_send}"
    #     # finally, send the message
    s.send(to_send.encode())

# close the socket
s.close()
