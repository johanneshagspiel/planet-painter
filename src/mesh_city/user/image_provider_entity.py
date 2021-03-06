"""
This module contains the image provider log
"""
from calendar import monthrange
from datetime import datetime

from mesh_city.imagery_provider.top_down_provider_factory import TopDownProviderFactory
from mesh_city.logs.log_entity import LogEntity
from mesh_city.util.price_table_util import PriceTableUtil


class ImageProviderEntity(LogEntity):
	"""
	The image provider log class that stores all information regarding one image provider associated
	with a user such as api key, usage, quota etc.
	"""

	def __init__(
		self,
		file_handler,
		json_data=None,
		type_map_provider=None,
		api_key=None,
		quota=None,
		date_reset=None
	):
		"""
		Sets up a image provider, either from json or when created for the first time
		:param json_data: the json from which to load the image provider
		:param type_map_provider: what kind of image provider this is
		:param api_key: the api key associated with the image provider
		:param quota: the quota to be observed
		:param usage: a dictionary representing the total usage, static map usage
		and geocoding usage.
		:param date_reset: The date the monthly usage should be reset.
		"""
		super().__init__(path_to_store=file_handler.folder_overview['users.json'])
		if (type_map_provider and api_key and quota is not None):
			self.type = type_map_provider
			self.api_key = api_key
			self.usage = {"static_map": 0, "geocoding": 0, "total": 0}
			self.quota = int(quota)

			self.date_reset = ImageProviderEntity.calculate_end_of_month(datetime.today()).date()

			if date_reset is not None:
				self.date_reset = date_reset
				self.check_date_reset(datetime.today())

			self.top_down_provider = TopDownProviderFactory.get_top_down_provider(self)

		else:
			self.type = None
			self.api_key = None
			self.usage = None
			self.quota = None
			self.date_reset = None
			self.map_entity = None
			self.load_storage(json_data)
			self.top_down_provider = TopDownProviderFactory.get_top_down_provider(self)

	def load_storage(self, storage):
		"""
		Sets the fields of the class based on a json file
		:param storage:
		:return:
		"""
		self.type = storage["type_map_provider"]
		self.api_key = storage["api_key"]
		self.usage = storage["usage"]
		self.quota = float(storage["quota"])
		self.date_reset = ImageProviderEntity.calculate_end_of_month(datetime.today()).date()

	def for_storage(self):
		"""
			Turns the class into a json compliant form
			:return: the class in a json compliant form
			"""

		return {
			"type_map_provider": self.type,
			"api_key": self.api_key,
			"usage":
			{
			"static_map": self.usage["static_map"],
			"geocoding": self.usage["geocoding"],
			"total": self.usage["total"]
			},
			"quota": self.quota,
			"date_reset": str(self.date_reset)
		}

	def increment_usage(self):
		"""
		Increments the usage
		:return:
		"""
		old_usage = self.usage["total"]
		temp_cost = PriceTableUtil.one_increase(old_usage)
		temp_new_total = old_usage + temp_cost
		self.usage["total"] = round(temp_new_total, 4)
		self.usage["static_map"] = round(temp_new_total, 4)

	def check_date_reset(self, current_date):
		"""
		Checks if the usage should be reset if a new month has started
		:return: nothing (but the usage fields are reset to 0)
		"""

		if current_date >= self.date_reset:
			self.usage["static_map"] = 0
			self.usage["geocoding"] = 0
			self.usage["total"] = 0
			self.date_reset = ImageProviderEntity.calculate_end_of_month(current_date)

	@staticmethod
	def calculate_end_of_month(date):
		"""
		Helper method to calculate the end of a month
		:return: a string containing the end of the month
		"""
		temp_end = monthrange(date.year, date.month)
		return datetime(date.year, date.month, temp_end[1])

	# pylint: disable=W0613
	def action(self, logs):
		"""
		Action performed when called by the log manager when writing to file
		:param logs: global log context
		:return: just turns the object to json
		"""
		return self.for_storage()
