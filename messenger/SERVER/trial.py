import json
import  datetime
import time

from DB.schemas.communication_schema import CommunicationSchema
cs = CommunicationSchema()
#

users = cs.searchFriends("user",None)
for u in users['users']:
    print(u)

# print(json.dumps({"auth_success":"'",'error':50401}))
# print(json.loads(json.dumps({"auth_success":"'",'error':50401}))['error']==50401)
