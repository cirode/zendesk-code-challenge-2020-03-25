# class UnknownCommand():
# 	def __init__(self, raw_command):
# 		self._raw_command = raw_command

# 	def exec(self):
# 		print(f'\nErrmmm.. not sure what you mean by "{self._raw_command}", try again!')
# 		return False

# class QuitCommand():
# 	def invocation(self):
# 		return 'quit'

# 	def describe():
# 		return "end the madness!"

# 	def exec(self,database):
# 		return True

# class SearchCommand():

# 	def __init__(self, input_cmd=input):
# 		self._input_cmd = input_cmd
	
# 	def invocation(self):
# 		pass

# 	def describe(self):
# 		return "set the minions a-searching"

# 	def exec(self, database):
# 		table = self._get_option(database.tables)
# 		field = self._get_option(fields)
# 		value = self._input_cmd("Enter search value")
# 		results = database.search(table, field, value)
# 		self._print_results(results)
# 		return False

# 	def _print_results(self, results):
# 		self._print_cmd(json.dumps(json_object, indent=2))

# 	def _get_table(self, tables):
# 		for i in range(len(tables)):
# 			print("Enter ")
# 		self._input_cmd()

# 	def _get_field(self, fields):
# 		for i in range(len(tables)):
# 			print("Enter ")
# 		self._input_cmd()


# class ZearchInterface():
# 	def __init__(self,known_commands=[SearchCommand(), QuitCommand()],print_func=print,input_func=input):
# 		self._input_cmd = input_cmd
# 		self._command_parser = command_parser
# 		self._known_commands = known_commands

# 	def startup_hook(self):
# 		print("Hi! I'm Zearch, the Zendesk Search Cli")

# 	def get_command(self):
# 		print("\n\nWhat do you want to do?:")
# 		for i in range(len(self._known_commands)):
# 			command = self._known_commands[i]
# 			invocation = command.invocation() or i
# 			print(f"- Type '{invocation}' to {command.describe()}\n")
# 		return self._parse(input())

# 	def shutdown_hook(self):
# 		print("Catchya Next Time!")

# 	def _parse(self, raw_command):
# 		try:
# 			command_index = int(raw_command)
# 			return self._known_commands[command_index]
# 		except ValueError,KeyError:
# 			return UnknownCommand(raw_command)
