from specs.helper import *
from zearch.database import Database, InvalidSchemaException, IndexedTable, Link, ReverseLink
from pathlib import Path
import tempfile


class TestDatabase__fields_for_table():
	def setup_method(self):
		self.table = MagicMock(spec=IndexedTable)
		self.database=Database()
		self.database.add(self.table)

	def test_fields_for_table_asks_the_table_for_the_fields(self):
		expect(self.database.fields_for_table(self.table.name)).to(equal(self.table.fields.return_value))