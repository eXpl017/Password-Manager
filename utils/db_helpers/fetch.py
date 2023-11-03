import sys
#sys.path.append('/home/ubuntu/Password Manager')
from utils.db_helpers.add import compute_masterkey
from utils.db_helpers.db_ops import search_in_db
from utils.encryption.aesutil import encrypt, decrypt
from configurations.globals import console, db, cursor
from getpass import getpass
from rich import print as printc
from rich.table import Table
import pyperclip
import hashlib


def get_masterpass():
	
	masterpass = ""
	while (1):
		masterpass = getpass(prompt="Enter the MasterPassword: ")
		if masterpass==getpass(prompt="Re-enter MasterPassword: ") and masterpass!="":
			break
		printc("[yellow][+] Please try again![/yellow]")

	return masterpass


def fetch_pass(masterpass, salt, search, copy, decrypted_pass=False):
	
	result = search_in_db(cursor, 'pm', 'entries', search)

	if len(result) == 0:
		printc("[yellow][+] No results for this search query![/yellow]")
		return 

	if (decrypted_pass and len(result)>1) or (not decrypted_pass):
		table = Table(title='Results')
		table.add_column('Site Name')
		table.add_column('URL')
		table.add_column('Email')
		table.add_column('Username')
		table.add_column('Password')

		for i in result:
			table.add_row(i[0],i[1],i[2],i[3],"{HIDDEN}")

		console.print(table)
		return

	if decrypted_pass and len(result)==1:
		masterkey = compute_masterkey(masterpass, salt)
		decrypted = decrypt(result[0][4], masterkey)

	if copy:
		pyperclip.copy(decrypted.decode())
		printc("[green][+] Password copied to clipboard![/green]")
	else:
		printc(f"[green][-] Password here: {decrypted.decode()}[/green]")

	db.close()