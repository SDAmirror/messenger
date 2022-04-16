import smtplib
import ssl


class Validator:
    def generate_code(self):
        from random import randint
        code = str(randint(1000000, 9999999))
        return code

    def send_code(self, receiver_email, code):
        result = {'result': {}, 'errors': []}
        port = 465  # For SSL
        smtp_server = "smtp.gmail.com"
        password = "doripass568word"
        # sender = "myvideoboxdsa@gmail.com"
        # receiver_email = "flamehst@mail.ru"
        # password = 'ziqzxjotlibxpkfq'
        sender = "amanbolganovadaria@gmail.com"

        message = """Check:
        Subject: SMTP e-mail test
        YOUR CODE is """ + code

        # Create a secure SSL context
        try:
            context = ssl.create_default_context()
        except Exception as e:
            print(e)
            result['errors'] = "SSL context creation error"

        with smtplib.SMTP_SSL(smtp_server, port, context=context) as server:
            try:
                server.login(sender, password)
            except Exception as e:
                print(e)
                result['errors'] = "Server login error"

            # Send email here
            try:
                server.sendmail(sender, receiver_email, message)
            except Exception as e:
                result['errors'] = "Server error: couldn't send code"

        return result

    def validate(self, user, code_generated, code_received):
        return code_generated == code_received

