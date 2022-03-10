import json
import uuid
print(type(uuid.uuid4()),uuid.uuid4())
data = json.loads('{"name":"somename"}')
dumo = json.dumps({"name": "name"})
print(type(data),data)
print(type(dumo),dumo)