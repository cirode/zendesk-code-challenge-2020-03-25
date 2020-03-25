from specs.helper import *
from zearch import Config,Zearch,interface
from pathlib import Path
import tempfile

class TestZearch():

	def setup_method(self):
		self.interface = MagicMock(spec=interface.ZearchGuiInterface)
		self.db_schema = MagicMock()
		self.file_dir = MagicMock(spec=Path)
		self.config = MagicMock(spec=Config, interface=self.interface, database_schema=self.db_schema, file_dir=self.file_dir)
		self.zearch = Zearch(self.config)

	@patch('zearch.Database')
	def test_calls_interface_startup_hook_given_in_config(self, mock_database):
		self.zearch.run()
		expect(self.interface.startup_hook.mock_calls).to(contain(call()))

	@patch('zearch.Database')
	def test_creates_the_database_from_given_file_path(self, mock_database):
		self.zearch.run()
		expect(mock_database.from_file_dir.mock_calls).to(contain(call(file_dir = self.file_dir, schema= self.db_schema)))

	@patch('zearch.Database')
	def test_calls_interface_run(self, mock_database):
		self.zearch.run()
		expect(self.interface.run.mock_calls).to(contain(call(mock_database.from_file_dir.return_value)))
	