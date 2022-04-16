import socket
import ssl
from threading import Thread
import json

import message_processor
from  MessageCtryptor import RSACryptor

def listen_for_messages():
    while True:

        message = s.recv(2048).decode()
        {
            'sender': 'client',  # 'sender':'server'
            'keys': True,
            'data': {'message': 'wadawd', 'username': 'user1'}  # dawdawdwdawdawdawdawdw
        }
        # database check if user exist
        # check keys
        # if keys ok:
        #   send message
        # else:
        #   renew keys

        #database
        #save to database ()
        if not message:
            print("closed")
            break
        print("\n" + message)


SERVER_HOST = "localhost"
SERVER_PORT = 4430
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
    "url": "registration",
    # "authentification_check": False,
    "authentification_token": "d3a5f6cb-01a8-4bff-b076-64550ff85921",
    # "authorization_check": False,
    "authorization_data": ["user1", "password1"],
    "registration_data": {
        "username": "usery3333w",
        "password": "password3",
        "first_name": "first_name3",
        "last_name": "last_name3",
        "email": "myvideoboxdsa@gmail.com"
    }
}).encode())
print("sent")
m = s.recv(2048).decode()

print(m, 'recived')
mess = json.loads(str(m))
print(mess)
if mess['auth_success']:
    print(mess['AuthenticationUser'])

    # make a thread that listens for messages to this client & print them
    t = Thread(target=listen_for_messages)
    # make the thread daemon so it ends whenever the main thread ends
    t.daemon = True
    # start the thread
    t.start()

    while True:

        to_send = input('message')

        # database check if user exist
        # check keys
        # if keys ok:
        #   send message
        # else:
        #   renew keys
        if to_send == '':
            to_send = '1'
        if to_send.lower() == 'q':
            s.close()
            break
        username = input('username')
        message = {}

        s.send(to_send.encode())
else:
    print("failed")
    s.close()




# close the socket
s.close()
