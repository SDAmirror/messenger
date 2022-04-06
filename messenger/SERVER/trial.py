def user_registration_part1(id, cryptor, logger,data):
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


    checkUser = userSchema.getUserByUsername(user.username)

    if checkUser['user'] == None and len(checkUser['errors']) == 0:
        validation_res = False
        validator = Validator()
        code_send_attempts = 3
        while code_send_attempts > 0:
            code_generated = validator.generate_code()
            ress = validator.send_code(user.email, code_generated)
            if len(ress['errors']) == 0:
                pass
            else:
                response_model = message_sender.send_message(json.dumps({"message": "Validation code error", "auth_success": False}))
            attempts = 3

            while attempts > 0:
                try:
                    message = client.recv(1024).decode()
                    message = message_recirver.recieve_message(id, str(message))
                except Exception as e:
                    print(f"error: {e}")


                try:
                    code_validation_data = json.loads(message)
                except:
                    print("error json load")
                    response_model = message_sender.send_message(json.dumps({"message": "data transmition failure packets are damaged", "auth_success": False}))
                code_received = code_validation_data['validation_code']

                # validator.valid(user, code, coderecieved)  (TRUE/FALSE) {result:TRUE/FALSE,errors=[]}

                validation_res = validator.validate(user, code_generated, code_received)
                if validation_res:
                    break
                attempts -= 1

            code_send_attempts -= 1
            if validation_res:
                break
        if validation_res == True:

            ress = userSchema.createNewUser(user)
            if 'username_taken' in ress['errors']:
                response_model = message_sender.send_message(json.dumps({"message": "registration failed: username already taken", "auth_success": False}))
            if ress['created']:
                usertoken = str(createAuthToken(user.username))
                authUser = AuthenticatedUser(user.__dict__, usertoken)
                # try catch
                flag = newAuthorisation(user.username, usertoken, '', '', '')
                if not flag:
                    response_model = message_sender.send_message(json.dumps({"AuthenticationUser": authUser.__dict__, "auth_success": False}))
                else:
                    # TODO registration logs
                    response_model = message_sender.send_message(json.dumps({"AuthenticationUser": authUser.__dict__, "auth_success": True}))
                    flag_processor_success = True


            else:
                response_model = message_sender.send_message(json.dumps({"message": "registration failed", "auth_success": False}))
        else:
            response_model = message_sender.send_message(json.dumps({"message": "registration failed", "auth_success": False}))
    else:
        response_model = message_sender.send_message(json.dumps({"message": "registration failed", "auth_success": False}))
