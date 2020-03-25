from specs.helper import *
from zearch.database import Database, InvalidSchemaException
from pathlib import Path
import shutil
import tempfile


class TestDatabase__from_file_dir():

	
	def setup_method(self):
		self.file_dir = Path('.','specs','sample_files')

	## Schema Testing
	def test_when_given_a_dir_that_does_not_contain_the_files_listed_by_schema_raises_invalid_schema_exception(self):
		schema = {"woops":{"primary_key":"_id"}}
		expect(lambda : Database.from_file_dir(self.file_dir, schema)).to(raise_error(InvalidSchemaException))

	def test_when_schema_primary_key_doesnt_exist_in_table_raises_invalid_schema_exception(self):
		schema = {"woops":{"primary_key":"whatnow?"}}
		expect(lambda : Database.from_file_dir(self.file_dir, schema)).to(raise_error(InvalidSchemaException))


	## Creation of IndexedTables
	@patch('zearch.database.IndexedTable')
	def test_when_given_a_dir_that_does_contain_the_files_listed_by_schema_returns_database_with_tables(self, index_table_mock):
		schema = {"users":{"primary_key":"_id"}, "organisations":{"primary_key":"_id"}}
		database = Database.from_file_dir(self.file_dir, schema)
		expect(database.tables).to(equal([index_table_mock.from_file.return_value,index_table_mock.from_file.return_value]))

	@patch('zearch.database.IndexedTable')
	def test_when_given_a_dir_that_does_contain_the_files_listed_by_schema_created_tables_with_the_schemas_and_files(self,index_table_mock):
		schema = {"users":{"primary_key":"_id"},"organisations":{"primary_key":"_id"}}
		database = Database.from_file_dir(self.file_dir, schema)

		expect(index_table_mock.from_file.mock_calls).to(contain(call("users",schema["users"],Path(self.file_dir,"users.json"))))
		expect(index_table_mock.from_file.mock_calls).to(contain(call("organisations",schema["organisations"],Path(self.file_dir,"organisations.json"))))
