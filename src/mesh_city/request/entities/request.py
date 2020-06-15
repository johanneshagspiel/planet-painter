"""
See :class:`.Request`
"""

from typing import Any

from mesh_city.request.layers.layer import Layer
from mesh_city.request.scenario.scenario import Scenario


class Request:
	"""Stores all relevant data of a request"""

	def __init__(
		self,
		request_id,
		num_of_horizontal_images,
		num_of_vertical_images,
		x_grid_coord,
		y_grid_coord,
		zoom,
		layers=None,
		scenarios=None
	) -> None:
		self.request_id = request_id
		self.x_grid_coord = x_grid_coord
		self.y_grid_coord = y_grid_coord
		self.num_of_horizontal_images = num_of_horizontal_images
		self.num_of_vertical_images = num_of_vertical_images
		self.zoom = zoom
		self.layers = [] if layers is None else layers
		self.scenarios = [] if scenarios is None else scenarios

	def add_layer(self, layer: Layer) -> None:
		"""
		Adds a layer to this request.

		:param layer: the layer that is to be added
		:return: None
		"""
		self.layers.append(layer)

	def add_scenario(self, scenario: Scenario) -> None:
		"""
		Adds a scenario to this request.

		:param scenario: the scenario that is to be added
		:return: None
		"""
		self.scenarios.append(scenario)

	def has_scenario_of_type(self, scenario_type: type) -> bool:
		"""
		Returns whether this request has a scenario of the given type or not.

		:param scenario_type: The type of scenario to check for
		:return: None
		"""
		for scenario in self.scenarios:
			if isinstance(scenario, scenario_type):
				return True
		return False

	def get_scenario_of_type(self, scenario_type: type) -> Any:
		"""
		Tries to get a scenario of the specified type.

		:param scenario_type: The type of scenario to get an instance of
		:return: An instance of this scenario type if the class has one, else errors. Typed as Any
		         because of type system limitations.
		"""
		for scenario in self.scenario:
			if isinstance(scenario, scenario_type):
				return scenario
		raise ValueError("No layer of type " + str(scenario_type) + " exists")

	def has_layer_of_type(self, layer_type: type) -> bool:
		"""
		Returns whether this request has a layer of the given type or not.

		:param layer_type: The type of layer to check for
		:return: None
		"""
		for layer in self.layers:
			if isinstance(layer, layer_type):
				return True
		return False

	def get_layer_of_type(self, layer_type: type) -> Any:
		"""
		Tries to get a layer of the specified type.

		:param layer_type: The type of layer to get an instance of
		:return: An instance of this layer type if the class has one, else errors. Typed as Any
		         because of type system limitations.
		"""
		for layer in self.layers:
			if isinstance(layer, layer_type):
				return layer
		raise ValueError("No layer of type " + str(layer_type) + " exists")
