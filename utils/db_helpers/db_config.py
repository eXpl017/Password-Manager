#!/usr/bin/python3

import os
import sys
import mariadb

from rich import print as printc
from rich.console import Console
console = Console()


def db_config():
	try:
		conn = mariadb.connect(
			# user = os.environ.get('PM_USER'),
			# password = os.environ.get('PM_PASS'),
			# host = os.environ.get('PM_HOST'),
			# port = int(os.environ.get('PM_PORT'))

			user = 'root',
			password = '',
			host = 'localhost',
			port = 3306
		)
	except mariadb.Error as e:
		console.print_exception(show_locals=True)
		sys.exit(1)

	return conn