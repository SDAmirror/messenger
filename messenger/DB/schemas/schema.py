from DB.models.user_model import CreateUser
import DB.database as db
connection_eror = "connection error"
database_error = "database error"
class UserSchema:
    def __init__(self):
        self.db = db
    def authenticate_user(self,id,username,token):
        auth_flag = False
        try:
            con = self.db.get_connection()
            cur = con.cursor()
            cur.execute("insert into authentication_session() where username = %s and token=%s", (username, token))
            rows = cur.fetchone()
            if len(rows) == 0:
                auth_flag = False
            else:
                auth_flag = True
        except Exception as e:
            auth_flag = False
            print(connection_eror,e)
        finally:
            con.close()
        return auth_flag
    def check_authentication(self,username, token):
        auth_flag = False
        try:
            con = self.db.get_connection()
            try:

                cur = con.cursor()
                cur.execute("select * from authentication_session where username = %s and token=%s", (username, token))
                rows = cur.fetchone()
                if len(rows) == 0:
                    auth_flag = False
                else:
                    auth_flag = True
                con.close()
            except Exception as e:
                auth_flag = False
                print( e)
            finally:
                con.close()


        except Exception as e:
            print(connection_eror,e)
        return auth_flag
    def username_exist(self,username):
        try:
            try:
                con = self.db.get_connection()
                cur = con.cursor()
                cur.execute("select * from user_base ub, user_profile up where username = %s and up.user_id = ub.id",
                            (username,))

                if len(cur.fetchall()) == 0: return {"exist":False,"errors":[]}
            except Exception as e:
                print(e)
                return {"exist": False, "errors": ["database error"]}
            finally:
                cur.close()
                con.close()
        except Exception as e:
            print("connection error",e)
            return {"exist":False,"errors":["connection error"]}

    def getUserByUsername(self,username):
        try:
            try:
                user = CreateUser()
                con = self.db.get_connection()
                cur = con.cursor()
                cur.execute("select * from user_base ub, user_profile up where username = %s and up.user_id = ub.id",
                            (username,))
                row = {}
                for buff in cur:
                    c = 0
                    for col in cur.description:
                        row.update({str(col[0]): buff[c]})
                        c += 1
                user.id = row["id"]
                user.username = row["username"]
                user.password = row["password"]
                user.email = row["email"]
                user.first_name = row["first_name"]
                user.last_name = row["last_name"]
                user.is_active = row["is_active"]
                return_block = {"user": user, "errors": []}

            except:
                return_block = {"user": None, "errors": ["error"]}
            finally:
                cur.close()
                con.close()
        except Exception as e:
            print("connection error",e)
        return return_block

    def registrateUser(self, user):
        try:
            try:
                con = self.db.get_connection()
                cur = con.cursor()

            except Exception as e:
                print(e)
            finally:
                cur.close()
                con.close()
        except Exception as e:
            print(connection_eror)
