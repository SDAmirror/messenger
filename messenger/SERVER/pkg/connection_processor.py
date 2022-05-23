import json
import uuid
import re
from DB.schemas.schema import UserSchema
from DB.models.user_model import CreateUser
from DB.models.user_model import AuthenticatedUser
from .email_validation import Validator
from pkg.message_processor import *
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
        print(e,'authen token validation')
        return {"exist": False, "errors": ["Auth Token validation error"]}


def createAuthToken(username):
    try:
        return uuid.uuid4()
    except Exception as e:
        print(e,'create auth token')
        return {"exist": False, "errors": ["Auth Token creation error"]}


def refreshAuthToken(username, token):
    userSchema = UserSchema()
    try:
        return {'exist':userSchema.refreshAuthToken(username, token),'errors':[]}
    except Exception as e:
        print(e, 'auth token refresh ')
        return {"exist": False, "errors": ["Auth Token  refreshing error"]}


def newAuthorisation(username, token, mac_address, oSys, other_info):
    userSchema = UserSchema()
    fdeleted = False
    try:
        ress = userSchema.deleteAuthToken(username)
        fdeleted = ress['deleted']
    except Exception as e:
        print(e)
    try:
        return userSchema.insertAuthToken(username, token, mac_address, oSys, other_info)
    except Exception as e:
        print(e, 'new auth token')
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



def user_authentication(id, cryptor, logger,data):
    print(data,'atu',type(data))
    userSchema = UserSchema()
    flag = False
    errors = []
    response_model = ''
    user = None


    token = data["authentification_token"]
    username = data["authorization_data"][0]

    if authentification_token_validation(token, username):
        ress = userSchema.getUserByUsername(username)
        if ress['user'] == None:
            errors.append(ress['errors'])
            response_model = json.dumps({"message": "authentication failed", "auth_success": False})
            return {'responce': response_model, 'errors': errors, 'flag': flag}
        usertoken = str(createAuthToken(username))
        authUser = AuthenticatedUser(ress["user"].__dict__, usertoken)
        ress = refreshAuthToken(username, usertoken)
        eflag = ress['exist']
        if not eflag:
            response_model = json.dumps({"AuthenticationUser": authUser.__dict__, "auth_success": False})
            errors.append('token refresh ')
        else:
            flag = True
            response_model = json.dumps({"AuthenticationUser": authUser.__dict__, "auth_success": True})
    else:
        response_model = json.dumps({"message": "authentication failed", "auth_success": False})

    return {'responce': response_model, 'errors': errors, 'flag': flag,'user':user}
def user_authorisation(id, message_sender, logger,data):

    user = None
    userSchema = UserSchema()
    flag = False
    errors = []
    response_model = ''

    username, password = data["authorization_data"][0], data["authorization_data"][1]
    ress = authorisation(username, password)
    if ress["user"] != None:
        user = ress['user']
        print(user.__dict__)
        usertoken = str(createAuthToken(username))
        authUser = AuthenticatedUser(user.__dict__, usertoken)
        # try catch
        eflag = newAuthorisation(username, usertoken, '', '', '')
        if not eflag:
            resp = message_sender.send_message(id, json.dumps({"AuthenticationUser": authUser.__dict__, "auth_success": False}))
        else:
            print(authUser.__dict__)
            resp = message_sender.send_message(id, json.dumps({"AuthenticationUser": authUser.__dict__, "auth_success": True}))
            flag = True

        # TODO return token info from validation,
        # refreshAuthentication(username,token)
        flag_processor_success = True

    else:
        resp = message_sender.send_message(id, json.dumps({"AuthenticationUser": None, "auth_success": False}))
    return {'responce': resp, 'errors': errors, 'flag': flag,'user':user}

def user_registration_part1(id, message_sender, logger,data):
    userSchema = UserSchema()
    flag = False
    errors = []
    response_model = ''
    user = CreateUser()
    user.username = data["registration_data"]["username"]
    user.password = data["registration_data"]["password"]
    user.first_name = data["registration_data"]["first_name"]
    user.last_name = data["registration_data"]["last_name"]
    user.email = data["registration_data"]["email"]
    user.is_active = True

    if not email_validation(user.email):
        response_model = message_sender.send_message(json.dumps({"message": "registration failed: wrong email format", "auth_success": False}))
        return {'success':False,'response':response_model}
    checkUser = userSchema.getUserByUsername(user.username)

    if checkUser['user'] == None and len(checkUser['errors']) == 0:
        return {'success':True,'user':user}
    else:
        response_model = message_sender.send_message(id,json.dumps({"message": "registration failed: username taken", "auth_success": False}))
        return {'success':False,'response':response_model}
def user_registration_part2(id, message_sender, logger,user,context=None):
    validator = Validator()
    code_generated = validator.generate_code()
    ress = validator.send_code(user.email, code_generated,context)
    if len(ress['errors']) == 0:
        return {'success':True,'code':code_generated}
    else:
        response_model = message_sender.send_message(id,json.dumps({"message": "Validation code error", "auth_success": False}))
        return {'success':False,'response':response_model}

def user_registration_part3(id, message_sender, logger,user, code,message):
    validator = Validator()

    # try:
    #     message = message_recirver.recieve_message(id, str(message))
    #     code_validation_data = json.loads(message)
    # except Exception as e:
    #     print("error json load",
    #           e,
    #           type(e).__name__,  # TypeError
    #           __file__,  # /tmp/example.py
    #           e.__traceback__.tb_lineno  # 2
    #           )
    #     response_model = message_sender.send_message(id,json.dumps({"message": "data transmition failure packets are damaged", "auth_success": False}))
    #     return {'success':False,'response':response_model}
    # code_received = code_validation_data['validation_code']
    code_received = message

    # validator.valid(user, code, coderecieved)  (TRUE/FALSE) {result:TRUE/FALSE,errors=[]}

    validation_res = validator.validate(user, code, code_received)
    return {'success':True,'validation':validation_res}
def user_registration_part4(id, message_sender, logger,user):
    userSchema = UserSchema()
    flag = False
    errors = []
    response_model = ''
    ress = userSchema.createNewUser(user)
    if 'username_taken' in ress['errors']:
        response_model = message_sender.send_message(id,json.dumps({"message": "registration failed: username already taken", "auth_success": False}))
        return {'success':False,'response':response_model}
    if ress['created']:
        usertoken = str(createAuthToken(user.username))
        authUser = AuthenticatedUser(user.__dict__, usertoken)
        # try catch
        flag = newAuthorisation(user.username, usertoken, '', '', '')
        if not flag:

            response_model = message_sender.send_message(id,json.dumps({"AuthenticationUser": authUser.__dict__, "auth_success": False}))
            return {'success': False, 'response': response_model,'errors':['UserAuthorisationFailure']}
        else:
            # TODO registration logs
            response_model = message_sender.send_message(id,json.dumps({"AuthenticationUser": authUser.__dict__, "auth_success": True}))
            return {'success': True, 'response': response_model}
    else:
        response_model = message_sender.send_message(id,json.dumps({"message": "registration failed because of: {}".format(';'.join(ress['errors'])), "auth_success": False}))
        return {'success': False, 'response': response_model,'errors':['UsernameTaken']}
