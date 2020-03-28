from PyInquirer import style_from_dict, Token, prompt
import json

style = style_from_dict({
    Token.QuestionMark: '#E91E63 bold',
    Token.Selected: '#673AB7 bold',
    Token.Answer: '#2196f3 bold'
})


class ZearchGuiInterface():

	def startup_hook(self):
		print("Hi! I'm Zearch, the Zendesk Search Cli\n\n")
		print("Excuse me a sec while I get the minions to index those files. Back in a Jiffy!!\n")

	def run(self, database):
		print("Ok! Right to go!\n\n")
		next_command = ZearchMainMenu()
		while next_command is not None:
			next_command = next_command.run(database)
		self.shutdown_hook()

	def shutdown_hook(self):
		print("Byeee!")

class ZearchMainMenu():
	
	def __init__(self,known_commands=None):
		self._known_commands = known_commands or [SearchCommand(), QuitCommand()]

	def run(self, database):
		questions = [
		    {
		        'type': 'list',
		        'name': 'subcommand',
		        'message': 'What would you like me to attempt today?',
		        'choices': [{"name":command.describe(), "value":command} for command in self._known_commands]
		    }
		]
		return prompt(questions, style=style)["subcommand"]


class QuitCommand():

	def describe(self):
		return "Quit! End the madness!"

	def run(self,database):
		print('No worries! Catch you later!')

class SearchCommand():

	def describe(self):
		return "Set the minions a-searching"

	def run(self, database):
		print("Sure!... errm.. let's see here...\n")
		questions = [
		    {
		        'type': 'list',
		        'name': 'table_name',
		        'message': 'What table do you want to search on?',
		        'choices': [table.name for table in database.tables]
		    },
		]
		table_name = prompt(questions, style=style)["table_name"]
		questions = [
		    {
		        'type': 'list',
		        'name': 'field',
		        'message': 'What field?',
		        'choices': database.fields_for_table(table_name)
		    },
		]	
		field = prompt(questions, style=style)["field"]	
		questions = [
		    {
		        'type': 'input',
		        'name': 'value',
		        'message': f'What value for field "{field}"?'
		    },
		]
		value = prompt(questions, style=style)["value"]
		results = database.search(table_name, field, value, include_links=True)
		self._print_results(results)
		return ZearchMainMenu()

	def _print_results(self, results):
		print(json.dumps(results, indent=2)+"\n\n")
