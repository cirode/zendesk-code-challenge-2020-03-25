from specs.helper import *
from zearch.database import Database
import re


class TestDatabaseSearchIntegration__single_table():

	def setup_method(self):
		self.file_dir = Path('.','specs','sample_files')
		self.schema = {"users" : {"primary_key": "_id"}}
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

	def test_search_for_a_user_with_a_non_existing_value_returns_empty_list(self):
		result = self.database.search("users","_id", 'NOPE!')
		expect(result).to(equal([]))



class TestDatabaseSearchIntegration__multiple_tables():

	def setup_method(self):
		self.file_dir = Path('.','specs','sample_files')
		self.schema = {
			"users" : 
				{
					"primary_key": "_id", 
					"foreign_keys": {'organization_id': {'name': 'organisation','reverse_name': 'user', 'table': 'organisations'}}
				}, 
			"organisations":
				{
					"primary_key": "_id"
				},
			"tickets": 
				{
					"primary_key": "_id",
					"foreign_keys": {
						'assignee_id': {'name': 'assignee', 'reverse_name': 'assigned_ticket', 'table': 'users'},
						'submitter_id': {'name': 'submitter','reverse_name': 'submitted_ticket', 'table': 'users'}
					}
				}
			}
		self.database = Database.from_file_dir(file_dir=self.file_dir, schema=self.schema)

	### include_links False

	def test_include_links_false_search_for_a_user_by_id_returns_correct_item(self):
		expected_result = get_test_data("users")[10]
		result = self.database.search("users","_id", expected_result["_id"])
		expect(len(result)).to(equal(1))
		expect(result[0]['_id']).to(equal(expected_result['_id']))

	def test_include_links_false_search_for_user_with_include_links_set_to_false_returns_just_the_user(self):
		expected_result = get_test_data("users")[11]
		result = self.database.search("users","tags", expected_result["tags"][2], include_links=False)
		expect(result).to(equal([expected_result]))


	### include_links True

	def test_include_links_true_returns_the_user_with_assigned_tickets_using_provided_reverse_name(self):		
		expected_result =  get_test_data("users")[0]
		assigned_tickets = list(filter(None,[ticket for ticket in get_test_data("tickets") if ticket.get('assignee_id') == expected_result['_id']]))
		result = self.database.search("users","_id", expected_result["_id"], include_links=True)[0]
		result_assigned_tickets = [value for attr,value in result.items() if re.match('^assigned_ticket_.*',attr)]
		expect(result_assigned_tickets).to(equal(assigned_tickets))

	def test_include_links_true_returns_the_user_with_submitted_tickets(self):
		expected_result =  get_test_data("users")[0]
		submitted_tickets = list(filter(None,[ticket for ticket in get_test_data("tickets") if ticket.get('submitter_id') == expected_result['_id']]))
		result = self.database.search("users","_id", expected_result["_id"], include_links=True)[0]
		result_submitted_tickets = [value for attr,value in result.items() if re.match('^submitted_ticket_.*',attr)]
		expect(result_submitted_tickets).to(equal(submitted_tickets))

	def test_include_links_true_returns_the_user_with_linked_organisation(self):
		expected_result =  get_test_data("users")[0]
		self.org = [org for org in get_test_data("organisations") if org['_id'] == expected_result['organization_id']][0]
		result = self.database.search("users","_id", expected_result["_id"], include_links=True)[0]
		result_org = [value for attr,value in result.items() if re.match('^organisation$',attr)]
		expect(result_org).to(equal([self.org]))
