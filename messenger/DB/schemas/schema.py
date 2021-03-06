import uuid

import psycopg2.extras

from DB.models.user_model import CreateUser
import DB.database as db2
connection_eror = "connection error"
database_error = "database error"
class UserSchema:
    def __init__(self,db):
        # self.db = db2
        self.db = db
        if db == None:
            self.db = db2.get_connection()
    def authenticate_user(self,id,username,token):
        auth_flag = False
        try:
            # con = self.db.get_connection()
            con = self.db
            cur = con.cursor()
            cur.execute("insert into authentication_session() where username = %s and token=%s", (username, token,))
            rows = cur.fetchone()
            auth_flag = True
            cur.close()
        except Exception as e:
            auth_flag = False
            print(connection_eror,e)

            
        return auth_flag

    def check_authentication(self,username, token):
        auth_flag = False
        try:
            # con = self.db.get_connection()
            con = self.db
            try:

                cur = con.cursor()
                cur.execute("select * from authentication_session where username = %s and token=%s", (username, token,))
                rows = cur.fetchone()
                if len(rows) == 0:
                    auth_flag = False
                else:
                    auth_flag = True
                
                cur.close()
            except Exception as e:
                auth_flag = False
                print( e)



        except Exception as e:
            print(connection_eror,e)
        return auth_flag

    def username_exist(self,username):
        try:
            # con = self.db.get_connection()
            con = self.db

            try:
                cur = con.cursor()
                cur.execute("select * from user_base ub, user_profile up where username = %s and up.user_id = ub.id",
                            (username,))

                if len(cur.fetchall()) == 0: return {"exist":False,"errors":[]}
                else: return {"exist":True,"errors":[]}
            except Exception as e:
                print(e)
                return {"exist": False, "errors": ["database error"]}
            finally:
                cur.close()
                
        except Exception as e:
            print("connection error",e)
            return {"exist":False,"errors":["connection error"]}

    def getUserByUsername(self,username):
        #TODO rewrite all call and add error processing
        try:
            # con = self.db.get_connection()
            con = self.db

            try:
                user = CreateUser()
                cur = con.cursor()
                cur.execute("select * from user_base ub, user_profile up where username = %s and up.user_id = ub.id",(username,))

                sizerow = cur.fetchone()

                row = {}
                if sizerow != None:

                    c = 0
                    for col in cur.description:
                        row.update({str(col[0]): sizerow[c]})
                        c += 1
                    user.id = str( row["id"])
                    user.username = row["username"]
                    user.password = row["password"]
                    user.email = row["email"]
                    user.first_name = row["first_name"]
                    user.last_name = row["last_name"]
                    user.is_active = row["is_active"]
                    return_block = {"user": user, "errors": []}
                else:
                    return_block = {"user": None, "errors": []}
            except Exception as e:
                print(e,'getByusername')
                return_block = {"user": None, "errors": [e]}
            finally:
                cur.close()
                
        except Exception as e:
            return_block = {"user": None, "errors": [e]}
            print("connection error",e)
        return return_block

    def registrateUser(self, user):
        try:
            # con = self.db.get_connection()
            con = self.db

            try:
                cur = con.cursor()

            except Exception as e:
                print(e)
            finally:
                cur.close()
                
        except Exception as e:
            print(connection_eror)

    def refreshAuthToken(self,username,token):
        commited = False
        try:
            # con = self.db.get_connection()
            con = self.db
            try:
                cur = con.cursor()
                cur.execute("update authentication_session set token= %s, authentication_date=now(),authentication_time=now() where username = %s",(token,username,))
                con.commit()
                commited = True
            except Exception as e:
                print(e)
                commited = False
            finally:
                cur.close()
                
        except Exception as e:
            commited = False
            print("connection error", e)
        return commited

    def insertAuthToken(self, username, token, mac_address, oSys, other_info):
        commited = False
        try:
            # con = self.db.get_connection()
            con = self.db
            try:
                cur = con.cursor()
                cur.execute("delete from authentication_session where username = %s",username)
                con.commit()
                commited = True
            except Exception as e:
                print(e)
                commited = False

            try:
                cur = con.cursor()
                cur.execute("insert into authentication_session(session_id, username, token, mac_address, os, other_info) values(%s,%s,%s,%s,%s,%s)", (  str(uuid.uuid4()), username, token, mac_address, oSys, other_info,))
                con.commit()
                commited = True
            except Exception as e:
                print(e)
                commited = False
            finally:
                cur.close()
                
        except psycopg2.OperationalError.ConnectionFailure as e:
            print(e)
        except Exception as e:
            commited = False
            print("connection error", e)
        return commited

    def deleteAuthToken(self,username):
        sql = "delete from authentication_session where username = %s "
        resp = {}
        try:
            # con = self.db.get_connection()
            con = self.db

            try:
                cur = con.cursor()
                cur.execute(sql,(username,))
                con.commit()
                resp = {'deleted':True,'errors':[]}
            except Exception as e:
                resp = {'deleted': False, 'errors': [e]}
                print(e)
            finally:
                cur.close()
                
        except Exception as e:
            print(connection_eror)
            resp = {'deleted': False, 'errors': [connection_eror,e]}

    def createNewUser(self, user):

        sql1 = "insert into user_base values(%s,%s,%s,%s)"

        sql2 = "insert into user_profile values(%s,%s,%s,%s,%s)"
        commited = False
        try:
            # con = self.db.get_connection()
            con = self.db

            try:
                cur = con.cursor()
                id = str(uuid.uuid4())
                cur.execute(sql1,(id,user.username,user.password,user.email,))
                # con.commit()
                commited = True
                try:
                    cur.execute(sql2, (str(uuid.uuid4()),id, user.first_name, user.last_name, False,))
                    con.commit()
                    commited = True
                except psycopg2.IntegrityError as e:
                    return {'created': False,'errors':['username_taken',e]}
                except Exception as e:
                    print(e,'user profile creation error')
                    return {'created': False, 'errors': ['server_error',e]}

            except Exception as e:
                print(e,"base user createion error")
                commited = False
            finally:
                cur.close()
                

        except Exception as e:
            commited = False
            print("connection error", e)
        return {'created':commited,'errors':[]}
