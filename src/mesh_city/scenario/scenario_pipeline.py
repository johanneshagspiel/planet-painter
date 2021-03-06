"""
See :class:`.ScenarioPipeline`

source for the part of creating an elipse mask for the trees:
source: Nadia Alramli
url: https://stackoverflow.com/questions/890051/how-do-i-generate-circular-thumbnails-with-pil
"""

import random
from enum import Enum
from typing import Sequence, Tuple

import geopandas as gpd
import numpy as np
import pandas as pd
from geopandas import GeoDataFrame
from pandas import DataFrame

from mesh_city.request.entities.request import Request
from mesh_city.request.layers.buildings_layer import BuildingsLayer
from mesh_city.request.layers.cars_layer import CarsLayer
from mesh_city.request.layers.image_layer import ImageLayer
from mesh_city.request.layers.trees_layer import TreesLayer
from mesh_city.scenario.scenario import Scenario


class ScenarioModificationType(Enum):
	"""
	Enum class representing types of modifications that can be part of a scenario.
	"""
	MORE_TREES = 0
	SWAP_CARS = 1
	PAINT_BUILDINGS_GREEN = 2


class ScenarioPipeline:
	"""
	A class used to create scenario's from requests whose behaviour can be customized by specifying
	what type of things it should change.
	"""

	def __init__(self, modification_list: Sequence[Tuple[ScenarioModificationType, int]]):
		self.__modification_list = modification_list

	def paint_buildings_green(
		self, building_dataframe, buildings_to_make_green: int
	) -> GeoDataFrame:
		"""
		Labels a certain number of polygons as Shrubbery, which is later used to paint parts of the buildings green.
		:param building_dataframe:
		:param buildings_to_make_green:
		:return:
		"""
		np.random.shuffle(building_dataframe.values)
		shrubbery_dataframe = building_dataframe.head(buildings_to_make_green)
		shrubbery_dataframe.loc[:, "label"] = "Shrubbery"
		new_building_dataframe = building_dataframe.iloc[buildings_to_make_green:]
		final_dataframe = shrubbery_dataframe.append(new_building_dataframe, ignore_index=True)
		return final_dataframe

	def add_more_trees(self, tree_dataframe: DataFrame, trees_to_add: int) -> DataFrame:
		"""
		Adds more trees to the image based on the detected trees
		:param request: the request for which to add more trees to
		:param trees_to_add: how many trees to add
		:return:
		"""
		filtered_trees = tree_dataframe[tree_dataframe['label'] == "Tree"]
		new_trees = []
		for _ in range(0, trees_to_add):
			source_tree_index = np.random.randint(0, len(filtered_trees))
			neighbour_tree_index = np.random.randint(0, len(filtered_trees))
			new_xmin, new_ymin, new_xmax, new_ymax = self.__compute_new_tree_bbox(
				source_tree_index, neighbour_tree_index, filtered_trees
			)
			new_trees.append(
				(
				new_xmin,
				new_ymin,
				new_xmax,
				new_ymax,
				filtered_trees.loc[source_tree_index, ["score"]],
				"AddedTree",
				source_tree_index
				)
			)

		new_trees_df = pd.DataFrame(
			new_trees, columns=["xmin", "ymin", "xmax", "ymax", "score", "label", "source_index"]
		)
		tree_dataframe = tree_dataframe.append(new_trees_df, ignore_index=True)
		return tree_dataframe

	def swap_cars_with_trees(
		self, car_dataframe: DataFrame, tree_dataframe: DataFrame, cars_to_swap: int
	) -> Tuple[DataFrame, DataFrame]:
		"""
		Swaps a given number of cars with trees.
		:param request:
		:param cars_to_swap:
		:return:
		"""
		np.random.shuffle(car_dataframe.values)
		filtered_trees = tree_dataframe[tree_dataframe['label'] == "Tree"]
		changes_list = []
		for car_index in range(0, cars_to_swap):
			tree_to_replace_with_index = np.random.randint(0, len(filtered_trees))
			new_xmin, new_ymin, new_xmax, new_ymax = self.__compute_swapped_car_bbox(
				car_index, tree_to_replace_with_index, tree_dataframe, car_dataframe
			)
			changes_list.append(
				(new_xmin, new_ymin, new_xmax, new_ymax, tree_to_replace_with_index)
			)
		replaced_cars = car_dataframe.head(cars_to_swap)
		replaced_cars.loc[:, "source_index"] = -1
		replaced_cars.loc[:, ["xmin", "ymin", "xmax", "ymax", "source_index"]] = changes_list
		replaced_cars.loc[:, "label"] = "SwappedCar"
		car_dataframe = car_dataframe[cars_to_swap:]
		tree_dataframe = tree_dataframe.append(replaced_cars, ignore_index=True)
		return tree_dataframe, car_dataframe

	def __compute_swapped_car_bbox(
		self,
		car_to_swap_index: int,
		tree_to_replace_with_index: int,
		tree_dataframe: DataFrame,
		car_dataframe: DataFrame
	) -> Tuple[float, float, float, float]:
		"""
		Computes a new bounding box for a tree pasted where there is currently a car.
		:param car_to_swap_index: The car to paste a tree on
		:param tree_to_replace_with_index: The tree to paste onto the car
		:param tree_dataframe: The dataframe of tree detections
		:param car_dataframe: The dataframe of car detections
		:return: The bounding box for the pasted tree
		"""
		tree_xmin = tree_dataframe.iloc[tree_to_replace_with_index][0]
		tree_ymin = tree_dataframe.iloc[tree_to_replace_with_index][1]
		tree_xmax = tree_dataframe.iloc[tree_to_replace_with_index][2]
		tree_ymax = tree_dataframe.iloc[tree_to_replace_with_index][3]

		tree_distance_center_max_x = (tree_xmax - tree_xmin) / 2
		tree_distance_center_max_y = (tree_ymax - tree_ymin) / 2

		car_xmin = car_dataframe.iloc[car_to_swap_index][0]
		car_ymin = car_dataframe.iloc[car_to_swap_index][1]
		car_xmax = car_dataframe.iloc[car_to_swap_index][2]
		car_ymax = car_dataframe.iloc[car_to_swap_index][3]

		car_center_x = car_xmin + ((car_xmax - car_xmin) / 2)
		car_center_y = car_ymin + ((car_ymax - car_ymin) / 2)

		new_xmin = car_center_x - tree_distance_center_max_x
		new_xmax = car_center_x + tree_distance_center_max_x
		new_ymin = car_center_y - tree_distance_center_max_y
		new_ymax = car_center_y + tree_distance_center_max_y

		if new_xmin < 0:
			to_add = (-1) * new_xmin
			new_xmin = new_xmin + to_add
			new_xmax = new_xmax + to_add

		if new_ymin < 0:
			to_add = (-1) * new_ymin
			new_ymin = new_ymin + to_add
			new_ymax = new_ymax + to_add

		return new_xmin, new_ymin, new_xmax, new_ymax

	# pylint: disable=W0613
	def __compute_new_tree_bbox(self, source_tree, neighbour_tree, tree_dataframe) -> Tuple[
		float, float, float, float]:
		"""
		Computes a bounding box for a tree pasted near another tree.
		:param source_tree: the tree to place
		:param neighbour_tree: the location adjacent to which to place it at
		:return: The bounding box
		"""
		src_xmin = tree_dataframe.loc[source_tree]["xmin"]
		src_ymin = tree_dataframe.loc[source_tree]["ymin"]
		src_xmax = tree_dataframe.loc[source_tree]["xmax"]
		src_ymax = tree_dataframe.loc[source_tree]["ymax"]

		dest_xmin = tree_dataframe.loc[neighbour_tree]["xmin"]
		dest_ymin = tree_dataframe.loc[neighbour_tree]["ymin"]
		dest_xmax = tree_dataframe.loc[neighbour_tree]["xmax"]
		dest_ymax = tree_dataframe.loc[neighbour_tree]["ymax"]

		where_center_x = dest_xmin + ((dest_xmax - dest_xmin) / 2)
		where_center_y = dest_ymin + ((dest_ymax - dest_ymin) / 2)

		y_offset = random.uniform(-50, 50)
		x_offset = random.uniform(-50, 50)

		new_center_y = where_center_y + y_offset
		new_center_x = where_center_x + x_offset

		new_xmin = new_center_x - ((src_xmax - src_xmin) / 2)
		new_xmax = new_center_x + ((src_xmax - src_xmin) / 2)
		new_ymin = new_center_y - ((src_ymax - src_ymin) / 2)
		new_ymax = new_center_y + ((src_ymax - src_ymin) / 2)

		if new_xmin < 0:
			to_add = (-1) * new_xmin
			new_xmin = new_xmin + to_add
			new_xmax = new_xmax + to_add

		if new_ymin < 0:
			to_add = (-1) * new_ymin
			new_ymin = new_ymin + to_add
			new_ymax = new_ymax + to_add

		return new_xmin, new_ymin, new_xmax, new_ymax

	def process(self, request: Request) -> Scenario:
		"""
		Processes a request that is assumed to have a GoogleLayer with imagery (errors otherwise) and
		returns a list of detection layers corresponding to the detections_to_run variable.

		:param request: The request to process. Must have a GoogleLayer
		:return:
		"""

		if not request.has_layer_of_type(ImageLayer):
			raise ValueError(
				"The request to process should have imagery to create scenarios based of"
			)
		car_dataframe = None
		tree_dataframe = None
		buildings_dataframe = None
		if request.has_layer_of_type(CarsLayer):
			car_dataframe = pd.read_csv(
				request.get_layer_of_type(CarsLayer).detections_path, index_col=0
			)
		if request.has_layer_of_type(TreesLayer):
			tree_dataframe = pd.read_csv(
				request.get_layer_of_type(TreesLayer).detections_path, index_col=0
			)
			tree_dataframe.loc[:, "source_index"] = -1
		if request.has_layer_of_type(BuildingsLayer):
			buildings_dataframe = gpd.read_file(
				request.get_layer_of_type(BuildingsLayer).detections_path
			)
			if "label" not in buildings_dataframe.columns:
				buildings_dataframe["label"] = ""

		for (feature, information) in self.__modification_list:
			if feature == ScenarioModificationType.MORE_TREES:
				tree_dataframe = self.add_more_trees(
					tree_dataframe=tree_dataframe, trees_to_add=information
				)
			if feature == ScenarioModificationType.SWAP_CARS:
				tree_dataframe, car_dataframe = self.swap_cars_with_trees(
					car_dataframe=car_dataframe, tree_dataframe=tree_dataframe,
					cars_to_swap=information)
			if feature == ScenarioModificationType.PAINT_BUILDINGS_GREEN:
				buildings_dataframe = self.paint_buildings_green(
					building_dataframe=buildings_dataframe, buildings_to_make_green=information
				)
		return Scenario(
			cars=car_dataframe, trees=tree_dataframe, buildings=buildings_dataframe, request=request
		)
