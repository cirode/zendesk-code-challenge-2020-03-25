from specs.helper import *

from zearch.interface import ZearchGuiInterface
from zearch.database import Database



class TestZearchGuiInterface():

	def test_it_has_a_startup_hook_that_prints_things_to_stdout(self,capsys):
		ZearchGuiInterface().startup_hook()
		expect(capsys.readouterr().out).to(contain("I'm Zearch, the Zendesk Search Cli"))

	def test_it_has_a_shutdown_hook_that_prints_things_to_stdout(self,capsys):
		ZearchGuiInterface().shutdown_hook()
		expect(capsys.readouterr().out).to(contain("Bye"))



class TestZearchGuiInterface__run():

	def setup_method(self):
		self.database = MagicMock(spec=Database)

	@patch('zearch.interface.ZearchMainMenu')
	def test_passes_the_provided_database_to_the_main_menu(self,mock_main_menu):
		mock_main_menu.return_value.run.return_value = None
		ZearchGuiInterface().run(self.database)
		expect(mock_main_menu.return_value.run.mock_calls).to(contain(call(self.database)))

	@patch('zearch.interface.ZearchMainMenu')
	def test_it_calls_run_on_the_next_menu_object_returned(self,mock_main_menu):
		returned_menu = MagicMock(spec=ZearchGuiInterface)
		returned_menu.run.return_value = None
		mock_main_menu.return_value.run.return_value = returned_menu
		ZearchGuiInterface().run(self.database)
		expect(returned_menu.run.mock_calls).to(contain(call(self.database)))
