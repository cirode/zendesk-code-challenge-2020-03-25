import pdb
from expects import *
from unittest.mock import *
from pathlib import Path
import json


class AttributeDict(dict): 
	__getattr__ = dict.__getitem__
	__setattr__ = dict.__setitem__

def with_count(func):

	def wrap(*args,**kwargs):
		wrap.count +=1
		return func(*args,count=wrap.count,**kwargs)    
	wrap.count = 0
	return wrap

def get_test_data(table):
	file_dir = Path('.','specs','sample_files')
	file_name = f"{table}.json"
	with open(Path(file_dir, file_name)) as f:
		return json.loads(f.read())