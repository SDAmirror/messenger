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
import time

import jwt
start = time.time()
code = jwt.encode(payload= {
        "connection_case": {"authorization":False,"authentification":True,"registration":False,"recovery":False},
        "authentification_check": True,
        "authentification_token": "",
        "authorization_check": True,
        "authorization_data": ["username", "password"],
        "registration_data": {"username":"username","password":"password","first_name":"first_name","last_name":"last_name","email":"email"},
        "authentification_token": "",
        "authentification_token": "",
    },key="secret woed",algorithm="HS256")
text = jwt.decode(code,"secret woed",algorithms=["HS256"])

endt = time.time()


print(endt-start)
print(text)

