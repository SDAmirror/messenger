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













###--------------------------------------------------------------------
# import re
# import smtplib
# import dns.resolver
#
# # Address used for SMTP MAIL FROM command
# fromAddress = 'corn@bt.com'
#
# # Simple Regex for syntax checking
# regex = '^[_a-z0-9-]+(\.[_a-z0-9-]+)*@[a-z0-9-]+(\.[a-z0-9-]+)*(\.[a-z]{2,})$'
#
# # Email address to verify
# inputAddress = input('Please enter the emailAddress to verify:')
# addressToVerify = str(inputAddress)
#
# # Syntax check
# match = re.match(regex, addressToVerify)
# if match == None:
#     print('Bad Syntax')
#     raise ValueError('Bad Syntax')
#
# # Get domain for DNS lookup
# splitAddress = addressToVerify.split('@')
# domain = str(splitAddress[1])
# print('Domain:', domain)
#
# # MX record lookup
# records = dns.resolver.query(domain, 'MX')
# mxRecord = records[0].exchange
# mxRecord = str(mxRecord)
#
# # SMTP lib setup (use debug level for full output)
# server = smtplib.SMTP()
# server.set_debuglevel(0)
#
# # SMTP Conversation
# server.connect(mxRecord)
# server.helo(server.local_hostname)  ### server.local_hostname(Get local server hostname)
# server.mail(fromAddress)
# code, message = server.rcpt(str(addressToVerify))
# server.quit()
#
# # print(code)
# # print(message)
#
# # Assume SMTP response 250 is success
# if code == 250:
#     print('Success')
# else:
#     print('Bad')

#-----------------------------------------------------------------------------------
# class Connection_Processor:
#     def __init__(self,id, cryptor,logger):
#         self.__class__.__name__ = 'Connection_Processor'
#         self.id = id
#         self.cryptor = cryptor
#         self.logger = logger
#         self.userSchema = UserSchema()
#         self.flag = False
#
#     def authentication(self,message):
#         errors = []
#         response_model = ''
#         try:
#             data = json.loads(message)
#         except Exception as e:
#             errors.append(e)
#             return {'responce':None,'errors':errors,'flag':self.flag}
#             print("error json load",e)
#
#         print('responce')
#         token = data["authentification_token"]
#         username = data["authorization_data"][0]
#
#         if authentification_token_validation(token, username):
#             ress = self.userSchema.getUserByUsername(username)
#             usertoken = str(createAuthToken(username))
#             authUser = AuthenticatedUser(ress["user"].__dict__, usertoken)
#             ress = refreshAuthToken(username, usertoken)
#             flag = ress['exist']
#             if not flag:
#                 response_model = json.dumps({"AuthenticationUser": authUser.__dict__, "auth_success": False})
#                 errors.append('token refresh ')
#             else:
#                 self.flag = True
#                 response_model = json.dumps({"AuthenticationUser": authUser.__dict__, "auth_success": True})
#         else:
#             response_model = json.dumps({"message": "authentication failed", "auth_success": False})
#
#         return {'responce':response_model,'errors':errors,'flag':self.flag}

#-----------------------------------------------------------------------------------

