#-------------------------------------------------------------------------------------------------------------------
import queue
import socket
import uuid
from socket import *
from concurrent.futures import ProcessPoolExecutor as Pool
from collections import deque
from collections import deque
from select import select
from pkg.connection_processor import connection_processor
#postgres
#123456





active_clients = {}

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
##fibtype
def message_processor(message):
    return 44124


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
def client_handler(client,id):
    while True:
        yield'recv',client

        #TODO try catch if client disconnected then delete this socket
        #message handle
        try:
            message = client.recv(1024).decode()
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
        except ConnectionResetError as e:
            print(f"client {id} disconnected")


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


        connection_processor(client)

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