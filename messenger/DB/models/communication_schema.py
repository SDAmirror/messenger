import uuid
import psycopg2.extras
from DB.models.user_model import CreateUser
from DB.models.message_model import MessageInfo
import DB.database as db
connection_eror = "connection error"
database_error = "database error"

class CommunicationSchema:
    def __init__(self):
        self.db = db

    def insert_message(self,message,logger):
        # sql1 = "insert into messages values(%s,%s,%s,%s)"
        # sql2 = "insert into message_info values(%s,%s,%s,%s)"
        sql =  "insert into message values(%s,%s,%s,%s,%s,%s,%s)"
        commited = False
        try:
            con = self.db.get_connection()
            try:
                psycopg2.extras.register_uuid()
                cur = con.cursor()
                cur.execute(sql,(message.id,message.content,message.send_date,message.send_time,message.sender,message.receiver,message.sent,))
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

    def searchForSimilar(self, username, logger):
        try:
            con = self.db.get_connection()
            messages = []
            try:
                cur = con.cursor()
                sql = "select * from message where receiver = %s and sent=false"
                cur.execute(sql,(username,))
                for row in cur.fetchall():
                    message = MessageInfo(row[0],row[1],row[2],row[3],row[4],row[5],row[6])
                    message.send_time = message.send_time.strftime('%H-%M-%S')
                    message.send_date = message.send_date.__str__()
                    messages.append(message)
                return_block = {"messages": messages, "errors": []}
            except Exception as e:
                print(e,'send_unsent_messages')
                return_block = {"messages": None, "errors": [e]}
            finally:
                cur.close()
                con.close()
        except Exception as e:
            return_block = {"messages": None, "errors": [e]}
            print("connection error",e)
        return return_block

    def updateSent(self,id,logger):


        sql = "update message set sent=true where id = %s"
        commited = False
        try:
            con = self.db.get_connection()
            try:
                psycopg2.extras.register_uuid()
                cur = con.cursor()
                cur.execute(sql, (id,))
                con.commit()
                commited = True
            except Exception as e:
                print(e, "message saving error")
                print( "message saving error")
                commited = False
            finally:
                cur.close()
                con.close()
        except Exception as e:
            commited = False
            print("connection error", e)
            return {'created': commited, 'errors': [e]}
        return {'created': commited, 'errors': []}
    def load_all_messages(self,username, logger):
        try:
            con = self.db.get_connection()
            messages = []
            try:
                cur = con.cursor()
                sql = "select * from message where receiver = %s or sender=%s"
                cur.execute(sql,(username,username,))
                for row in cur.fetchall():
                    message = MessageInfo(row[0],row[1],row[2],row[3],row[4],row[5],row[6])
                    message.send_time = message.send_time.strftime('%H-%M-%S')
                    message.send_date = message.send_date.__str__()
                    messages.append(message)
                return_block = {"messages": messages, "errors": []}
            except Exception as e:
                print(e,'send_unsent_messages')
                return_block = {"messages": None, "errors": [e]}
            finally:
                cur.close()
                con.close()
        except Exception as e:
            return_block = {"messages": None, "errors": [e]}
            print("connection error",e)
        return return_block