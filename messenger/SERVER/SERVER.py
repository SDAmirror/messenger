# import socket
# import json
# from threading import Thread
#
# # server's IP address
# SERVER_HOST = "localhost"
# SERVER_PORT = 5002 # port we want to use
# separator_token = "<SEP>" # we will use this to separate the client name & message
#
# # initialize list/set of all connected client's sockets
# client_sockets = {} # TODO database of clients/ session
# client_DB = {}
#
# # create a TCP socket
# s = socket.socket()
# # make the port as reusable port
# s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
# # bind the socket to the address we specified
# s.bind((SERVER_HOST, SERVER_PORT))
# # listen for upcoming connections
# s.listen(5)
# print(f"[*] Listening as {SERVER_HOST}:{SERVER_PORT}")
#
#
# def listen_for_client(cs):
#     """
#     This function keep listening for a message from `cs` socket
#     Whenever a message is received, broadcast it to all other connected clients
#     """
#     while True:
#         try:
#             # keep listening for a message from `cs` socket
#             msg = cs.recv(1024).decode()
#         except Exception as e:
#             # client no longer connected
#             # remove it from the set
#             print(f"[!] Error: {e}")
#             for key, value in dict(client_sockets).items():
#                 if value == cs:
#                     del client_sockets[key]
#         else:
#             # if we received a message, replace the <SEP>
#             # token with ": " for nice printing
#             msg = msg.replace(separator_token, ": ")
#         # iterate over all connected sockets'
#         messParts = msg.split('----')
#         client_sockets[messParts[1]].send(msg.encode())


#
#
# while True:
#     # we keep listening for new connections all the time
#     client_socket, client_address = s.accept()
#     print(client_socket)
#
#     print(f"[+] {client_address} connected.")
#     so = client_socket.fileno()
#
#     print("{} :: :: {}".format(type(so), so))
#     ss = socket.fromfd( so,socket.AF_INET, socket.SOCK_STREAM)
#     client_socket.close()
#     print(ss)
#     # add the new connected client to connected sockets
#     try:
#         un = ss.recv(1024).decode()
#         client_sockets[un]=ss
#
#     except Exception as e:
#         # client no longer connected
#         # remove it from the set
#         print(f"[!] Error: {e}")
#
#     # start a new thread that listens for each client's messages
#     t = Thread(target=listen_for_client, args=(ss,))
#     # make the thread daemon so it ends whenever the main thread ends
#     t.daemon = True
#     # start the thread
#     t.start()
#
#
# # close client sockets
# for key in list(client_sockets.keys()):
#     client_sockets[key].close()
# # close server socket
# s.close()


#-------------------------------------------------------------------------------------------------------------------
import socket
import uuid
import json
import DB.database as db
#postgres
#123456

from socket import *
from concurrent.futures import ProcessPoolExecutor as Pool

from collections import deque
from select import select

clients = {}

tasks = deque()
pool = Pool(10)
recv_wait = {}
send_wait = {}
future_wait = {}

future_notify,future_event = socketpair()
def future_done(future):
    tasks.append(future_wait.pop(future))
    future_notify.send(b'x')
def future_monitor():
    while True:
        yield 'recv',future_event
        future_event.recv(1024)
tasks.append(future_monitor())
class somestruct:
    def __init__(self,client,id):
        self.client = client
        self.id = id

def message_processor(n):
    return 1


def run():

    while any([tasks,recv_wait,send_wait]):
        while not tasks:
            can_recv,can_send,[] = select(recv_wait,send_wait,[])
            for s in can_recv:
                tasks.append(recv_wait.pop(s))
            for s in can_send:
                tasks.append(send_wait.pop(s))
        task = tasks.popleft()
        try:
            why,what = next(task)
            if why == 'recv':
                #penalty box
                recv_wait[what] = task
            elif why == 'send':
                send_wait[what] = task
            elif why == 'future':
                future_wait[what] = task
                what.add_done_callback(future_done)
            else:
                raise RuntimeError("some error")
        except StopIteration:
            print('task done')

def client_handler(client):
    while True:
        yield'recv',client

        #TODO try catch if client disconnected then delete this socket
        #message handle
        message = client.recv(1024).decode()
        if not message:
            break


        future = pool.submit(message_processor, message)
        yield 'future',future
        result = future.result()
        # result = fib(n)
        resp = str(result).encode()
        yield 'send',client
        try:
            client.send(resp)
        except:
            print('cleint disconnected')
    print('closed')





def connection_processor(message):


    data = json.loads(message)


    {
        "case":"authorization,authentification,registration,recovery",
        "authentification_check": True,
        "authentification_token": "",
        "authorization_check": True,
        "authorization_data": ["username","password"],
        "authentification_token": "",
        "authentification_token": "",
    }

    def authentification_token_validation(token, username):
        # table authentication session
        # get by username
        # if rows not null
            #if token valid return True

        pass


    if not data['authentification_check']:
        token = data["authentification_token"]
        username = data["authorization_data"][0]
        #check if token valid for this user
        if authentification_token_validation(token,username):
            profile = {"messages":[{},{},{}],"friends":[]}
            return "authentication success"+json.dumps(profile)
        else:
            return "authentication failed"

    id
    """
    
    кейс 1
        я такой клиент ,я  не зарегестрирован, я хочу новый аккаунт
            форма регистрации
    кейс 2
        я зарегестрирован вот мои аторизационные данные
            проверить аторизационные данные
    кейс 3 
        я авторизован вот мой аутентификатор/токен private.key .crt
            вернуть информацию
    кейс 4
        я забыл пароль
            аутентификация        
            
    authentification_check: 
    authorization_check: 
    authentification_token: token
    authorization: [username,password]
    """



def base_server(address):
    sock = socket(AF_INET, SOCK_STREAM)
    sock.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
    sock.bind(address)
    sock.listen(5)
    print('connected')
    while True:
        yield 'recv',sock
        client, addr = sock.accept()
        message = client.recv(1024).decode()
        connection_processor(message)
        #{"username": "username","authSessionID": "id"}

        data = sock.recv(1024).decode('utf-8')  # this returns a JSON-formatted String
        #TODO function that starts cliebnt at connection.
        parsed_data = json.loads(data)
        id = uuid.UUID
        print(f"[+] {client} connected.")
        clients[id] =client
        # t = Thread(target=fib_handler,args=(client,),daemon=True)
        # t.start()
        # fib_handler(client)
        tasks.append(client_handler(client))





tasks.append(base_server(('localhost', 8888)))

if __name__ == '__main__':
    run()



#postgresql cursor

# 20000-50000

#while online
    # cursor work
#