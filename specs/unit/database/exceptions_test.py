from specs.helper import *
from zearch.database import DatabaseException, InvalidSchemaException
from zearch import ZearchException

class TestDatabaseException():

	def test_it_is_derived_from_zearch_exception(self):
		expect(DatabaseException()).to(be_a(ZearchException))

class TestInvalidSchemaException():

	def test_it_is_derived_from_database_exception(self):
		expect(InvalidSchemaException()).to(be_a(DatabaseException))