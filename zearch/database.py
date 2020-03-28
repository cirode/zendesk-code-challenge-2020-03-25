from collections.abc import Sequence
from .exceptions import ZearchException,InvalidSchemaException
from pathlib import Path
from collections import namedtuple
import os
import json
from copy import deepcopy

class Database():

	def __init__(self):
		self._table_index = {}

	def search(self,object_name,field,pattern, include_links=False):
		table = self._table_index[object_name]
		results = deepcopy(table.find_by_field(field, pattern))
		if include_links:
			return [self._set_reverse_linked_data(self._set_linked_data(result, table), table) for result in results]
		return results
			

	def fields_for_table(self, table_name):
		return self._table_index[table_name].fields()

	def add(self,table):
		self._table_index[table.name] = table

	def get_table(self,table_name):
		return self._table_index.get(table_name)

	def _set_reverse_linked_data(self, result, table):
		for reverse_link in table.linked_from():
			linked_table = self._table_index.get(reverse_link.table)
			results = linked_table.find_by_field(reverse_link.key,result[table.pk])
			for i,rev_linked_result in enumerate(results):
				result[f'{reverse_link.name}_{i}'] = rev_linked_result
		return result

	def _set_linked_data(self, result, table):
		for link in table.links_to():
			linked_table = self._table_index[link.table]
			linked_objects = linked_table.find_by_field(linked_table.pk,result.get(link.key))
			if len(linked_objects) > 0:
				result[link.name] = linked_objects[0]
		return result

	@property
	def tables(self):
		return list(self._table_index.values())
		
	@classmethod
	def from_file_dir(cls, file_dir, schema):
		files = file_dir.glob('*.json')
		file_index = dict([(cls._file_name_without_extension(file_path), file_path) for file_path in files])
		database = cls()
		for table_name in schema.keys():
			cls._create_table(table_name, schema, file_index,database)
		return database

	@classmethod
	##
	# Recursively go through and add the tables. Recursive so that the links can be formed in two directions
	##
	def _create_table(cls, table_name, schema, file_index,database):
		existing_table = database.get_table(table_name)
		if existing_table is not None:
			return existing_table

		file_path = file_index.get(table_name,None)
		if file_path is None:
			raise InvalidSchemaException(f"Expected {table_name}.json to exist, but not in directory")
		table = IndexedTable.from_file(file_path=file_path,name=table_name, schema=schema[table_name])
		database.add(table)
		for link in table.links_to():
			linked_table = cls._create_table(link.table, schema, file_index, database)
			linked_table.add_reverse_link(name=link.reverse_name,table_name=table.name, foreign_key=link.key)
		return table


	@classmethod
	def _file_name_without_extension(cls, path):
		base = os.path.basename(path)
		return os.path.splitext(base)[0]


ReverseLink = namedtuple("ReverseLink", field_names=['name','table','key','optional'], defaults=[False])
Link = namedtuple("Link", field_names=['name','table','key','reverse_name','optional'], defaults=[False])

class IndexedTable():		

	def __init__(self, name,schema):
		self._name = name
		self._schema = schema
		self._indexes = {}
		self._reverse_links = {}
		self._links = {}
		self._find_links()

	def add(self,item):
		if self.pk not in item:
			raise InvalidSchemaException(f"Expected {self.name}.json contain {self.pk} field but did not")	

		for key, value in item.items():
			self.indexes[key] = self.indexes.get(key,None) or BasicIndex()
			self.indexes[key].add(item, value)

	def fields(self):
		return self.indexes.keys()

	def find_by_field(self,field, pattern):
		return self.indexes[field].get(pattern)

	def add_reverse_link(self, name,table_name, foreign_key):
		if name in self._reverse_links:
			raise InvalidSchemaException(f"Multiple reverse links called '{name}' detected in table '{self._name}'")
		self._reverse_links[name] = ReverseLink(name=name,table=table_name, key= foreign_key)

	def linked_from(self):
		return list(self._reverse_links.values())

	def links_to(self):
		return list(self._links.values())

	@property
	def name(self):
		return self._name

	@property
	def indexes(self):
		return self._indexes

	@property
	def pk(self):
		return self._schema["primary_key"]

	def _find_links(self):
		for foreign_key, info in self._schema.get("foreign_keys",{}).items():
			name = info["name"]
			if name in self._links:
				raise InvalidSchemaException(f"Multiple links called '{name}' detected in table '{self._name}'")
			self._links[name] = Link(key=foreign_key,**info)

	@classmethod
	def from_file(cls,file_path,name, schema):
		table = cls(name=name,schema=schema)
		with open(file_path) as f:
			data = json.loads(f.read())
			for item in data:
				table.add(item)
		return table

class BasicIndex():
	def __init__(self):
		self._index = {}
	
	def add(self,item,key):
		if not self._is_non_str_sequence(key):
			key = [key]
		for k in key:
			k = str(k)
			self._index[k] = self._index.get(k,None) or []
			self._index[k].append(item)

	def get(self,key):
		return self._index.get(str(key),[])

	def _is_non_str_sequence(self,obj):
		return isinstance(obj, Sequence) and not isinstance(obj, str)

