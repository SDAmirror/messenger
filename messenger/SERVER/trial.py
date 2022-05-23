import json
import  datetime
import time

from DB.schemas.message_shema import MessageSchema
ms = MessageSchema()
#

messages = ms.send_unsent_messages('user3',1)

c = 1
for i in messages['messages']:
    print(i.__dict__)
    if c % 2 == 0:
        r = ms.updateSent(i.id,1)
        print(r)
    c+=1
#

# print(json.dumps({"auth_success":"'",'error':50401}))
# print(json.loads(json.dumps({"auth_success":"'",'error':50401}))['error']==50401)
