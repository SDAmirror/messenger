# -------------------------------------------------------------------------------------------------------------------
import concurrent.futures
import socket
import ssl
import uuid
import rsa
from socket import *
from concurrent.futures import ProcessPoolExecutor as Pool
from pkg.message_processor import Message_Sender, Message_Recirver, Message_Processor
from pkg import message_processor
from pkg import connection_processor
from collections import deque
from select import select
from pkg.MessageCtryptor import RSACryptor

# postgres
# 123456

keypairs = {}
active_clients = {}

tasks = deque()
pool = Pool(10)
concurrent.futures.wait(tasks)
recv_wait = {}
send_wait = {}
future_wait = {}

future_notify, future_event = socketpair()


def future_done(future):
    tasks.append(future_wait.pop(future))
    future_notify.send(b'x')


def future_monitor():
    while True:
        yield 'recv', future_event
        # change
        future_event.recv(1024)


tasks.append(future_monitor())


class somestruct:
    def __init__(self, client, id):
        self.client = client
        self.id = id


##fibtype


def run():
    while any([tasks, recv_wait, send_wait]):
        empty_tasks = True
        while not any([tasks, recv_wait, send_wait]):
            pass
        while not tasks:
            try:
                can_recv, can_send, [] = select(recv_wait, send_wait, [])
                for s in can_recv:
                    tasks.append(recv_wait.pop(s))
                for s in can_send:
                    tasks.append(send_wait.pop(s))
            except Exception as e:
                print(e, 'len error qoq')

        try:
            task = tasks.pop()
            why, what = next(task)
            if why == 'recv':
                # penalty box
                recv_wait[what] = task
            elif why == 'send':
                send_wait[what] = task
            elif why == 'future':
                future_wait[what] = task
                what.add_done_callback(future_done)
            else:
                print('i"m waiting')
                continue
        except StopIteration:
            print('task done')
            continue


def client_handler(client, id):
    cryptor = RSACryptor(id)

    # pub = create_keys(id)
    # priv,pub
    # prive,pub file write.
    # 'priv'+str(id)+'.pem'
    # 'pub'+str(id)+'.pem'
    # client.send(pub)

    future = pool.submit(connection_processor.connection_processor, client, id, cryptor)
    yield 'future', future
    connectionSuccessFlag = future.result()
    print(connectionSuccessFlag)
    if not connectionSuccessFlag:
        active_clients.pop(id)
        client.close()
        return
    # recirver = Message_Recirver
    # sender = Message_Sender
    while True:

        # TODO try catch if client disconnected then delete this socket
        # message handle
        try:
            yield 'recv', client
            message = client.recv(1024).decode()
            print(message)

            future = pool.submit(message_processor.message_processor, message)
            yield 'future', future
            result = future.result()

            resp = str(result).encode()

            yield 'send', client
            try:
                client.send(resp)
            except Exception as e:
                print('client disconnected', e)
                client.close()
                break
        except ConnectionResetError as e:
            print(f"client {id} disconnected")
            client.close()
            break

    print('closed')


def base_server(address):
    context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
    context.load_cert_chain('server.crt', 'server.key', password='firstkey')

    ssock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    ssock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    ssock.bind(address)
    ssock.listen(5)
    with context.wrap_socket(ssock, server_side=True) as sock:
        #
        # sock = socket(AF_INET, SOCK_STREAM)
        # sock.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
        # sock.bind(address)
        # sock.listen(5)
        # print('connected')
        while True:
            yield 'recv', sock
            client, addr = sock.accept()
            id = uuid.uuid4()
            print(f"[+] {client} connected with id {id}")
            active_clients[id] = client
            # t = Thread(target=fib_handler,args=(client,),daemon=True)
            # t.start()
            # fib_handler(client)
            tasks.append(client_handler(client, id))


tasks.append(base_server(('localhost', 8888)))

if __name__ == '__main__':
    run()

# postgresql cursor

# 20000-50000

# while online
# cursor work
#
