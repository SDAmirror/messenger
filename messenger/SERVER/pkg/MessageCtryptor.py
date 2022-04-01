import os

import rsa
#TODO client sends public key not server
class RSACryptor:
    def __init__(self,id):
        self.id = id
    def load_Private_key(self):
        return 1
    def load_Public_key(self):
        return 1

    def decrypt(self,message):
        key = self.load_Public_key()
        return message

    def encrypt(self,message):
        key = self.load_Private_key()
        return message


def delete_RSA_keys(id):
    path = 'CLIENTSpackage/rsa_keys/{}'
    try:
        os.remove(path.format(f'private{id}.pem'))
    except FileNotFoundError as e:
        print('file: {} not found'.format(path.format(f'private{id}.pem')), e)
    except OSError as error:
        print("There was an error.", error)
    try:
        os.remove(path.format(f'public{id}.pem'))
    except FileNotFoundError as e:
        print('file: {} not found'.format(path.format(f'public{id}.pem')), e)
    except OSError as error:
        print("There was an error.", error)
    try:
        os.remove(path.format(f'client_public{id}.pem'))
    except FileNotFoundError as e:
        print('file: {} not found'.format(path.format(f'client_public{id}.pem')), e)
    except OSError as error:
        print("There was an error.", error)

def send_prepare(id):
    pub, priv = rsa.newkeys(1024)
    butes = pub._save_pkcs1_pem()
    with open(f'CLIENTSpackage/rsa_keys/pub{id}.pem','wb') as pubpem:
        print(butes)
        pubpem.write(butes)



