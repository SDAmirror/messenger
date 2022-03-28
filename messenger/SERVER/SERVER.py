#-------------------------------------------------------------------------------------------------------------------
import concurrent.futures
import socket
import uuid
from socket import *
from concurrent.futures import ProcessPoolExecutor as Pool

from collections import deque
from select import select
from pkg.connection_processor import connection_processor
#postgres
#123456





active_clients = {}

tasks = deque()
pool = Pool(10)
concurrent.futures.wait(tasks)
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
        #change
        future_event.recv(1024)
tasks.append(future_monitor())
class somestruct:
    def __init__(self,client,id):
        self.client = client
        self.id = id

##fibtype
def message_processor(message):
    return 44124


def run():

    while any([tasks,recv_wait,send_wait]):
        empty_tasks =True
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
                print(e,'len error qoq')


        try:
            task = tasks.pop()
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
                print('i"m waiting')
                continue
        except StopIteration:
            print('task done')
            continue

def client_handler(client,id):

    future = pool.submit(connection_processor,client)
    yield 'future', future
    connectionSuccessFlag = future.result()
    print(connectionSuccessFlag)
    if not connectionSuccessFlag:
        active_clients.pop(id)
        client.close()
        return

    while True:


        #TODO try catch if client disconnected then delete this socket
        #message handle
        try:
            yield 'recv', client
            message = client.recv(1024).decode()
            print(message)
            if not message:
                break

            future = pool.submit(message_processor, message)
            yield 'future', future
            result = future.result()
            # result = fib(n)
            resp = str(result).encode()
            yield 'send', client
            try:
                client.send(resp)
            except Exception as e:
                print('cleint disconnected', e)
                client.close()
                break
        except ConnectionResetError as e:
            print(f"client {id} disconnected")
            client.close()
            break


    print('closed')












def base_server(address):
    sock = socket(AF_INET, SOCK_STREAM)
    sock.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
    sock.bind(address)
    sock.listen(5)
    print('connected')
    while True:
        yield 'recv',sock
        client, addr = sock.accept()
        id = uuid.uuid4()
        print(f"[+] {client} connected with id {id}")
        active_clients[id] =client
        # t = Thread(target=fib_handler,args=(client,),daemon=True)
        # t.start()
        # fib_handler(client)
        tasks.append(client_handler(client,id))






tasks.append(base_server(('localhost', 8888)))

if __name__ == '__main__':
    run()



#postgresql cursor

# 20000-50000

#while online
    # cursor work
#