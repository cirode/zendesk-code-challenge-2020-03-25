from specs.helper import *
from zearch.database import Database
import re


class TestDatabaseSearchManyIntegration__single_table():

	def setup_method(self):
		self.file_dir = Path('.','specs','sample_files')
		self.schema = {"users" : {"primary_key": "_id"}}
		self.database = Database.from_file_dir(file_dir=self.file_dir, schema=self.schema)
		self.all_data = get_test_data("users")

	def test_search_for_a_user_by_id_returns_correct_items(self):
		expected_result1 = self.all_data[10]
		expected_result2 = self.all_data[18]
		patterns = [expected_result1["_id"],expected_result2["_id"]]
		result = self.database.search_many("users","_id", patterns)
		expect(result).to(equal([expected_result1,expected_result2]))


	# def test_search_for_a_user_by_tag_returns_correct_item(self):
	# 	expected_result = get_test_data("users")[11]
	# 	result = self.database.search("users","tags", expected_result["tags"][2])
	# 	expect(result).to(equal([expected_result]))

	# def test_search_for_a_user_by_locale_returns_all_matching_items(self):
	# 	searched_locale = 'en-AU'
	# 	expected_results = [item for item in get_test_data("users") if item.get('locale') == searched_locale]
	# 	result = self.database.search("users","locale",searched_locale)
	# 	expect(result).to(equal(expected_results))

	# def test_search_for_a_user_with_a_non_existing_value_returns_empty_list(self):
	# 	result = self.database.search("users","_id", 'NOPE!')
	# 	expect(result).to(equal([]))
