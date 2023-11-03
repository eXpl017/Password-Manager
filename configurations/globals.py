from utils.db_helpers.db_config import db_config
from rich.console import Console
import mariadb

console = Console()
db = db_config()
cursor = db.cursor()