from specs.helper import *
from zearch.database import Database, InvalidSchemaException, IndexedTable, Link, ReverseLink
from pathlib import Path
import tempfile


##
# Technically an integration test as not mocking. The mocking was becoming pretty arduous, 
# This should tell me something about the modelling
# TODO: Look at this
class TestDatabase__from_file_dir():

	def setup_method(self):
		self.file_dir = Path('.','specs','sample_files')

	## Schema Testing
	def test_when_given_a_dir_that_does_not_contain_the_files_listed_by_schema_raises_invalid_schema_exception(self):
		schema = {"woops":{"primary_key":"_id"}}
		expect(lambda : Database.from_file_dir(self.file_dir, schema)).to(raise_error(InvalidSchemaException))


	def test_when_given_a_dir_that_does_contain_the_files_listed_by_schema_returns_database_with_tables(self):
		schema = {"tickets":{"primary_key":"_id"}, "users":{"primary_key":"_id"}}
		database = Database.from_file_dir(self.file_dir, schema)
		expect([t.name for t in database.tables]).to(equal(["tickets","users"]))

	### With foreign key info in schema
	def test_when_table_has_foreign_key_adds_reverse_link_to_other_table(self):
		schema = {"tickets":{"primary_key":"_id","foreign_keys":{"submitter_id": {"name": "submitter", "reverse_name": "submitted_ticket", "table": "users"}}}, "users":{"primary_key":"_id"}}
		database = Database.from_file_dir(self.file_dir, schema)
		users_table = [t for t in database.tables if t.name == 'users'][0]
		expect(users_table.linked_from()).to(equal([ReverseLink(key="submitter_id", name="submitted_ticket",table="tickets")]))

	def test_when_table_has_foreign_key_in_reverse_order_adds_reverse_link_to_other_table(self):
		schema = {"users":{"primary_key":"_id"},"tickets":{"primary_key":"_id","foreign_keys":{"submitter_id": {"name": "submitter", "reverse_name": "submitted_ticket", "table": "users"}}}}
		database = Database.from_file_dir(self.file_dir, schema)
		users_table = [t for t in database.tables if t.name == 'users'][0]
		expect(users_table.linked_from()).to(equal([ReverseLink(key="submitter_id", name="submitted_ticket",table="tickets")]))

class TestDatabase__fields_for_table():
	def setup_method(self):
		self.table = MagicMock(spec=IndexedTable)
		self.database=Database()
		self.database.add(self.table)

	def test_fields_for_table_asks_the_table_for_the_fields(self):
		expect(self.database.fields_for_table(self.table.name)).to(equal(self.table.fields.return_value))