# class Database():

# 	def __init__(self, **kwargs):
# 		pass

# 	def search(self,object_name,field,pattern):
# 		self._tables[object_name].find_by_field(field, pattern)

# 	@classmethod
# 	def from_file_dir(cls, file_dir):
# 		pass

# class DatabaseTable():

# 	@classmethod
# 	def load_from_file(cls, file_path):
# 		pass

# 	def __init__(index, *args, **kwargs):
# 		pass

# 	def find_by_field(field, pattern):
# 		return self._field_indexes[field].find(pattern)

import pdb
class BasicIndex():
	def __init__(self):
		self._index = {}
	
	def add(self,item,key):
		self._index[key] = self._index.get(key,None) or []
		self._index[key].append(item)

	def get(self,key):
		return self._index.get(key,[])