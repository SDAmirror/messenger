class Message:
    def __init__(self,id,content,send_date,send_time):
        self.id = id
        self.content = content
        self.send_date = send_date
        self.send_time = send_time

class MessageInfo(Message):
    def __init__(self,id, content, send_date, send_time,sender,reciver,sent = False):
        self.__class__.__name__ = "MessageInfo"
        self.sender = sender
        self.reciver = reciver
        self.sent = sent
        super().__init__(id, content, send_date, send_time,)