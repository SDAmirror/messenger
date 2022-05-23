import datetime
import socket
import ssl
import time
from threading import Thread
import json
import message_processor
from  MessageCtryptor import RSACryptor


def listen_for_messages():
    while True:

        # message = s.recv(2048).decode()
        message = s.recv(2048)
        message = message_receiver.recieve_message(1,message)
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
        print(message)


SERVER_HOST = "172.20.10.8"
SERVER_HOST = "localhost"
# SERVER_HOST = "192.168.76.217"
SERVER_PORT = 4430

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
    key = message_sender.send_message(1,cryptor.load_Public_key()['key'].save_pkcs1())
    s.send(key)
except ConnectionResetError as e:
    print(f"client {id} disconnected")
    s.close()

cou = 3
while True:
    s.send(message_sender.send_message(1,json.dumps({
        "auth_check":1,
        "url": "authorization",
        # "authentification_check": False,
        "authentification_token": "d3a5f6cb-01a8-4bff-b076-64550ff85921",
        # "authorization_check": False,
        "authorization_data": ["user3", "password3"],
        "registration_data": {
            "username": "555666",
            "password": "passwordww3",
            "first_name": "first_name3",
            "last_name": "last_name3",
            # "email": "myvideoboxdsa@gmail.com"
            "email": "d.sadykov@astanait.edu.kz"
            # "email": "gulnur.kst@gmail.com"
        }
    })))
    m = s.recv()
    status = json.loads(message_receiver.recieve_message(1,m))
    if status['auth_data_exchange']:
        break
    else:
        cou -=1
        if status['error']==50401:
            print('data sent unsuccessful')
#
#
# while True:
#     code=input('code')
#     if code == "q":break
#     s.send(message_sender.send_message(1,code))
#     print("sent")
#     m = s.recv(2048)
#     m = message_receiver.recieve_message(1, m)
#     print(m)

print("sent")
m = s.recv(2048)
m = message_receiver.recieve_message(1, m)

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
        message = {'reciever':username, 'body': to_send, 'send_date': str(datetime.date.today()),'send_time':datetime.datetime.now().strftime("%H:%M:%S") }




        s.send(message_sender.send_message(1,json.dumps(message)))
        # s.send(json.dumps(message).encode())
else:
    print("failed")
    s.close()


s.close()
