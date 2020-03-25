from specs.helper import *
from zearch.database import Database, InvalidSchemaException, IndexedTable
from pathlib import Path
import tempfile


class TestDatabase__from_file_dir():

	
	def setup_method(self):
		self.file_dir = Path('.','specs','sample_files')

	## Schema Testing
	def test_when_given_a_dir_that_does_not_contain_the_files_listed_by_schema_raises_invalid_schema_exception(self):
		schema = {"woops":{"primary_key":"_id"}}
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

		expect(index_table_mock.from_file.mock_calls).to(contain(call(name="users",schema=schema["users"],file_path=Path(self.file_dir,"users.json"))))
		expect(index_table_mock.from_file.mock_calls).to(contain(call(name="organisations",schema=schema["organisations"],file_path=Path(self.file_dir,"organisations.json"))))


class TestDatabase__fields_for_table():
	def setup_method(self):
		self.table = MagicMock(spec=IndexedTable)
		self.database=Database(tables=[self.table])

	def test_fields_for_table_asks_the_table_for_the_fields(self):
		expect(self.database.fields_for_table(self.table.name)).to(equal(self.table.fields.return_value))