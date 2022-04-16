import json
import time

import rsa

from pkg.MessageCtryptor import RSACryptor
from pkg.message_processor import Message_Sender
from pkg.message_processor import Message_Recirver

cryptor = RSACryptor(2)
cryptor.generate_RSA_keys()
sender = Message_Sender(cryptor)
reciv = Message_Recirver(cryptor)
servpub = cryptor.load_Public_key()


pub,priv = rsa.newkeys(1024)
cryptor.set_client_public_key(pub.save_pkcs1())
t64 = "Lorem Ipsum is simply dummy text of the printing and typesetting industry. Lorem Ipsum has been the industry's standard dummy text ever since the 1500s, when an unknown printer took a galley of type and scrambled it to make a type specimen book. It has survived not only five centuries, but also the leap into electronic typesetting, remaining essentially unchanged. It was popularised in the 1960s with the release of Letraset sheets containing Lorem Ipsum passages, and more recently with desktop publishing software like Aldus PageMaker including versions of Lorem Ipsum.Lorem Ipsum is simply dummy text of the printing and typesetting industry. Lorem Ipsum has been the industry's standard dummy text ever since the 1500s, when an unknown printer took a galley of type and scrambled it to make a type specimen book. It has survived not only five centuries, but also the leap into electronic typesetting, remaining essentially unchanged. It was popularised in the 1960s with the release of Letraset sheets containing Lorem Ipsum passages, and more recently with desktop publishing software like Aldus PageMaker including versions of Lorem Ipsum."
t62 = json.dumps({'non':None})



c = sender.send_message(2,t64)

ts = time.time()
m=''

# print(te





te = time.time()
print(te-ts,'\n',c)

