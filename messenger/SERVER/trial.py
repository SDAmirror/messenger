import os

import rsa


# def send_prepare(id):
#     pub, priv = rsa.newkeys(1024)
#     butes = pub._save_pkcs1_pem()
#     with open(f'pkg/CLIENTSpackage/rsa_keys/pub{id}.pem','wb') as pubpem:
#         print(butes)
#         pubpem.write(butes)
#
# send_prepare(1)
#
# path = 'pkg/CLIENTSpackage/rsa_keys/{}'
#
# try:
# 	os.remove(path.format('pub1.pem'))
# except FileNotFoundError as e:
# 	print('file not found',e)
# except OSError as error:
# 	print("There was an error.",error)
a = ''
def generate_secret(id):
    global a
    (pub, priva) = rsa.newkeys(1024)

    a = pub._save_pkcs1_pem().decode('utf-8')
    print(a)
    # with open(f'pkg/CLIENTSpackage/rsa_keys/private{id}.pem', 'w') as priv_key_file:
    #     priv_key_file.write(priva.save_pkcs1().decode('utf-8'))

    with open(f'pkg/CLIENTSpackage/rsa_keys/public{id}.pem', 'w') as pub_key_file:
        pub_key_file.write(pub.save_pkcs1().decode('utf-8'))
    
    # with open(f'pkg/CLIENTSpackage/rsa_keys/private{id}.pem', 'r') as privatefile:
    #     keydata = privatefile.read()
    #     priv = rsa.PrivateKey.load_pkcs1(keydata,'PEM')



    with open(f'pkg/CLIENTSpackage/rsa_keys/public{id}.pem', 'r') as publicfile:
        pub = rsa.PublicKey.load_pkcs1(publicfile.read())
        print(pub)


generate_secret(4)