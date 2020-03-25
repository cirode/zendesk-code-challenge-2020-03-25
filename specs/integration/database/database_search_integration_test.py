from specs.helper import *
from zearch.database import Database


class TestDatabaseSearchIntegration():

	def setup_method(self):
		self.file_dir = Path('.','specs','sample_files')
		self.schema = {"users" : {"primary_key": "_id"}, "organisations": {"primary_key": "_id"}, "tickets": {"primary_key": "_id"}}
		self.database = Database.from_file_dir(file_dir=self.file_dir, schema=self.schema)

	def test_search_for_a_user_by_id_returns_correct_item(self):
		expected_result = get_test_data("users")[10]
		result = self.database.search("users","_id", expected_result["_id"])
		expect(result).to(equal([expected_result]))


	def test_search_for_a_user_by_tag_returns_correct_item(self):
		expected_result = get_test_data("users")[11]
		result = self.database.search("users","tags", expected_result["tags"][2])
		expect(result).to(equal([expected_result]))

	def test_search_for_a_user_by_locale_returns_all_matching_items(self):
		searched_locale = 'en-AU'
		expected_results = [item for item in get_test_data("users") if item.get('locale') == searched_locale]
		result = self.database.search("users","locale",searched_locale)
		expect(result).to(equal(expected_results))
