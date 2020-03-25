from specs.helper import *
from zearch.exceptions import DatabaseException, InvalidSchemaException,ZearchException,InvalidConfigException

class TestDatabaseException():

	def test_it_is_derived_from_zearch_exception(self):
		expect(DatabaseException()).to(be_a(ZearchException))

class TestInvalidSchemaException():

	def test_it_is_derived_from_database_exception(self):
		expect(InvalidSchemaException()).to(be_a(DatabaseException))


class TestInvalidConfigException():
	def test_it_is_derived_from_zearch_exception(self):
		expect(InvalidConfigException()).to(be_a(ZearchException))