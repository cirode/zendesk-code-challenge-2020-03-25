from specs.helper import *
from zearch.database import BasicIndex

class TestBasicIndex__get():

	def setup_method(self):
		self.index = BasicIndex()

	def test_given_key_that_doesnt_exist_returns_empty_list(self):
		expect(self.index.get('what')).to(equal([]))
		
	def test_given_string_value_that_exists_returns_indexed_item(self):
		value = 'value1'
		indexed_item = 12345
		self.index.add(indexed_item,value)
		expect(self.index.get(value)).to(equal([indexed_item]))

	def test_given_string_value_that_exists_multiple_times_returns_indexed_items(self):
		value= 'value1'
		indexed_item1 = 12345
		indexed_item2 = 9721
		self.index.add(indexed_item1,value)
		self.index.add(indexed_item2,value)
		expect(self.index.get(value)).to(equal([indexed_item1,indexed_item2]))

	def test_given_int_value_that_exists_returns_index_item(self):
		value = 65752
		indexed_item = 12345
		self.index.add(12345,value)
		expect(self.index.get(value)).to(equal([indexed_item]))