# def connection_processor(pool,client, id, cryptor,logger):
#     print('connerctio')
#     # try:
#     global message_sender
#     global message_recirver
#     message_sender.cryptor = cryptor
#     message_recirver.cryptor = cryptor
#     flag_processor_success = False
#     message = client.recv(1024).decode()
#     message = message_recirver.recieve_message(id, str(message))
#     userSchema = UserSchema()
#
#     try:
#         data = json.loads(message)
#     except:
#         print("error json load")
#         return flag_processor_success
#     {
#         "connection_case": {"authorization": False, "authentification": True, "registration": False, "recovery": False},
#         "authentification_check": True,
#         "authentification_token": "",
#         "authorization_check": True,
#         "authorization_data": ["username", "password"],
#         "registration_data": {"username": "username", "password": "password", "first_name": "first_name",
#                               "last_name": "last_name", "email": "email"},
#         "authentification_token": "",
#         "authentification_token": "",
#     }
#
#     # path authentication
#     if data['authentification_check']:
#         response_model = ''
#
#         print('responce')
#         token = data["authentification_token"]
#         username = data["authorization_data"][0]
#
#         if authentification_token_validation(token, username):
#             ress = userSchema.getUserByUsername(username)
#             usertoken = str(createAuthToken(username))
#             authUser = AuthenticatedUser(ress["user"].__dict__, usertoken)
#             flag = refreshAuthToken(username, usertoken)
#
#             if not flag:
#                 response_model = json.dumps({"AuthenticationUser": authUser.__dict__, "auth_success": False})
#             else:
#                 flag_processor_success = True
#                 response_model = json.dumps({"AuthenticationUser": authUser.__dict__, "auth_success": True})
#         else:
#             response_model = json.dumps({"message": "authentication failed", "auth_success": False})
#
#         print(response_model)
#
#         client.send(response_model.encode())
#
#     #authorisation
#     elif data["authorization_check"] and not data['authentification_check']:
#         username, password = data["authorization_data"][0], data["authorization_data"][1]
#         ress = authorisation(username, password)
#         if ress["user"] != None:
#             usertoken = str(createAuthToken(username))
#             authUser = AuthenticatedUser(ress["user"].__dict__, usertoken)
#             # try catch
#             flag = newAuthorisation(username, usertoken, '', '', '')
#             if not flag:
#                 resp = message_sender.send_message(id,json.dumps({"AuthenticationUser": authUser.__dict__, "auth_success": False}))
#                 client.send(resp.encode())
#             else:
#                 resp = message_sender.send_message(id, json.dumps({"AuthenticationUser": authUser.__dict__, "auth_success": True}))
#                 client.send(resp.encode())
#
#
#             # TODO return token info from validation,
#             # refreshAuthentication(username,token)
#             flag_processor_success = True
#
#         else:
#             resp = message_sender.send_message(id, json.dumps(
#                 {"AuthenticationUser": None, "auth_success": False}))
#             client.send(resp.encode())
#
#
#     else:
#         if data['url'] == 'registration':
#             user = CreateUser()
#             user.username = data["registration_data"]["username"]
#             user.password = data["registration_data"]["password"]
#             user.first_name = data["registration_data"]["first_name"]
#             user.last_name = data["registration_data"]["last_name"]
#             user.email = data["registration_data"]["email"]
#             user.is_active = True
#
#             if not email_validation(user.email):
#                 client.send(
#                     json.dumps({"message": "registration failed: wrong email format", "auth_success": False}).encode())
#                 return flag_processor_success
#
#             checkUser = userSchema.getUserByUsername(user.username)
#
#             if checkUser['user'] == None and len(checkUser['errors']) == 0:
#
#                 # database.get_code()
#                 validation_res = False
#                 validator = Validator()
#                 code_send_attempts = 3
#                 while code_send_attempts > 0:
#                     code_generated = validator.generate_code()
#                     ress = validator.send_code(user.email, code_generated)
#                     if len(ress['errors']) == 0:
#                         pass
#                     else:
#                         client.send(json.dumps({"message": "Validation code error", "auth_success": False}).encode())
#
#                     attempts = 3
#
#                     while attempts > 0:
#                         try:
#                             message = client.recv(1024).decode()
#                             message = message_recirver.recieve_message(id, str(message))
#                         except Exception as e:
#                             print(f"error: {e}")
#                             return flag_processor_success
#
#                         try:
#                             code_validation_data = json.loads(message)
#                         except:
#                             print("error json load")
#                             client.send(json.dumps({"message": "data transmition failure packets are damaged",
#                                                     "auth_success": False}).encode())
#                             return flag_processor_success
#
#                         # TODO checkers
#                         code_received = code_validation_data['validation_code']
#
#                         # validator.valid(user, code, coderecieved)  (TRUE/FALSE) {result:TRUE/FALSE,errors=[]}
#
#                         validation_res = validator.validate(user, code_generated, code_received)
#                         if validation_res:
#                             break
#                         attempts -= 1
#
#                     code_send_attempts -= 1
#                     if validation_res:
#                         break
#                 if validation_res == True:
#
#                     ress = userSchema.createNewUser(user)
#                     if 'username_taken' in ress['errors']:
#                         client.send(json.dumps(
#                             {"message": "registration failed: username already taken", "auth_success": False}).encode())
#                     if ress['created']:
#                         usertoken = str(createAuthToken(user.username))
#                         authUser = AuthenticatedUser(user.__dict__, usertoken)
#                         # try catch
#                         flag = newAuthorisation(user.username, usertoken, '', '', '')
#                         if not flag:
#                             client.send(
#                                 json.dumps(
#                                     {"AuthenticationUser": authUser.__dict__, "auth_success": False}).encode())
#                         else:
#                             # TODO registration logs
#                             client.send(
#                                 json.dumps(
#                                     {"AuthenticationUser": authUser.__dict__, "auth_success": True}).encode())
#                             flag_processor_success = True
#
#
#                     else:
#                         client.send(json.dumps({"message": "registration failed", "auth_success": False}).encode())
#                     # break
#                 else:
#                     client.send(json.dumps({"message": "registration failed", "auth_success": False}).encode())
#
#
#
#             else:
#                 client.send(json.dumps({"message": "registration failed", "auth_success": False}).encode())
#     return flag_processor_success
#     # except Exception as e:
#     #     print(f"error: {e}")

