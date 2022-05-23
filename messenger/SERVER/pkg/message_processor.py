import uuid
from DB.models.message_model import MessageInfo
from DB.schemas.message_shema import MessageSchema


def message_rpepare(data,username,loger):
    try:
        reciever = data['reciever']
        body = data['body']
        send_date = data['send_date']
        send_time = data['send_time']
        id = uuid.uuid4()
        message = MessageInfo(id, body, send_date, send_time, username, reciever)
        return {'message': message, 'errors': []}
    except Exception as e:
        return {'message': None, 'errors': [e]}
def send_unsent_messages(username,logger):
    schema = MessageSchema()
    messages = schema.send_unsent_messages(username,logger)

    return messages
def updateSent(id,logger):
    schema = MessageSchema()

    return schema.updateSent(id, logger)
def message_processor(message,logger):

    schema = MessageSchema()

    return schema.insert_message(message,logger)


class Message_Recirver:
    def __init__(self, cryptor=None):
        self.cryptor = cryptor

    def recieve_message(self, id, message):
        m = self.cryptor.decrypt(message)
        return m.rstrip()
class Message_Sender:
    def __init__(self, cryptor=None):
        self.cryptor = cryptor

    def send_message(self, id, message):

        return self.cryptor.encrypt(id,message)
        # return message


class Message_Processor:
    def __init__(self, client):
        self.client = client
