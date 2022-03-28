import smtplib
import ssl


class Validator:
    def generate_code(self):
        from random import randint
        code = str(randint(1000000, 9999999))
        return code

    def send_code(self, receiver_email, code):
        port = 465  # For SSL
        smtp_server = "smtp.gmail.com"
        # password = input("Type your password and press enter: ")
        password = "doripass568word"

        sender = "amanbolganovadaria@gmail.com"
        receiver = "damanbolghanova@gmail.com"

        message = """From: Check <amanbolganovadaria@gmail.com>
        Subject: SMTP e-mail test
        YOUR CODE is """ + self.generate_code()

        # Create a secure SSL context
        context = ssl.create_default_context()

        with smtplib.SMTP_SSL(smtp_server, port, context=context) as server:
            server.login(sender, password)
            # Send email here
            server.sendmail(sender, receiver, message)

    # def validate(self, user, code, code_received):

