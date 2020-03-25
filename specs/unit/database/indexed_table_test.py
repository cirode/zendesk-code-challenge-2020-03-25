from specs.helper import *
from zearch.database import IndexedTable, InvalidSchemaException
from pathlib import Path
import json

class TestIndexedTable__from_file():


	def setup_method(self):
		self.file_dir = Path('.','specs','sample_files')
		self.schema = {"primary_key":"_id"}
		self.file_name = "users.json"
		self.first_item = get_test_data("users")[0]
		self.second_item = get_test_data("users")[1]

	#adding items to table
	@patch('zearch.database.IndexedTable.__init__', return_value=None)
	@patch('zearch.database.IndexedTable.add', return_value=None)
	def test_it_creates_the_table_with_the_table_schema(self, mock_table_constructor, mock_table_add):
		table = IndexedTable.from_file(file_path=Path(self.file_dir,self.file_name), name="users",schema=self.schema)
		expect(IndexedTable.__init__.mock_calls).to(contain(call(name="users",schema=self.schema)))

	@patch('zearch.database.IndexedTable.__init__', return_value=None)
	@patch('zearch.database.IndexedTable.add', return_value=None)
	def test_it_calls_add_for_each_item_in_the_file(self,mock_table_constructor,mock_table_add):
		table = IndexedTable.from_file(file_path=Path(self.file_dir,self.file_name), name="users",schema=self.schema)
		expect(table.add.mock_calls).to(contain(call(self.first_item)))
		expect(table.add.mock_calls).to(contain(call(self.second_item)))


	
class TestIndexedTable__add():

	def setup_method(self):
		self.file_dir = Path('.','specs','sample_files')
		self.schema = {"primary_key":"_id"}
		self.file_name = "users.json"
		self.table = IndexedTable(name="users",schema=self.schema)
		self.first_item = get_test_data("users")[0]

	#schema testing	
	def test_when_schema_primary_key_doesnt_exist_in_table_raises_invalid_schema_exception(self):
	 	schema = {"primary_key":"whatnow?"}
	 	table = IndexedTable(name="users", schema=schema)
	 	expect(lambda : table.add(self.first_item)).to(raise_error(InvalidSchemaException))

	
	#loading and indexing
	@patch('zearch.database.BasicIndex')
	def test_when_schema_primary_key_does_exist_in_table_creates_an_index_per_column_in_file(self,mock_index_cls):
		self.table.add(self.first_item)
		num_fields = 19
		mock_constructor_calls = [call for call in mock_index_cls.mock_calls if call == call()]
		expect(len(mock_constructor_calls)).to(equal(num_fields))

	@patch('zearch.database.BasicIndex')
	def test_when_schema_primary_key_does_exist_in_table_hydrates_the_index_with_values_from_that_column(self,mock_index_cls):
		self.table.add(self.first_item)
		indexes = self.table.indexes
		for field in ['_id', 'tags','organization_id']:
			expect(indexes[field].add.mock_calls).to(contain(call(self.first_item,self.first_item[field])))


class TestIndexedTable__fields():
	def setup_method(self):
		self.file_dir = Path('.','specs','sample_files')
		self.schema = {"primary_key":"_id"}
		self.file_name = "users.json"
		self.table = IndexedTable(name="users",schema=self.schema)
		self.first_item = get_test_data("users")[0]
		self.table.add(self.first_item)

	def test_fields_returns_all_fields_for_this_table(self):
		expect(self.table.fields()).to(equal(self.first_item.keys()))

