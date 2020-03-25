import pdb
from expects import *
from unittest.mock import *
from pathlib import Path
import json


def get_test_data(table):
	file_dir = Path('.','specs','sample_files')
	file_name = f"{table}.json"
	with open(Path(file_dir, file_name)) as f:
		return json.loads(f.read())