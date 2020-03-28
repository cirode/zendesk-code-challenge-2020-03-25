from specs.helper import *

from zearch.interface import ZearchMainMenu, style,QuitCommand
from zearch.database import Database


class TestZearchMainMenu__run():

	def setup_method(self):
		self.database = MagicMock(spec=Database)

	
	@patch('zearch.interface.SearchCommand')
	@patch('zearch.interface.QuitCommand')
	@patch('zearch.interface.prompt')
	def test_defaults_known_commands_to_search_and_quit(self,mock_prompt,quit_command,search_command):
		def prompt_listener(questions,style):
			expect([choice['value'] for choice in questions[0]["choices"]]).to(equal([search_command.return_value, quit_command.return_value]))
			return {"subcommand": None}
		mock_prompt.side_effect = prompt_listener
		ZearchMainMenu().run(self.database)
		#called once
		expect(len(mock_prompt.mock_calls)).to(equal(1))

	@patch('zearch.interface.prompt')
	def test_allows_the_provided_commands_to_define_their_own_description(self,mock_prompt):
		mock_command = MagicMock(spec=QuitCommand)
		mock_command.describe.return_value = "blah blah description"
		def prompt_listener(questions,style):
			expect([choice['name'] for choice in questions[0]["choices"]]).to(equal(["blah blah description"]))
			return {"subcommand": None}
		mock_prompt.side_effect = prompt_listener
		ZearchMainMenu(known_commands=[mock_command]).run(self.database)
		#called once
		expect(len(mock_prompt.mock_calls)).to(equal(1))

	@patch('zearch.interface.prompt')
	def test_returns_the_selected_command(self,mock_prompt):
		mock_command = MagicMock(spec=QuitCommand)
		def prompt_listener(questions,style):
			return {"subcommand": mock_command}
		mock_prompt.side_effect = prompt_listener
		expect(ZearchMainMenu().run(self.database)).to(equal(mock_command))