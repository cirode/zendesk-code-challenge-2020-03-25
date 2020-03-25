# from interface import ZearchInterface

# class Config():
# 	def __init__(self, args):
# 		pass

# 	@property
# 	def file_path(self):
# 		return args.file_path

# 	@property
# 	def database_schema(self):
# 		return {
# 			"organisations": {"primary_key": "_id"},
# 			"users": {"primary_key": "_id", "foreign_keys": {"organization_id": {"table":"organizations", "name": "organization"}}}
# 			"tickets": {"primary_key": "_id", "foreign_keys": {"assignee_id": {"table": "users", "name": "assignee"}, "submitter_id": {"table": "users", "name": "submitter"}}}
# 		}

# 	@property
# 	def interface(self):
# 		return ZearchInterface(known_commands=)

# class Zearch():
# 	def __init__(self, config):
# 		self._config=config

# 	def run(self):
# 		interface = self._config.interface
# 		interface.startup_hook()
# 		database = Database.from_file_dir(file_dir = self._config.file_dir, schema= self._config.database_schema)
# 		cause_exit = False
# 		while not cause_exit:
# 			command = interface.get_command()
# 			cause_exit = command.exec(self._database)
# 		interface.shutdown_hook()

class ZearchException(Exception):
	pass