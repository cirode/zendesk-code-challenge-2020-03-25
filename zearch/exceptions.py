class ZearchException(Exception):
	pass

class DatabaseException(ZearchException):
	pass

class InvalidSchemaException(DatabaseException):
	pass

class InvalidConfigException(DatabaseException):
	pass