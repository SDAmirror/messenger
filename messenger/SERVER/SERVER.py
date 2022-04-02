# -------------------------------------------------------------------------------------------------------------------
import concurrent.futures
import socket
import ssl
import uuid
import rsa
import logging
from concurrent.futures import ProcessPoolExecutor as Pool
# from pkg.message_processor import Message_Sender, Message_Recirver, Message_Processor
from pkg import message_processor
from pkg import connection_processor
from collections import deque
from select import select
from pkg.MessageCtryptor import RSACryptor
from logger import Logging

# postgres
# 123456
loger = 1

keypairs = {}
active_clients = {}

tasks = deque()
pool = Pool(10)
concurrent.futures.wait(tasks)
recv_wait = {}
send_wait = {}
future_wait = {}

future_notify, future_event = socket.socketpair()


def future_done(future):
    tasks.append(future_wait.pop(future))
    future_notify.send(b'x')


def future_monitor():
    while True:
        yield 'recv', future_event
        # change
        future_event.recv(1024)


tasks.append(future_monitor())

logger_temp=Logging()
logger = logger_temp.logger



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
    global logger
    logger.log(logging.INFO,'creation of server keys')
    cryptor = RSACryptor(id)
    cryptor.generate_RSA_keys()
    try:
        ress = cryptor.load_Public_key()
        if ress['key']==None:
            print("key not found") # ЭТО ОШИБКА тоже
            print(ress['errors'])

        key = ress['key'].save_pkcs1().decode('utf-8')

        client.send(key.encode())
    except ConnectionResetError as e:
        print(f"client {id} disconnected")
        client.close()

    try:

        public_key = client.recv(1024).decode()
        cryptor.set_client_public_key(public_key)
    except ConnectionResetError as e:
        print(f"client {id} disconnected")
        client.close()

    message_sender = message_processor.Message_Sender(cryptor)
    message_receiver = message_processor.Message_Recirver(cryptor)
    # pub = create_keys(id)
    # priv,pub
    # prive,pub file write.
    # 'priv'+str(id)+'.pem'
    # 'pub'+str(id)+'.pem'
    # client.send(pub)


    future = pool.submit(connection_processor.connection_processor, client, id, cryptor,logger)
    yield 'future', future
    connectionSuccessFlag = future.result()
    print(connectionSuccessFlag)
    if not connectionSuccessFlag:
        active_clients.pop(id)
        client.close()
        return

    while True:

        # TODO try catch if client disconnected then delete this socket
        # message handle
        try:
            yield 'recv', client
            message = client.recv(1024).decode()
            print(message)

            future = pool.submit(message_processor.message_processor, message,logger)
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
    logger.log(logging.INFO,'creation of base server')
    context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
    context.load_cert_chain('server.crt', 'server.key', password='firstkey')

    ssock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    ssock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    ssock.bind(address)
    ssock.listen(5)
    with context.wrap_socket(ssock, server_side=True) as sock:
        print('got')

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


tasks.append(base_server(('localhost', 4430)))

if __name__ == '__main__':
    run()

# postgresql cursor

# 20000-50000

# while online
# cursor work
#
