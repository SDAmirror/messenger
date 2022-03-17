import uuid


class BaseUser:
    username: str
    password: str
    email: str
    def __init__(self,username,password,email):
        self.email = email
        self.username = username
        self.password = password



class CreateUser(BaseUser):

    id : uuid.UUID
    first_name : str
    last_name : str
    is_active : bool

    def __init__(self):
        self.__class__.__name__ = "User"
class AuthenticatedUser:
    def __init__(self,user,token):
        self.user = user
        self.authentication_token = token
        self.__class__.__name__ = "AuthenticationUser"
