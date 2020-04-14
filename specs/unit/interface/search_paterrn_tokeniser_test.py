from specs.helper import *
from zearch.interface import SearchPatternTokeniser


class TestSearchPatternTokeniser__parse():

	def test_single_string_returns_list_with_string(self):
		expect(SearchPatternTokeniser().parse('thingtobeparsed')).to(equal(['thingtobeparsed']))

	def test_single_int_returns_list_with_string(self):
		expect(SearchPatternTokeniser().parse(3)).to(equal(['3']))

	def test_with_OR_returns_both_strings_as_list(self):
		expect(SearchPatternTokeniser().parse('thingtobeparsed OR thisone')).to(equal(['thingtobeparsed', 'thisone']))