from specs.helper import *

from zearch.interface import QuitCommand
from zearch.database import Database

class TestQuitCommand():

	def setup_method(self):
		self.database = MagicMock(spec=Database)

	def test_describe_returns_a_string_describing_the_command(self):
		expect(QuitCommand().describe()).to(contain('Quit'))

	def test_run_returns_none_as_this_causes_the_cli_to_quit(self):
		expect(QuitCommand().run(self.database)).to(be_none)