import json
import uuid
from DB.schemas.schema import UserSchema
from DB.models.user_model import CreateUser
from DB.models.user_model import AuthenticatedUser
import jwt


"""

кейс 1
    я такой клиент ,я  не зарегестрирован, я хочу новый аккаунт
        форма регистрации
кейс 2
    я зарегестрирован вот мои аторизационные данные
        проверить аторизационные данные
кейс 3 
    я авторизован вот мой аутентификатор/токен private.key .crt
        вернуть информацию
кейс 4
    я забыл пароль
        аутентификация        

authentification_check: 
authorization_check: 
authentification_token: token
authorization: [username,password]
"""

def authorisation(username,password):
    userSchema = UserSchema()
    ress = userSchema.getUserByUsername(username)
    if len(ress['errors']) == 0:
        user = ress['user']
        if not user == None:
            if user.password == password:
                return ress

def authentification_token_validation(token, username):
    userSchema = UserSchema()
    return userSchema.check_authentication(username, token)

def email_validation():
    return True

def createAuthToken(username):
    return uuid.uuid4()

def connection_processor(client):
    print("processosr")
    # yield 'recv', client
    message = client.recv(1024).decode()
    message = str(message)
    # ///////////////////////////////////
    userSchema = UserSchema()


    data = json.loads(message)

    {
        "connection_case": {"authorization":False,"authentification":True,"registration":False,"recovery":False},
        "authentification_check": True,
        "authentification_token": "",
        "authorization_check": True,
        "authorization_data": ["username", "password"],
        "registration_data": {"username":"username","password":"password","first_name":"first_name","last_name":"last_name","email":"email"},
        "authentification_token": "",
        "authentification_token": "",
    }
    if data['authentification_check']:
        token = data["authentification_token"]
        username = data["authorization_data"][0]
        # check if token valid for this user


        if authentification_token_validation(token, username):
            ress = userSchema.getUserByUsername(username)
            # yield 'send', client

            client.send(json.dumps({"user": ress['user'].__dict__, "auth_succses": True}).encode())
            return
        else:
           # yield 'send', client
           client.send(json.dumps({"message": "authentication failed", "auth_succses": False}).encode())
           return

    elif data["authorization_check"] and not data['authentification_check']:
        username, password = data["authorization_data"][0], data["authorization_data"][1]
        ress = authorisation(username, password)
        if ress["user"] != None:
            usertoken = str(createAuthToken(username))
            authUser = AuthenticatedUser(ress["user"].__dict__,usertoken)
            #try catch
            client.send(json.dumps({"AuthenticationUser": authUser.__dict__, "auth_succses": True}).encode())
            #TODO return token info from validation,
            # refreshAuthentication(username,token)
            return
        else:
            # yield 'send', client
            client.send(json.dumps({"message": "authorisation failed", "auth_succses": False}).encode())
            return

    else:
        if data['connection_case']['registration']:
            user = CreateUser()
            user.username = data["registration_data"]["username"]
            user.password = data["registration_data"]["password"]
            user.first_name = data["registration_data"]["first_name"]
            user.last_name = data["registration_data"]["last_name"]
            user.email = data["registration_data"]["email"]
            user.is_active = True
            if email_validation(user):
                userSchema.createNewUser(user)


