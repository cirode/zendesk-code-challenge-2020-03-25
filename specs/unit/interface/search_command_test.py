from specs.helper import *

from zearch.interface import SearchCommand,ZearchMainMenu
from zearch.database import Database
from collections import deque

class TestSearchCommand():

	def setup_method(self):
		self.database = MagicMock(spec=Database)
		self.database.search.return_value = {"result": "yeah"}

	def test_describe_returns_a_string_describing_the_command(self):
		expect(SearchCommand().describe().lower()).to(contain('search'))

	@patch('zearch.interface.prompt')
	def test_run_returns_a_main_menu_object(self, mock_prompt):
		mock_prompt.side_effect = [{"table_name": "table1"}, {"field": "_id"},{"value": "1"},{"links": True}]
		expect(SearchCommand().run(self.database)).to(be_a(ZearchMainMenu))

	@patch('zearch.interface.prompt')
	def test_run_calls_database_search_with_the_results_of_the_questions(self, mock_prompt):
		mock_prompt.side_effect = [{"table_name": "table1"}, {"field": "somethinginteresting"},{"value": "hmmmm"},{"links": 'woop'}]
		SearchCommand().run(self.database)
		expect(self.database.search.mock_calls).to(contain(call("table1", "somethinginteresting", "hmmmm", include_links='woop')))


	@patch('zearch.interface.prompt')
	def test_run_calls_database_fields_for_table_to_get_correct_fields_once_it_knows(self, mock_prompt):
		mock_prompt.side_effect = [{"table_name": "table1"}, {"field": "somethinginteresting"},{"value": "hmmmm"},{"links": True}]
		SearchCommand().run(self.database)
		expect(self.database.fields_for_table.mock_calls).to(contain(call("table1")))


	@patch('zearch.interface.prompt')
	def test_run_uses_the_returned_feilds_to_provide_options_for_fields_prompt(self, mock_prompt):
		answers = deque([{"table_name": "table1"}, {"field": "somethinginteresting"},{"value": "hmmmm"},{"links": True}])

		def prompt_listener(questions,style):
			if questions[0]['name'] == 'field':
				expect(questions[0]["choices"]).to(equal(self.database.fields_for_table.return_value))
			return answers.popleft()
		mock_prompt.side_effect = prompt_listener
		SearchCommand().run(self.database)
		expect(answers).to(be_empty)

	@patch('zearch.interface.json')
	@patch('zearch.interface.prompt')
	def test_run_pretty_prints_the_results(self, mock_prompt, mock_json):
		mock_prompt.side_effect = [{"table_name": "table1"}, {"field": "somethinginteresting"},{"value": "hmmmm"},{"links": True}]
		SearchCommand().run(self.database)
		expect(mock_json.dumps.mock_calls).to(contain(call(self.database.search.return_value, indent=2)))

