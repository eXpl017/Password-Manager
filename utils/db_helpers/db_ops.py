import sys
from configurations.globals import console
from rich import print as printc
import mariadb

from utils.db_helpers.db_config import db_config
db = db_config()


def create_db(cursor, db_name):
	try:
		create_cmd = f"CREATE DATABASE IF NOT EXISTS {db_name}"
		cursor.execute(create_cmd)
		printc("[green][+] DB '{db_name}' created![/green]")
	except mariadb.Error as e:
		printc("[red][!] Error while creating DB![/red]")
		console.print_exception(show_locals=True)
		sys.exit(1)


def create_table(cursor, table_name, attr_tuple):
	
	try:
		create_cmd = f"CREATE TABLE IF NOT EXISTS {table_name}{attr_tuple}"
		cursor.execute(create_cmd)
		printc(f"[green][+] Table '{table_name}' created![/green]")
	except mariadb.Error as e:
		printc("[red][!] Error while creating Table!")
		console.print_exception(show_locals=True)
		sys.exit(0)


def insert_in_table(cursor, db_name, table_name, attr_tuple, values):

	try:
		insert_cmd = f"INSERT INTO {db_name}.{table_name} {attr_tuple} VALUES {values}"
		print(insert_cmd)
		cursor.execute(insert_cmd)
		cursor.connection.commit()
		printc("[green][+] Added keys to database![/green]")
	except mariadb.Error as e:
		printc("[red][!] Error while inserting values to table!")
		console.print_exception(show_locals=True)
		sys.exit(0)
	return


def search_in_db(cursor, db_name, table_name, search):

	search_cmd = f"SELECT * FROM {db_name}.{table_name}"
	try:
		if len(search) == 0:
			search_cmd = search_cmd
		else:
			search_cmd += " WHERE "
			for i in search:
				search_cmd += f"{i}='{search[i]}' AND "
			search_cmd = search_cmd[:-5]

		cursor.execute(search_cmd)
		result = cursor.fetchall()

	except mariadb.Error as e:
		printc("[red][+] Unable to fetch results / Table empty![/red]")
		console.print_exception(show_locals=True)
		sys.exit(0)

	return result


def update_in_db (cursor, db_name, table_name, attr, value):
	pass