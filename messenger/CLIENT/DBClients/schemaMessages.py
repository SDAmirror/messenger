import DB.database as db
import datetime

import CLIENT.DBClients.database as db

class MessagesSchema:
    def __init__(self):
        self.db = db

    def send_message(self, message, sender_id, sent):
        try:
            con = self.db.get_connection_sqlite()
            try:
                cursor = con.cursor()
                date_time = datetime.datetime.now()
                # sent check ?
                cursor.execute("insert into messages values(%s, %s, %s, %s, %s')", (message, date_time.strftime("%Y-%m-%d %H:%M:%S"), sent, sender_id, 'sent'))
                con.commit()
            except Exception as e:
                print("connection error", e)
        except Exception as e:
            print("error in sending message", e)
        finally:
            db.close_connectin_sqlite(con)

    def receive_message(self, message, sender_id):
        try:
            con = self.db.get_connection_sqlite()
            try:
                cursor = con.cursor()
                date_time = datetime.datetime.now()
                sent = False
                # sent check ?
                cursor.execute("insert into messages values(%s, %s, %s, %s, %s')", (message, date_time.strftime("%Y-%m-%d %H:%M:%S"), sent, sender_id, 'received'))
                con.commit()
            except Exception as e:
                print("connection error", e)
        except Exception as e:
            print("error in receiving message", e)
        finally:
            db.close_connectin_sqlite(con)




