import socket
import random
import ssl
import sys
from threading import Thread
from datetime import datetime
from colorama import Fore, init
import json

# init colors
import message_processor
from  MessageCtryptor import RSACryptor

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
SERVER_PORT = 4430  # server's port
separator_token = "<SEP>"  # we will use this to separate the client name & message

cryptor = RSACryptor(1)
cryptor.generate_RSA_keys()

message_sender = message_processor.Message_Sender(cryptor)
message_receiver = message_processor.Message_Recirver(cryptor)

s = ssl.wrap_socket(socket.socket())
s.connect((SERVER_HOST, SERVER_PORT))

print("[+] Connected.")
try:
    server_public_key = s.recv(2048).decode()
    cryptor.set_server_public_key(server_public_key)
except ConnectionResetError as e:
    print(f"client {id} disconnected")
    s.close()
try:
    key = message_sender.send_message(1,cryptor.load_Public_key()['key'].save_pkcs1().decode('utf-8'))
    s.send(key.encode())
except ConnectionResetError as e:
    print(f"client {id} disconnected")
    s.close()



s.send(json.dumps({
    "url": "authorisation",
    "authentification_check": False,
    "authentification_token": "d3a5f6cb-01a8-4bff-b076-64550ff85921",
    "authorization_check": False,
    "authorization_data": ["user1", "password1"],
    # "registration_data": {
    #     "username": "useryw",
    #     "password": "password3",
    #     "first_name": "first_name3",
    #     "last_name": "last_name3",
    #     "email": "flamehst@mail.ru"
    # }
}).encode())
print("sent")
m = s.recv(2048).decode()

print(m, 'recived')
mess = json.loads(str(m))
print(mess)
if mess['auth_success']:
    print(mess['AuthenticationUser'])
else:
    print("failed")
    s.close()

def listen_for_messages():
    while True:
        message = s.recv(2048).decode()
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
    if to_send == '':
        to_send = '1'
    if to_send.lower() == 'q':
        s.close()
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
