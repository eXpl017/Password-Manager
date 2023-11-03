#!/usr/bin/python3

import sys
sys.path.append('/home/ubuntu/Password Manager')
from configurations.globals import console, db, cursor
from utils.db_helpers.db_ops import create_db, create_table, insert_in_table
from utils.db_helpers.fetch import get_masterpass
from utils.encryption.aesutil import get_hash, get_salt
from rich import print as printc
import mariadb


def config():
	
	create_db(cursor, 'pm')
	printc("[green][+] New DB config created![/green]")

	cursor.execute("USE pm")
	printc("[green][+] Using the databse 'pm'[/green]")

	secrets_colmns = r'(masterpass_hash TEXT NOT NULL, device_secret TEXT NOT NULL)'
	entries_colmns = r'(sitename TEXT NOT NULL, siteurl TEXT NOT NULL, email TEXT, username TEXT, password TEXT NOT NULL)'
	create_table(cursor, "secrets", secrets_colmns)
	create_table(cursor, "entries", entries_colmns)

	masterpass = get_masterpass()
	masterpass_hash = get_hash(masterpass)
	printc("[green][+] Hash for MasterPassword generated![/green]")

	salt = get_salt()
	printc("[green][+] Device secret/Salt generated![/green]")

	secrets_attr = '(masterpass_hash, device_secret)'
	values = (masterpass_hash, salt)
	insert_in_table(cursor, 'pm', 'secrets', secrets_attr, values)

	printc("[green][+] Configuration done![/green]")

	db.close()


config()