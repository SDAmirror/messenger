import socket
import random
import ssl
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
SERVER_PORT = 4430 # server's port
separator_token = "<SEP>" # we will use this to separate the client name & message

def listen_for_messages():
    while True:
        message = s.recv(1024).decode()
        if not message:
            print("closed")
            break
        print("\n" + message)


# context = ssl.create_default_context()
#
# with socket.create_connection((SERVER_HOST, 443)) as sock:
#     with context.wrap_socket(sock, server_hostname=SERVER_HOST,ssl_version=ssl.PROTOCOL_TLSv1, ciphers="ADH-AES256-SHA") as s:
# print(s.version())
#
# prompt the client for a name
# make a thread that listens for messages to this client & print them

s = ssl.wrap_socket(socket.socket())
s.connect((SERVER_HOST, SERVER_PORT))
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

    s.send(to_send.encode())

# close the socket
s.close()


