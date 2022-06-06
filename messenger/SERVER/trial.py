import hashlib

hasspassword = hashlib.new("sha256")
hasspassword.update("user.password".encode())

password = hasspassword.hexdigest()
print(password,type(password))