import sys
#sys.path.append('/home/ubuntu/Password Manager')
import base64
from Crypto.Cipher import AES
from Crypto import Random
import random
from hashlib import sha256
import string


def get_hash(s):

	return sha256(s.encode()).hexdigest()


def get_salt(length=16):

	chars = string.ascii_letters + string.digits
	return ''.join(random.choice(chars) for _ in range(length))


def encrypt(raw, masterkey):
	
	raw = raw.encode()
	IV = Random.new().read(AES.block_size)
	encryptor = AES.new(masterkey, AES.MODE_CBC, IV)
	padding = AES.block_size - len(raw) % AES.block_size
	raw +=  bytes([padding]) * padding
	data = IV + encryptor.encrypt(raw)
	return base64.b64encode(data).decode()


def decrypt(source, key):
	
	# enc = base64.b64decode(enc)
	# iv = enc[:16]
	# cipher = AES.new(masterkey, AES.MODE_CBC, iv)
	# return unpad(cipher.decrypt(enc[:16]))

	# IV = enc[:AES.block_size]
	# decryptor = AES.new(masterkey, AES.MODE_CBC, IV)
	# data = decryptor.decrypt(enc[AES.block_size:])
	# padding = data[-1]
	# if enc[-padding] != bytes([padding]) * padding:
	# 	raise ValueError("Invalid Padding!")
	# return data[:-padding]


	source = source.encode()
	source = base64.b64decode(source)
	IV = source[:AES.block_size]  # extract the IV from the beginning
	decryptor = AES.new(key, AES.MODE_CBC, IV)
	data = decryptor.decrypt(source[AES.block_size:])  # decrypt
	padding = data[-1]  # pick the padding value from the end; Python 2.x: ord(data[-1])
	if data[-padding:] != bytes([padding]) * padding:  # Python 2.x: chr(padding) * padding
		raise ValueError("Invalid padding...")
	return data[:-padding]  # remove the padding