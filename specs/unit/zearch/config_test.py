from specs.helper import *
from zearch import Config, interface, exceptions
from pathlib import Path
import tempfile

class TestConfig(): 	
	def test_interface_returns_a_ZearchGUIInterface_instance(self):
		expect(Config({}).interface).to(be_a(interface.ZearchGuiInterface))

	def test_database_schema_returns_the_schema_for_these_files(self):
		schema = {
			"organisations": {"primary_key": "_id"},
			"users": {"primary_key": "_id"},
			"tickets": {"primary_key": "_id"}
		}
		expect(Config({}).database_schema).to(equal(schema))

	def test_file_dir_given_a_path_that_exists_returns_a_path_wrapped_file_dir(self):
		with tempfile.TemporaryDirectory() as tmpdir:
			args = AttributeDict({'file_dir': tmpdir})
			expect(Config(args).file_dir).to(equal(Path(tmpdir)))

	def test_file_dir_given_a_path_that_doesnt_exist_raises_an_invalid_config_exception(self):
		args = AttributeDict({'file_dir': 'prollydoesntexist'})
		expect(lambda : Config(args).file_dir).to(raise_error(exceptions.InvalidConfigException))