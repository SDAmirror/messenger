import json
import uuid
import re
from DB.schemas.schema import UserSchema
from DB.models.user_model import CreateUser
from DB.models.user_model import AuthenticatedUser
from .email_validation import Validator
from message_processor import *
import rsa

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
message_recirver = Message_Recirver()
message_sender = Message_Sender()

def authorisation(username, password):
    userSchema = UserSchema()
    ress = userSchema.getUserByUsername(username)
    if len(ress['errors']) == 0:
        user = ress['user']
        if not user == None:
            if user.password == password:
                return ress


def authentification_token_validation(token, username):
    userSchema = UserSchema()
    try:
        return userSchema.check_authentication(username, token)
    except Exception as e:
        print(e)
        return {"exist": False, "errors": ["Auth Token validation error"]}


def createAuthToken(username):
    try:
        return uuid.uuid4()
    except Exception as e:
        print(e)
        return {"exist": False, "errors": ["Auth Token creation error"]}


def refreshAuthToken(username, token):
    userSchema = UserSchema()
    try:
        return userSchema.refreshAuthToken(username, token)
    except Exception as e:
        print(e)
        return {"exist": False, "errors": ["Auth Token  refreshing error"]}


def newAuthorisation(username, token, mac_address, oSys, other_info):
    userSchema = UserSchema()
    try:
        return userSchema.insertAuthToken(username, token, mac_address, oSys, other_info)
    except Exception as e:
        print(e)
        return {"exist": False, "errors": ["Authorization error"]}


# check email
def email_validation(email):
    email_pattern = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
    if (re.fullmatch(email_pattern, email)):
        return True
    else:
        return False

# try:
#     emailObject = validate_email(testEmail)
#     testEmail = emailObject.email
#     print(testEmail)
# except EmailNotValidError as errorMsg:
#     print(str(errorMsg))

def connection_processor(client, id,cryptor):
    global message_sender
    global message_recirver
    message_sender.cryptor = cryptor
    message_recirver.cryptor = cryptor
    print("processors")
    flag_processor_success = False
    message = client.recv(1024).decode()
    message = message_recirver.recieve_message(id, str(message))
    userSchema = UserSchema()


    try:
        data = json.loads(message)
    except:
        print("error json load")
        return flag_processor_success
    {
        "connection_case": {"authorization": False, "authentification": True, "registration": False, "recovery": False},
        "authentification_check": True,
        "authentification_token": "",
        "authorization_check": True,
        "authorization_data": ["username", "password"],
        "registration_data": {"username": "username", "password": "password", "first_name": "first_name",
                              "last_name": "last_name", "email": "email"},
        "authentification_token": "",
        "authentification_token": "",
    }
    if data['authentification_check']:
        token = data["authentification_token"]
        username = data["authorization_data"][0]
        # check if token valid for this user

        if authentification_token_validation(token, username):
            ress = userSchema.getUserByUsername(username)
            usertoken = str(createAuthToken(username))
            authUser = AuthenticatedUser(ress["user"].__dict__, usertoken)
            flag = refreshAuthToken(username, usertoken)

            # yield 'send', client

            if not flag:
                client.send(json.dumps({"AuthenticationUser": authUser.__dict__, "auth_succses": False}).encode())

            else:
                flag_processor_success = True
                client.send(json.dumps({"AuthenticationUser": authUser.__dict__, "auth_succses": True}).encode())

        else:
            # yield 'send', client
            client.send(json.dumps({"message": "authentication failed", "auth_succses": False}).encode())


    elif data["authorization_check"] and not data['authentification_check']:
        username, password = data["authorization_data"][0], data["authorization_data"][1]
        ress = authorisation(username, password)
        if ress["user"] != None:
            usertoken = str(createAuthToken(username))
            authUser = AuthenticatedUser(ress["user"].__dict__, usertoken)
            # try catch
            flag = newAuthorisation(username, usertoken, '', '', '')
            if not flag:
                client.send(json.dumps({"AuthenticationUser": authUser.__dict__, "auth_success": False}).encode())
            else:
                client.send(json.dumps({"AuthenticationUser": authUser.__dict__, "auth_success": True}).encode())

            # TODO return token info from validation,
            # refreshAuthentication(username,token)
            flag_processor_success = True

        else:
            # yield 'send', client
            client.send(json.dumps({"message": "authorisation failed", "auth_succses": False}).encode())


    else:
        if data['connection_case'] == 'registration':
            user = CreateUser()
            user.username = data["registration_data"]["username"]
            user.password = data["registration_data"]["password"]
            user.first_name = data["registration_data"]["first_name"]
            user.last_name = data["registration_data"]["last_name"]
            user.email = data["registration_data"]["email"]
            user.is_active = True

            if not email_validation(user.email):
                client.send(json.dumps({"message": "registration failed: wrong email format", "auth_succses": False}).encode())
                return flag_processor_success

            checkUser = userSchema.getUserByUsername(user.username)

            if checkUser['user'] == None and len(checkUser['errors']) == 0:

                # database.get_code()
                validation_res = False
                validator = Validator()
                code_send_attems = 3
                while code_send_attems > 0:
                    code_generated = validator.generate_code()
                    ress = validator.send_code(user.email, code_generated)
                    if len(ress['errors']) == 0:
                        pass
                    else:
                        client.send(json.dumps({"message": "Validation code error", "auth_success": False}).encode())

                    attemps = 3

                    while attemps > 0:
                        try:
                            message = str(client.recv(1024).decode())
                        except Exception as e:
                            return flag_processor_success

                        try:
                            code_validation_data = json.loads(message)
                        except:
                            print("error json load")
                            client.send(json.dumps({"message": "data transmition failure packets are damaged",
                                                    "auth_success": False}).encode())
                            return flag_processor_success

                        #TODO checkers
                        code_received = code_validation_data['validation_code']

                        # validator.valid(user, code, coderecieved)  (TRUE/FALSE) {result:TRUE/FALSE,errors=[]}

                        validation_res = validator.validate(user, code_generated, code_received)
                        if validation_res:
                            break
                        attemps -= 1

                    code_send_attems -= 1
                    if validation_res:
                        break
                if validation_res == True:

                    ress = userSchema.createNewUser(user)
                    if 'username_taken' in ress['errors']:
                        client.send(json.dumps({"message": "registration failed: username already taken", "auth_succses": False}).encode())
                    if ress['created']:
                        usertoken = str(createAuthToken(user.username))
                        authUser = AuthenticatedUser(user.__dict__, usertoken)
                        # try catch
                        flag = newAuthorisation(user.username, usertoken, '', '', '')
                        if not flag:
                            client.send(
                                json.dumps(
                                    {"AuthenticationUser": authUser.__dict__, "auth_succses": False}).encode())
                        else:
                            # TODO registration logs
                            client.send(
                                json.dumps(
                                    {"AuthenticationUser": authUser.__dict__, "auth_succses": True}).encode())
                            flag_processor_success = True


                    else:
                        client.send(json.dumps({"message": "registration failed", "auth_succses": False}).encode())
                    # break
                else:
                    client.send(json.dumps({"message": "registration failed", "auth_succses": False}).encode())



            else:
                client.send(json.dumps({"message": "registration failed", "auth_succses": False}).encode())
    return flag_processor_success
