from collections.abc import Sequence 

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