import uuid
import psycopg2.extras
from DB.models.user_model import CreateUser
from DB.models.message_model import MessageInfo
import DB.database as db
connection_eror = "connection error"
database_error = "database error"

class MessageSchema:
    def __init__(self):
        self.db = db

    def insert_message(self,message,logger):

        sql1 = "insert into messages values(%s,%s,%s,%s)"
        sql2 = "insert into message_info values(%s,%s,%s,%s)"
        sql =  "insert into message values(%s,%s,%s,%s,%s,%s,%s)"
        commited = False
        try:
            con = self.db.get_connection()

            try:
                psycopg2.extras.register_uuid()
                cur = con.cursor()
                cur.execute(sql,(message.id,message.content,message.send_date,message.send_time,message.sender,message.receiver,message.sent))
                # id = str(uuid.uuid4())
                # cur.execute(sql1, (message.id, message.content, message.send_date,message.send_time))
                # # con.commit()
                # commited = True
                # try:
                #     cur.execute(sql2, (str(uuid.uuid4()), message.id, message.sender,message.reciver,message.sent))
                #     con.commit()
                #     commited = True
                # except Exception as e:
                #     print(e, 'message save error')
                #     {'created': False, 'errors': ['server_error', e]}
                con.commit()
                commited = True
            except Exception as e:
                print(e, "message saving error")
                commited = False
            finally:
                cur.close()
                con.close()

        except Exception as e:
            commited = False
            print("connection error", e)
            return {'created': commited, 'errors': [e]}
        return {'created': commited,'errors':[]}