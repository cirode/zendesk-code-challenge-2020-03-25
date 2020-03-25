from collections.abc import Sequence
from . import ZearchException
from pathlib import Path
import os


class DatabaseException(ZearchException):
	pass

class InvalidSchemaException(DatabaseException):
	pass


class Database():

	def __init__(self, tables):
		self.tables = tables

	def search(self,object_name,field,pattern):
		self._tables[object_name].find_by_field(field, pattern)

	@classmethod
	def from_file_dir(cls, file_dir, schema):
		files = file_dir.glob('*.json')
		file_index = dict([(cls._file_name_without_extension(file_path), file_path) for file_path in files])
		tables = []
		for table_name, table_schema in schema.items():
			file_path = file_index.get(table_name,None)
			if file_path is None:
				raise InvalidSchemaException(f"Expected {table_name}.json to exist, but not in directory")
			tables.append(IndexedTable.load_from_file(table_name, table_schema,file_path))
		return cls(tables)

	@classmethod
	def _file_name_without_extension(cls, path):
		base = os.path.basename(path)
		return os.path.splitext(base)[0]

class IndexedTable():

	@classmethod
	def load_from_file(cls, name, schema, file_path):
		pass

	def __init__(index, *args, **kwargs):
		pass

	def find_by_field(field, pattern):
		return self._field_indexes[field].find(pattern)

class BasicIndex():
	def __init__(self):
		self._index = {}
	
	def add(self,item,key):
		if not self._is_non_str_sequence(key):
			key = [key]
		for k in key:
			self._index[k] = self._index.get(k,None) or []
			self._index[k].append(item)

	def get(self,key):
		return self._index.get(key,[])

	def _is_non_str_sequence(self,obj):
		return isinstance(obj, Sequence) and not isinstance(obj, str)

