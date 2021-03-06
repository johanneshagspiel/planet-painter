"""
Module containing the user_entity class
"""

from mesh_city.logs.log_entity import LogEntity
from mesh_city.user.image_provider_entity import ImageProviderEntity


class UserEntity(LogEntity):
	"""
	The user entity class which store all the information associated with the user such as
	name and map providers associated with the user
	"""

	def __init__(self, file_handler, json=None, name=None, image_providers=None):
		"""
		Sets up a user, either from json or when created for the first time.

		:param file_handler: the file handler needed to store the user
		:param json: the json from which to create the user
		:param name: the name of the user
		:param image_providers: the image providers associated with the user
		"""

		super().__init__(path_to_store=file_handler.folder_overview['users.json'])
		self.file_handler = file_handler

		if (name and image_providers is not None):
			self.name = name
			self.image_providers = image_providers
			self.check_name()
		else:
			self.name = None
			self.image_providers = None
			self.load_storage(json)

	def load_storage(self, storage):
		"""
		Sets up the user from a json file.
		:param json: the json file from which to set up the user
		:return: nothing (the fields of the user are initialized correctly)
		"""

		key, value = list(storage.items())[0]
		self.name = key
		self.image_providers = {}
		self.load_image_providers(value)

	def load_image_providers(self, json):
		"""
		Helper method to set up the image providers from json.

		:param json: the json file from which to set up the image providers
		:return: nothing (the image providers field is set up correctly)
		"""

		for item in json.items():
			self.image_providers[item[0]] = (ImageProviderEntity(self.file_handler, item[1]))

	def for_storage(self):
		"""
		Turns the class into a json compliant form.

		:return: the class in json compliant form
		"""

		self.check_name()
		temp_image_providers = {}
		for key, value in self.image_providers.items():
			temp_image_providers[key] = value.for_storage()

		return temp_image_providers

	def action(self, logs):
		"""
		The action performed by the log reader when writing this class to a larger log.

		:param logs: the log to which to write this class to
		:return: the updated logs
		"""

		to_store = self.for_storage()
		logs[self.name] = to_store
		return logs

	def check_name(self):
		"""
		Helper method to check that each name of the image providers is unique.

		:return: nothing (all the image providers have unique names)
		"""

		names = {}
		for key in self.image_providers.keys():
			if key in names:
				old_name = key
				new_value = names[old_name] + 1
				new_name = str(old_name) + "_" + str(new_value)

				names[new_name] = 0
				names[old_name] = new_value

				# new_key = new_name
				# self.image_providers[new_key] = self.image_providers.pop(old_name)
				# names[old_name] = new_value
			else:
				names[key] = 0
