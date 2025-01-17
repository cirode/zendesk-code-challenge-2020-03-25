from .interface import ZearchGuiInterface
from .database import Database
from .exceptions import InvalidConfigException
from pathlib import Path

class Config():
	def __init__(self, args):
		self._args = args

	@property
	def file_dir(self):
		path = Path(self._args.file_dir)
		if not path.is_dir():
			raise InvalidConfigException("File dir must exist")
		return path

	@property
	def database_schema(self):
		return {
			"organisations": {"primary_key": "_id"},
			"users": {"primary_key": "_id","foreign_keys": {'organization_id': {'name': 'organisation','reverse_name': 'user', 'table': 'organisations'}}},
			"tickets": {
				"primary_key": "_id",
				"foreign_keys": {
						'assignee_id': {'name': 'assignee', 'reverse_name': 'assigned_ticket', 'table': 'users'},
						'submitter_id': {'name': 'submitter','reverse_name': 'submitted_ticket', 'table': 'users'}
					}
				}
		}

	@property
	def interface(self):
		return ZearchGuiInterface()

class Zearch():
	def __init__(self, config):
		self._config=config

	def run(self):
		interface = self._config.interface
		interface.startup_hook()
		database = Database.from_file_dir(file_dir = self._config.file_dir, schema= self._config.database_schema)
		interface.run(database)