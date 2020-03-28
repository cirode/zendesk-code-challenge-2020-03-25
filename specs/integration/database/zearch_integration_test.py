from specs.helper import *
import json
from zearch import Zearch, Config

from zearch.interface import SearchCommand,QuitCommand
##
# NOTE: I'm not sure how to interact with the prompt for these, but if I stub out the prompt, I can drive the application
# Not Ideal, but it does excercise most of the application
class TestZearchIntegration():

	def setup_method(self):
		self.file_dir = Path('.','specs','sample_files')
		args = AttributeDict({'file_dir':self.file_dir})
		self.config = Config(args)
		self.zearch = Zearch(config=self.config)

	@patch('zearch.interface.prompt')
	def test_search_for_a_user_by_id_returns_correct_item(self, mock_prompt,capsys):
		## 
		# expected result
		expected_result = get_test_data("users")[2]
		assigned_tickets = list(filter(None,[ticket for ticket in get_test_data("tickets") if ticket.get('assignee_id') == expected_result['_id']]))
		submitted_tickets = list(filter(None,[ticket for ticket in get_test_data("tickets") if ticket.get('submitter_id') == expected_result['_id']]))
		org = [org for org in get_test_data("organisations") if org['_id'] == expected_result['organization_id']][0]
		expected_result['organisation'] = org
		for i,assigned_ticket in enumerate(assigned_tickets):
			expected_result[f'assigned_ticket_{i}'] = assigned_ticket
		for i,submitted_ticket in enumerate(submitted_tickets):
			expected_result[f'submitted_ticket_{i}'] = submitted_ticket


		search_field = '_id'
		questions_and_answer_functions = [
				# first do a search
				{'q': 'What would you like me to attempt today?',	'a': lambda qs,style: {qs[0]["name"]:SearchCommand()}},
				{'q': 'What table do you want to search on?', 		'a': lambda qs,style: {qs[0]["name"]:"users"}},
				{'q': 'What field?', 								'a': lambda qs,style: {qs[0]["name"]:search_field}},
				{'q': f'What value for field "{search_field}"?', 	'a':lambda qs,style: {qs[0]["name"]:expected_result[search_field]}},
				# then quit
				{'q':'What would you like me to attempt today?', 	'a':lambda qs,style: {qs[0]["name"]:QuitCommand()}}
			]
		asked_questions= []
		@with_count
		def mock_prompt_handler(questions,style,count):
			try:
				message = questions[0]['message']
				asked_questions.append(message)
				q_and_a = questions_and_answer_functions[count-1]
				#make sure we're answering the right question
				expect(q_and_a['q']).to(equal(message))
				return q_and_a['a'](questions,style)
			except IndexError:
				raise 'The application asked more questions than we have configured'
		mock_prompt.side_effect = mock_prompt_handler
		self.zearch.run()
		## double check we've got the right search
		expect(capsys.readouterr().out).to(contain(json.dumps([expected_result], indent=2)))