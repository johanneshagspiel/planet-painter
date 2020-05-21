"""
A module that contains the log manager who is responsible for performing all the actions associated with logs
"""

import json
import os
from pathlib import Path


class LogManager:
	"""
	A class that is responsible for logging every request made.
	"""

	def __init__(self, resource_path=Path(__file__).parents[1].joinpath("resources")):
		self.resource_path = resource_path
		self.image_path = resource_path.joinpath("images")
		self.log_path = resource_path.joinpath("logs", "log_request_.json")

	def get_request_number(self):
		"""
		This method is needed because request manager needs to know the number of the next request
		to name the folder appropriately
		:return: the number of the next request
		"""

		max_log = 0

		if self.log_path.is_file():  # pylint: disable=no-member
			with open(self.log_path, "r") as json_log:
				data = json_log.read()
				json_log.close()
			logs = json.loads(data)

			for item in logs.values():
				for element in item:
					element = [int(k) for k, v in element.items()][0]
					if element > max_log:
						max_log = element
		else:
			max_log = 0

		max_directory = 0

		self.image_path.mkdir(exist_ok=True)
		if len(os.listdir(self.image_path)) == 0:
			max_directory = 0
		else:
			for directory in os.listdir(self.image_path):
				if directory.split("_")[1] != "":
					temp_result = int(directory.split("_")[1])
					if temp_result > max_directory:
						max_directory = temp_result

		return max_log + 1 if max_log > max_directory else max_directory + 1

	def write_entry_log(self, log_entry):
		"""
		A method to write one log entry entity to the associated correct location
		:param log_entry: the log entry with its appropriate location to store it to
		:return: nothing
		"""

		with open(log_entry.path_to_store, "r") as json_log:
			data = json_log.read()
		logs = json.loads(data)
		result = log_entry.action(self, logs)

		with open(log_entry.log_path, "w") as json_log:
			json.dump(result, fp=json_log)
			json_log.close()
