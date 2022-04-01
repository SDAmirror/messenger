import os

import rsa


def send_prepare(id):
    pub, priv = rsa.newkeys(1024)
    butes = pub._save_pkcs1_pem()
    with open(f'pkg/CLIENTSpackage/rsa_keys/pub{id}.pem','wb') as pubpem:
        print(butes)
        pubpem.write(butes)

send_prepare(1)

path = 'pkg/CLIENTSpackage/rsa_keys/{}'

try:
	os.remove(path.format('pub1.pem'))
except FileNotFoundError as e:
	print('file not found',e)
except OSError as error:
	print("There was an error.",error)