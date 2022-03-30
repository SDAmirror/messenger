# from DB.models.user_model import CreateUser
# import DB.database as db
# import json
#
#
# def getUserByUsername(username):
#     try:
#         user = CreateUser()
#         con = db.get_connection()
#         cur = con.cursor()
#         cur.execute("select * from user_base ub, user_profile up where username = %s and up.user_id = ub.id",
#                     (username,))
#         row = {}
#         for buff in cur:
#             c = 0
#             for col in cur.description:
#                 row.update({str(col[0]): buff[c]})
#                 c += 1
#         user.id = row["id"]
#         user.username = row["username"]
#         user.password = row["password"]
#         user.email = row["email"]
#         user.first_name = row["first_name"]
#         user.last_name = row["last_name"]
#         user.is_active = row["is_active"]
#         return {"result": user, "errors": []}
#     except:
#         {"result": {}, "errors": ["error"]}
#     finally:
#         con.close()
# mess = getUserByUsername("user1")
#
# print(json.dumps({"user":mess['result'].__dict__}))
# import time
#
# import jwt
# start = time.time()
# code = jwt.encode(payload= {
#         "connection_case": {"authorization":False,"authentification":True,"registration":False,"recovery":False},
#         "authentification_check": True,
#         "authentification_token": "",
#         "authorization_check": True,
#         "authorization_data": ["username", "password"],
#         "registration_data": {"username":"username","password":"password","first_name":"first_name","last_name":"last_name","email":"email"},
#         "authentification_token": "",
#         "authentification_token": "",
#     },key="secret woed",algorithm="HS256")
# text = jwt.decode(code,"secret woed",algorithms=["HS256"])
#
# endt = time.time()
#
#
# print(endt-start)
# print(text)




#-------------------------------
# import smtplib, ssl
# from email.mime.text import MIMEText
# from email.mime.multipart import MIMEMultipart
#
# sender_email = "myvideoboxdsa@gmail.com"
# receiver_email = "flamehst@mail.ru"
# password = 'ziqzxjotlibxpkfq'
#
# message = MIMEMultipart("alternative")
# message["Subject"] = "multipart test"
# message["From"] = sender_email
# message["To"] = receiver_email
#
# # Create the plain-text and HTML version of your message
# text = """\
# Hi,
# How are you?
# Real Python has many great tutorials:
# www.realpython.com"""
# html = """\
# <html>
#   <body>
#     <p>Hi,<br>
#        How are you?<br>
#        <a href="http://www.realpython.com">Real Python</a>
#        has many great tutorials.
#     </p>
#   </body>
# </html>
# """
#
# # Turn these into plain/html MIMEText objects
# part1 = MIMEText(text, "plain")
# part2 = MIMEText(html, "html")
#
# # Add HTML/plain-text parts to MIMEMultipart message
# # The email client will try to render the last part first
# message.attach(part1)
# message.attach(part2)
#
# # Create secure connection with server and send email
# context = ssl.create_default_context()
# with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as server:
#     server.login(sender_email, password)
#     server.sendmail(
#         sender_email, receiver_email, message.as_string()
#     )
import random
import re
import time

def email_validation(email):
    email_pattern = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
    if (re.fullmatch(email_pattern, email)):
        return True
    else:
        return False

ts = time.time()
res = email_validation("wwdwad,@del.cw")
te = time.time()
print(te-ts,res)




