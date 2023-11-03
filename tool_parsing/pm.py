#!/usr/bin/python3

import argparse
import sys
sys.path.append('/home/ubuntu/Password Manager')
from getpass import getpass
from configurations.globals import console, db, cursor
from utils.encryption.aesutil import get_hash
from utils.db_helpers.add import add_entry
from utils.db_helpers.fetch import *
from utils.db_helpers.db_ops import search_in_db
from rich import print as printc


parser = argparse.ArgumentParser(description='Password Manager')

parser.add_argument('option', help="(a)dd / (e)xtract / (g)enerate")
parser.add_argument('-s', '--sitename', dest='sitename', help="Site Name")
parser.add_argument('-u', '--siteurl', dest='siteurl', help='Site URL')
parser.add_argument('-e', '--email', dest='email', help='Email-id')
parser.add_argument('-l', '--username', dest='username', help='Username')
parser.add_argument('-c', '--copy', action='store_true', help='Copy password to clipboard')

args = parser.parse_args()

def input_and_validate_masterpass():
	masterpass = get_masterpass()
	masterpass_hash = get_hash(masterpass)
	result = search_in_db(cursor, 'pm', 'secrets', '')
	hashed_mp, salt = result[0]
	if masterpass_hash != hashed_mp:
		#print(masterpass_hash, result)
		printc("[red][!] WRONG![/red]")
		return None

	return [masterpass, salt]

def main():
	if args.option in ['add','a']:
		if args.sitename==None or args.siteurl==None or args.username==None:
			if args.sitename==None:
				printc("[red][!] Please enter Sitename.[/red]")
			elif args.siteurl==None:
				printc("[red][!] Please enter Siteurl.[/red]")
			elif args.username==None:
				printc("[red][!] Please enter Username.[/red]")
			return

		if args.email==None:
			args.email=''

		res = input_and_validate_masterpass()
		print(res)
		if res is not None:
			add_entry(res[0][0], res[0][1], args.sitename, args.siteurl, args.email, args.username)

	if args.option in ['extract', 'e']:
		res = input_and_validate_masterpass()
		if res==None:
			printc("[red][!] WRONG![/red]")

		search = {}
		if args.sitename is not None:
			search['sitename'] = args.sitename
		if args.siteurl is not None:
			search['siteurl'] = args.siteurl
		if args.email is not None:
			search['email'] = args.email
		if args.username is not None:
			search['username'] = args.username

		if res is not None:
			fetch_pass(res[0][0], res[0][1], search, args.copy, True)

	if args.option in ['update', 'u']:
		res.input_and_validate_masterpass()



main()