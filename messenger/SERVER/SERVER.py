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
context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)


def future_done(future):
    tasks.append(future_wait.pop(future))
    future_notify.send(b'x')


def future_monitor():
    while True:
        yield 'recv', future_event
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
            # try:
            can_recv, can_send, [] = select(recv_wait, send_wait, [])
            for s in can_recv:
                tasks.append(recv_wait.pop(s))
            for s in can_send:
                tasks.append(send_wait.pop(s))
            # except Exception as e:
            #     print(e, 'len error qoq')

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
    connectionSuccessFlag = False
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
        cryptor.set_client_public_key(public_key)
    except ConnectionResetError as e:
        print(f"client {id} disconnected",e)
        client.close()
        return


    # con_procc = connection_processor.Connection_Processor(id,cryptor,logger)
    print('server keys exhcanged')
    # yield 'recv', client
    # message = client.recv(2048)
    # message = message_receiver.recieve_message(id, message)
    # print(message)
    # try:
    #     message = json_loader(message)
    # except json.JSONDecodeError as e:
    #     print(e, 'auth data recieve error')
    # except Exception as e:
    #     print(e, 'loader error')
    authdatacounter = 0
    attempcounter = 1
    while True:
        if attempcounter > 5:
            connectionSuccessFlag = False
            break
        while True:
            try:
                yield 'recv', client
                message = client.recv(2048)
                message = message_receiver.recieve_message(id, message)
                print(message)
                try:
                    message = json_loader(message)
                    try:
                        if 'auth_check' in list(message.keys()):
                            client.send(message_sender.send_message(id,json.dumps({"auth_data_exchange":True,'error':0})))
                            break
                        else:
                            client.send(message_sender.send_message(id,json.dumps({"auth_data_exchange":False,'error':50401})))
                    except ConnectionResetError as e:
                        print('error asc', e)
                        print(f"client {id} disconnected")
                        client.close()
                        return

                except json.JSONDecodeError as e:
                    print(e, 'auth data recieve error')
            except ConnectionResetError as e:
                print('error asc', e)
                print(f"client {id} disconnected")
                active_clients.pop(id)
                client.close()
                cryptor.delete_RSA_keys()
                return
            except Exception as e:
                print('error asc', e)
                break
                # print(f"client {id} disconnected")
                # active_clients.pop(id)
                # client.close()
                # cryptor.delete_RSA_keys()
                # return




            authdatacounter +=1
            if authdatacounter >6:
                active_clients.pop(id)
                client.close()
                cryptor.delete_RSA_keys()
                return


        procedure = False

        if message['url'] == 'authentication':
            fn = con_procc.user_authentication
            future = pool.submit(fn, id, cryptor, logger, message)
            yield 'future', future
            ress = future.result()


            connectionSuccessFlag = ress['flag']

            resp = message_sender.send_message(id, ress['responce'])
            yield 'send', client
            client.send(resp)
            user = ress['user']
            print(ress,'205')
        elif message['url'] == 'authorization':
            fn = con_procc.user_authorisation
            future = pool.submit(fn, id, message_sender, logger, message)
            yield 'future', future
            ress = future.result()

            connectionSuccessFlag = ress['flag']

            yield 'send', client
            client.send(ress['responce'])
            user = ress['user']
        elif message['url'] == 'registration':
            procedure = True
            fn = con_procc.user_registration_part1
            future = pool.submit(fn, id, message_sender, logger, message)
            yield 'future', future
            r1ress = future.result()
            print(r1ress,220)
            if r1ress['success']:
                user = r1ress['user']

                validation_res = False
                code_send_attempts = 3
                while code_send_attempts > 0:



                    r2ress = con_procc.user_registration_part2(id, message_sender, logger, user,context)
                    print(r2ress,231)
                    try:print(user.__dict__)
                    except Exception as e:print(e)
                    if r2ress['success']:
                        code = r2ress['code']
                        attempts = 3
                        print(code)
                        while attempts > 0:
                            try:
                                yield 'recv',client
                                message = client.recv(2048)
                                message = message_receiver.recieve_message(id,message)
                                print(message)
                                try:
                                    message = json_loader(message)
                                    if not 'code' in list(message.keys()):
                                        client.send(message_sender.send_message(id, json.dumps(
                                            {'url': 'registration', "auth_data_exchange": False,
                                             'error': 'data crashed or code or sent code empty'})))

                                        attempts -= 1
                                        continue
                                except json.JSONDecodeError as e:
                                    client.send(message_sender.send_message(id, json.dumps({'url':'registration',"auth_data_exchange": False, 'error': 'data crashed or code or sent code empty'})))
                                    print(e, 'auth data recieve error')
                                    attempts -= 1
                                    continue
                                except Exception as e:
                                    client.send(message_sender.send_message(id, json.dumps(
                                        {'url': 'registration', "auth_data_exchange": False,
                                         'error': 'data crashed or code or sent code empty'})))
                                    print(e, 'auth data recieve error')
                                    attempts -= 1
                                    continue
                            except ConnectionResetError as e:
                                print('error asc', e)
                                print(f"client {id} disconnected")
                                active_clients.pop(id)
                                client.close()
                                cryptor.delete_RSA_keys()
                                return
                            except Exception as e:
                                print(f"error: {e}")

                            fn = con_procc.user_registration_part3
                            future = pool.submit(fn,id, message_sender, logger, user,code,message)
                            r3ress = future.result()
                            print(r3ress)
                            if r3ress['success']:
                                if r3ress['validation']:
                                    validation_res = True
                                    break
                                else:
                                    response = message_sender.send_message(id,json.dumps({'url':'registration',"auth_data_exchange": False, 'error': f"invalid code, you have {attempts-1} more attemps"}))
                                    client.send(response)
                            else:
                                client.send(message_sender.send_message(id,json.dumps({'url':'registration',"auth_data_exchange": False, 'error': "smth wrong"})))

                            attempts -= 1

                        code_send_attempts -= 1
                        if validation_res:
                            break
                        else:
                            response = message_sender.send_message(id,json.dumps({'url':'registration',"auth_data_exchange": False, 'error': "invalid code, we sent new code to your email"}))
                            client.send(response)



                if validation_res:
                    # if True:
                    fn = con_procc.user_registration_part4
                    print(user.__dict__,user)
                    future = pool.submit(fn, id, message_sender, logger, user)
                    yield 'future', future
                    r4ress = future.result()
                    if r4ress['success']:
                        connectionSuccessFlag = True
                        client.send(r4ress['response'])
                    else:
                        client.send(r4ress['response'])
                        connectionSuccessFlag = False
                else:
                    response_model = message_sender.send_message(id,json.dumps({'url':'registration',"message": "registration failed","auth_success": False}))
                    client.send(response_model)
            else:
                client.send(r1ress['response'])
                active_clients.pop(id)
                cryptor.delete_RSA_keys()
                client.close()
                return


            # resp = message_sender.send_message(id,r4ress['response'])
            # yield 'send',client
            # client.send(resp)
            # user = ress['user']
        if connectionSuccessFlag:
            break
        attempcounter += 1

    print('connect flag server ' ,connectionSuccessFlag)
    if not connectionSuccessFlag:
        active_clients.pop(id)
        client.close()
        cryptor.delete_RSA_keys()
        return

    active_users[user.username] = id
    future = pool.submit(message_processor.send_unsent_messages, user.username,logger)
    yield 'future', future
    ress = future.result()
    #if client ready to listen
    for message in ress['messages']:
        try:
            m = message_sender.send_message(id, json.dumps({'url':"message",'message':message.__dict__}))
            yield 'send', client
            client.send(m)

            message_processor.updateSent(message.id,logger)
        except Exception as e:
            print('unsent message not sent',e)
    # READY TO LISTEN
    print('ready to listen messages from {}'.format(user.username))
    while True:
        try:
            yield 'recv', client
            message = client.recv(2048)
            message = message_receiver.recieve_message(id,message)
            try:
                message = json_loader(message)
            except ConnectionAbortedError as e:
                print(f'con error{e}')
                print(f"client {id} disconnected")
                client.close()
                cryptor.delete_RSA_keys()
                active_clients.pop(id)
                break
            except ConnectionResetError as e:
                print('error asc', e)
                print(f"client {id} disconnected")
                active_clients.pop(id)
                client.close()
                cryptor.delete_RSA_keys()
            except Exception as e:
                print(e,'message load error')
                continue
                # client.close()
                # cryptor.delete_RSA_keys()
                # break
            print(message)
            if 'url' not in message.keys():
                continue
            if message['url']=='message':

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
                            message.sent = True
                            message_to_send = json.dumps({'url':"message",'message':message.__dict__})
                            active_clients[active_users[message.receiver]].send(message_sender.send_message(ress_id,message_to_send))

                        except Exception as e:
                            message.sent = False
                            print(e,'not sent to {}'.format(message.receiver))

                    future = pool.submit(message_processor.message_processor, message,logger)
                    yield 'future', future
                    ress = future.result()

                    if ress['created']:
                        response_model = json.dumps({'receiver':message.receiver,'url':"status",'saved':True,'sent': message.sent})
                    else:
                        response_model = json.dumps({'receiver':message.receiver,'url':"status",'saved': False, 'sent': message.sent})
            elif message['url']=='addfriendrequest':
                future = pool.submit(message_processor.addFriendRequest,message['userpattern'], logger)
                yield 'future', future
                ress = future.result()
                if ress['users'] != None:
                    users = ress['users']

                    response_model = json.dumps({'url':'addfriendresponse','users':users})
                else:
                    response_model = json.dumps({'url': 'addfriendresponse', 'users': []})
            elif message['url']=='loadchatrequest':

                future = pool.submit(message_processor.sendAllMessages,user.username, message['username'], logger)
                yield 'future', future
                ress = future.result()

                for message in ress['messages']:
                    try:
                        m = message_sender.send_message(id, json.dumps({'url':"message",'message':message.__dict__}))
                        yield 'send', client
                        client.send(m)

                        message_processor.updateSent(message.id, logger)
                    except ConnectionResetError as e:
                        print('error asc', e)
                        print(f"client {id} disconnected")
                        active_clients.pop(id)
                        client.close()
                        cryptor.delete_RSA_keys()
                        return
                    except Exception as e:
                        print('chat message not sent', e)
                response_model = json.dumps({'url': 'loadchatresponse', 'status':True})
            try:

                prep_message = message_sender.send_message(id, response_model)
                yield 'send', client
                client.send(prep_message)
            except ConnectionAbortedError as e:
                print(f'con error{e}')
                print(f"client {id} disconnected")
                client.close()
                cryptor.delete_RSA_keys()
                return
            except ConnectionResetError as e:
                print('error asc', e)
                print(f"client {id} disconnected")
                active_clients.pop(id)
                client.close()
                cryptor.delete_RSA_keys()
                return
            except Exception as e:
                print('client disconnected', e)
                continue



        except ConnectionAbortedError as e:
            print(f'con error{e}')
            print(f"client {id} disconnected")
            client.close()
            cryptor.delete_RSA_keys()
            return
        except ConnectionResetError as e:
            print(f'con error{e}')
            print(f"client {id} disconnected")
            client.close()
            cryptor.delete_RSA_keys()
            return
        except Exception as e:
            print(f'con error{e}')
            print(f"client {id} disconnected")
            client.close()
            cryptor.delete_RSA_keys()
            return
    print('closed')
    return

def base_server(address):
    logger.log(logging.INFO,'creation of base server')
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




# tasks.append(base_server(('192.168.76.217', 4430)))
# tasks.append(base_server(('172.20.10.8', 4430)))
tasks.append(base_server(('localhost', 4430)))
# tasks.append(base_server(('192.168.1.122', 4430)))

if __name__ == '__main__':
    try:
        print("run")
        run()

    except KeyboardInterrupt as e:
        pool.shutdown(wait=True,cancel_futures=True)
        print("keybord interupted",e)
    except Exception as e:
        print(e,'run error')
