import sys
#sys.path.append('/home/ubuntu/Password Manager')
from utils.encryption.aesutil import encrypt, decrypt
from configurations.globals import console, db, cursor
from utils.db_helpers.db_ops import insert_in_table
from getpass import getpass
import hashlib


def compute_masterkey(masterpass, salt):

	#masterpass and salt are plain, not hashed ones. 
	#we just binary encode them now
	hashing_algo = "sha512"
	dk_len = 32
	iterations = 100000
	return hashlib.pbkdf2_hmac(hashing_algo, masterpass.encode(), salt.encode(), iterations, dk_len)


def add_entry(masterpass, salt, sitename, url, email, username):
	
	password = getpass(prompt="Enter the password for this site: ")
	masterkey = compute_masterkey(masterpass, salt)

	encrypted = encrypt(password, masterkey)

	entries_attr = '(sitename, siteurl, email, username, password)'
	values = (sitename, url, username, email, encrypted)
	insert_in_table(cursor, 'pm', 'entries', entries_attr, values)
