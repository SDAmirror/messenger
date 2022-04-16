from DB.models.message_model import MessageInfo
from DB.schemas.message_shema import MessageSchema

def message_rpepare(data,loger):
    return data
def message_processor(data,logger):
    if 1: return 44124
    schema = MessageSchema()
    reciever = data['reciever']
    body = data['body']
    send_date = data['send_date']
    send_time = data['send_time']
    message = MessageInfo()
    schema.insert_message(message,logger)

    return 44124


class Message_Recirver:
    def __init__(self, cryptor=None):
        self.cryptor = cryptor

    def recieve_message(self, id, message):
        # return self.cryptor.decrypt(message)
        return message


class Message_Sender:
    def __init__(self, cryptor=None):
        self.cryptor = cryptor

    def send_message(self, id, message):
        # return self.cryptor.encrypt(message)
        return message


class Message_Processor:
    def __init__(self, client):
        self.client = client
