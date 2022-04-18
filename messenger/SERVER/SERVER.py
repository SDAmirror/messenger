import concurrent.futures
import json
import os
import socket
import ssl
import uuid
import logging
from concurrent.futures import ProcessPoolExecutor as Pool
# from pkg.message_processor import Message_Sender, Message_Recirver, Message_Processor
from pkg import message_processor
from pkg import connection_processor as con_procc
from collections import deque
from select import select
from pkg.MessageCtryptor import RSACryptor
from logger import Logging
from DB.models.message_model import MessageInfo

__basedir__ = os.path.dirname(os.path.realpath(__file__))
print(os.path.dirname(os.path.realpath(__file__)))
# postgres
# 123456
loger = 1

keypairs = {}
active_clients = {}
active_users = {}

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

def json_loader(data):
    return json.loads(data)

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
    user = None
    message_sender = message_processor.Message_Sender(cryptor)
    message_receiver = message_processor.Message_Recirver(cryptor)
    try:
        ress = cryptor.load_Public_key()
        if ress['key']==None:
            print("key not found") # ЭТО ОШИБКА тоже
            print(ress['errors'])

        key = ress['key'].save_pkcs1().decode('utf-8')
        yield 'send',client
        client.send(key.encode())
    except ConnectionResetError as e:
        print(f"client {id} disconnected")
        client.close()
        return

    try:
        yield 'recv',client
        public_key = client.recv(2048)

        key = message_receiver.recieve_message(id,public_key)
        cryptor.set_client_public_key(public_key)
    except ConnectionResetError as e:
        print(f"client {id} disconnected",e)
        client.close()
        return


    # con_procc = connection_processor.Connection_Processor(id,cryptor,logger)
    print('server')
    yield 'recv', client
    message = client.recv(2048)
    message = message_receiver.recieve_message(id, message)
    print(message)
    try:
        message = json_loader(message)

        # break
    except json.JSONDecodeError as e:
        print(e, 'auth data recieve error')
    except Exception as e:
        print(e, 'loader error')
    # while True:
    #     try:
    #
    #     except ConnectionResetError as e:
    #         print(f"client {id} disconnected")
    #         client.close()
    #         return
    #     except Exception as e:
    #         print('error asc',e)

    procedure = False
    if message['url'] == 'authentication':
        fn = con_procc.user_authentication
        future = pool.submit(fn, id, cryptor, logger, message)
        yield 'future', future
        ress = future.result()
        print(ress)

        connectionSuccessFlag = ress['flag']

        yield 'send', client
        resp = message_sender.send_message(id, ress['responce'])
        client.send(resp)
        user = ress['user']
    elif message['url'] == 'authorisation':
        fn = con_procc.user_authorisation
        future = pool.submit(fn, id, message_sender, logger, message)
        yield 'future', future
        ress = future.result()
        print(ress)

        connectionSuccessFlag = ress['flag']

        yield 'send', client
        resp = message_sender.send_message(id, ress['responce'])
        client.send(resp)
        user = ress['user']
    elif message['url'] == 'registration':
        procedure = True
        fn = con_procc.user_registration_part1
        future = pool.submit(fn, id, cryptor, logger, message)
        yield 'future', future
        ress = future.result()
        if ress['success']:
            user = ress['user']
            validation_res = False
            code_send_attempts = 3
            # while code_send_attempts > 0:
            #     fn = con_procc.user_registration_part2
            #     future = pool.submit(fn, id, cryptor, logger, user)
            #     yield 'future', future
            #     ress = future.result()
            #     if ress['success']:
            #         code = ress['code']
            #         attempts = 3
            #
            #         while attempts > 0:
            #             try:
            #                 message = client.recv(2048).decode()
            #
            #             except Exception as e:
            #                 print(f"error: {e}")
            #
            #             fn = con_procc.user_registration_part3
            #             future = pool.submit(fn,id, cryptor, logger, user,code,message)
            #             ress = future.result()
            #             if ress['success']:
            #                 if ress['validation']:
            #                     validation_res = True
            #                     break
            #                 else:
            #                     response = message_sender.send_message(id,f"invalid code, you have {attempts-1} more attemps")
            #                     client.send(response.encode())
            #             else:
            #                 client.send(ress['response'].encode())
            #
            #             attempts -= 1
            #
            #         code_send_attempts -= 1
            #         if validation_res:
            #             break
            #         else:
            #             response = message_sender.send_message(id,f"invalid code, we sent new code to your email")
            #             client.send(response.encode())
            # if validation_res:
            if True:
                fn = con_procc.user_registration_part4
                future = pool.submit(fn, id, cryptor, logger, user)
                yield 'future', future
                ress = future.result()
                if ress['success']:
                    connectionSuccessFlag = True
                    client.send(ress['response'].encode())
                else:
                    client.send(ress['response'].encode())
                    connectionSuccessFlag = False
            else:
                response_model = message_sender.send_message(id,json.dumps({"message": "registration failed","auth_success": False}))
                client.send(response_model)
        else:
            client.send(ress['response'])
            client.close()
            return



        future = pool.submit(fn, id, cryptor, logger, message)
        yield 'future', future
        ress = future.result()
        print(ress)

        connectionSuccessFlag = ress['flag']

        resp = message_sender.send_message(id,ress['responce'])
        yield 'send',client
        client.send(resp)
        user = ress['user']

    print('connect flag server ' ,connectionSuccessFlag)
    if not connectionSuccessFlag:
        active_clients.pop(id)
        client.close()
        cryptor.delete_RSA_keys()
        return

    active_users[user.username] = id

    while True:
        try:
            yield 'recv', client
            message = client.recv(2048)
            message = message_receiver.recieve_message(id,message)
            try:
                message = json_loader(message)
            except Exception as e:
                print(e,'message load error')
                #notify client that not sent
                continue
            print(message)
            future = pool.submit(message_processor.message_rpepare, message,user.username, logger)
            yield 'future', future
            ress = future.result()
            if ress['message'] != None:
                message = ress['message']
                if message.receiver in (active_users.keys()):
                    ress_id = active_users[message.receiver]
                    try:
                        message.id = str(message.id)
                        yield 'send',client
                        message_to_send = json.dumps({'message':message.__dict__})
                        active_clients[active_users[message.receiver]].send(message_sender.send_message(ress_id,message_to_send))

                        # active_clients[active_users[message.receiver]].send(json.dumps({'message':message.__dict__}).encode())
                        message.sent = True
                    except Exception as e:
                        print(e,'not sent to {}'.format(message.receiver))

                future = pool.submit(message_processor.message_processor, message,logger)
                yield 'future', future
                ress = future.result()

                if ress['created']:
                    response_model = json.dumps({'saved':True,'sent': message.sent})
                else:
                    response_model = json.dumps({'saved': False, 'sent': message.sent})

            try:
                prep_message = message_sender.send_message(id,response_model)
                yield 'send', client
                client.send(prep_message)
                # client.send(response_model.encode())
            except Exception as e:
                print('client disconnected', e)
                cryptor.delete_RSA_keys()
                client.close()
                break

        except ConnectionAbortedError as e:
            print(f'con error{e}')
            print(f"client {id} disconnected")
            client.close()
            cryptor.delete_RSA_keys()
            break
        except ConnectionResetError as e:
            print(f'con error{e}')
            print(f"client {id} disconnected")
            client.close()
            cryptor.delete_RSA_keys()
            break
        except Exception as e:
            print(f'con error{e}')
            print(f"client {id} disconnected")
            client.close()
            cryptor.delete_RSA_keys()
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
        while True:
            yield 'recv', sock
            client, addr = sock.accept()
            id = uuid.uuid4()
            # id = uuid.UUID('4913d052-26ab-47d3-b3fe-968be8f52980')
            print(f"[+] {client} connected with id {id}")
            logger.log(logging.INFO,"[+] {client} connected with id {id}")
            active_clients[id] = client
            tasks.append(client_handler(client, id))


tasks.append(base_server(('localhost', 4430)))

if __name__ == '__main__':
    try:
        print("run")
        run()
    except KeyboardInterrupt as e:
        print("keybord interupted",e)
