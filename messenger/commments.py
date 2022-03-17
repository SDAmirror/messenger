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

