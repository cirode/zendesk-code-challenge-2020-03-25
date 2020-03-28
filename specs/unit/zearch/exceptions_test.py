from specs.helper import *
from zearch.exceptions import  InvalidSchemaException,ZearchException,InvalidConfigException

class TestInvalidSchemaException():

	def test_it_is_derived_from_zearch_exception(self):
		expect(InvalidSchemaException()).to(be_a(ZearchException))


class TestInvalidConfigException():
	def test_it_is_derived_from_zearch_exception(self):
		expect(InvalidConfigException()).to(be_a(ZearchException))