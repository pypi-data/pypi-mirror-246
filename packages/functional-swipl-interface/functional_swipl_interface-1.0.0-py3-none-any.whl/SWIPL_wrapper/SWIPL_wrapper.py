from swiplserver import PrologMQI # https://www.swi-prolog.org/packages/mqi/prologmqi.html
from os import path, remove

TEMP = "temp_knowledge_base.pro"

# This wrapper class is used to make the SWIPL PrologMQI easier to use
# Only two functions are central to this class: load and query
# SWIPL_wrapper.load() takes a file location and loads it into the knoledge base.
# SWIPL_wrapper.query() takes a prolog query as a string and tests it against the knoledge base.
#
# All other functions simply wrap around query() and load() to improve usability.
# - queries() simply runs query on a list of prolog queries and returns the results as a list.
# - result_query() and result_queries() are the same as queries and query except it handles unwrapping assuming you
#   passed in a Result variable into the binding. This handles the removal of the list and dict to only give you the
#   first binding of result.
# - validate_query and validate_queries take in the name(s) of a relation already in the knoledge base and
#   value(s) to pass into that relation. It then returns tuple(s) of the value and the truthiness of if the value.
# - add_fact(s)() adds the given binding to the knoledge base (behind the scenes, creates or updates a temperary prolog file).
# - close() closes the prolog thread, prolog server, and deletes the temperary knoledge base file. This should be
#   called at the end of the program. If you do not call this, bugs and slowdowns may arise because any relations added
# 	in add_fact(s) will persist.
class SWIPL_wrapper:
	def __init__(self) -> None:
		self.mqi = PrologMQI()
		self.prolog_thread = self.mqi.create_thread()

	def load_file(self, file_path: str):
		try :
			self.prolog_thread.query(f"['{file_path}'].")
		except Exception as e:
			print(e)
			Exception("Failed to load prolog script")
		return self

	def query(self, query:str):
		return self.prolog_thread.query(query)

	def queries(self, querys:list) -> list:
		return [self.query(query) for query in querys]

	def result_query(self, query:str):
		result = self.query(query)
		if type(result) != list:
			print(result)
			Exception("Unexspected Prolog Return Type")
		else:
			return [*set(i["Result"] for i in result)]

	def result_queries(self, querys:list) -> list:
		return [self.result_query(query) for query in querys]

	def validate_query(self, function:str, value:str) -> tuple:
		result = self.query(f'{function}("{value}").')
		return (value, result[0] if type(result) == list else result)

	def validate_queries(self, function:str, values:list) -> list:
		return [self.validate_query(function, value) for value in values]

	def add_fact(self, knowledge:str):
		self.add_facts([knowledge])
		return self

	def add_facts(self, knowledges: list):
		with open(TEMP, "a") as file:
			for knowledge in knowledges:
				file.write(knowledge + "\n")
		self.load_file(TEMP)
		return self

	def close(self):
		self.prolog_thread.stop()
		self.mqi.stop()
		if path.exists(TEMP):
			remove(TEMP)
