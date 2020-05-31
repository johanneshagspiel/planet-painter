# pylint: disable=C0114,R0201,missing-class-docstring,missing-function-docstring

import unittest
from datetime import datetime
from pathlib import Path
from shutil import rmtree
from unittest.mock import ANY, call, Mock

from mesh_city.application import Application
from mesh_city.imagery_provider.request_manager import RequestManager
from mesh_city.imagery_provider.top_down_provider.google_maps_provider import GoogleMapsProvider
from mesh_city.user.entities.image_provider_entity import ImageProviderEntity
from mesh_city.user.entities.user_entity import UserEntity
from mesh_city.util.file_handler import FileHandler
from mesh_city.util.geo_location_util import GeoLocationUtil


class TestRequestManager(unittest.TestCase):

	resource_path = Path(__file__).parents[1].joinpath("resources")

	def setUp(self):

		self.provider1 = ImageProviderEntity(
			FileHandler(),
			type_map_provider="google_maps",
			api_key="AIzaSyD9cfAeQKFniipqRUgkcYy1sAtGXJYxNF4",
			quota=100,
			date_reset=datetime(2019, 2, 28)
		)
		provider_dict = {"google_maps": self.provider1}
		self.user_entity = UserEntity(FileHandler(), name="test user", image_providers=provider_dict)

		self.application = Application()
		self.application.late_init(self.user_entity)

		self.request_manager = self.application.request_manager
		self.request_manager.top_down_provider = GoogleMapsProvider(image_provider_entity=self.provider1)

		self.location_input = (-22.824637, -43.242729)

		self.two_coordinate_input = (-22.824637, -43.242729, -22.821384, -43.238813)
		self.correct_answer = (
			[(2.0, 2.0),
			 (-22.824266172626547, -43.24232666864772),
			 (-22.824266172626547, -43.24152200594317),
			 (-22.824266172626547, -43.240717343238614),
			 (-22.823524515859447, -43.24232666864772),
			 (-22.823524515859447, -43.24152200594317),
			 (-22.823524515859447, -43.240717343238614),
			 (-22.822782855052044, -43.24232666864772),
			 (-22.822782855052044, -43.24152200594317),
			 (-22.822782855052044, -43.240717343238614),
			 (-22.824266172626547, -43.23991268053406),
			 (-22.824266172626547, -43.23910801782951),
			 (-22.824266172626547, -43.238303355124955),
			 (-22.823524515859447, -43.23991268053406),
			 (-22.823524515859447, -43.23910801782951),
			 (-22.823524515859447, -43.238303355124955),
			 (-22.822782855052044, -43.23991268053406),
			 (-22.822782855052044, -43.23910801782951),
			 (-22.822782855052044, -43.238303355124955),
			 (-22.822041190204438, -43.24232666864772),
			 (-22.822041190204438, -43.24152200594317),
			 (-22.822041190204438, -43.240717343238614),
			 (-22.821299521316735, -43.24232666864772),
			 (-22.821299521316735, -43.24152200594317),
			 (-22.821299521316735, -43.240717343238614),
			 (-22.820557848389036, -43.24232666864772),
			 (-22.820557848389036, -43.24152200594317),
			 (-22.820557848389036, -43.240717343238614),
			 (-22.822041190204438, -43.23991268053406),
			 (-22.822041190204438, -43.23910801782951),
			 (-22.822041190204438, -43.238303355124955),
			 (-22.821299521316735, -43.23991268053406),
			 (-22.821299521316735, -43.23910801782951),
			 (-22.821299521316735, -43.238303355124955),
			 (-22.820557848389036, -43.23991268053406),
			 (-22.820557848389036, -43.23910801782951),
			 (-22.820557848389036, -43.238303355124955)]
		)  # yapf: disable

	def tearDown(self):
		for item in Path(__file__).parents[1].joinpath("resources").glob("*"):
			if item.is_dir():
				rmtree(item)
			else:
				item.unlink()

	def test_calculate_centre_coordinates_two_coordinate_input_correct(self):
		map_entity = Mock(spec=GoogleMapsProvider, wraps=Mock())
		map_entity.max_side_resolution_image = 640
		request_manager = self.application.request_manager

		list_of_coordinates = request_manager.calculate_locations(
			[self.two_coordinate_input[0], self.two_coordinate_input[1], self.two_coordinate_input[2],
			 self.two_coordinate_input[3]])

		self.assertEqual(self.correct_answer, list_of_coordinates)

	def test_calculate_number_of_requested_images_two_coordinate_input(self):
		number_of_images = self.application.request_manager.\
			calculate_locations(self.two_coordinate_input)
		self.assertEqual(37, len(number_of_images))

	def test_calculate_centre_coordinates_two_coordinate_input_latitude_turned_around(self):
		with self.assertRaises(Exception):
			self.application.request_manager.calculate_locations([self.two_coordinate_input[2],
			                                                      self.two_coordinate_input[1],
			                                                      self.two_coordinate_input[0],
			                                                      self.two_coordinate_input[3]])

	def test_calculate_number_of_requested_images_two_coordinate_longitude_turned_around(self):
		with self.assertRaises(Exception):
			self.application.request_manager.calculate_locations([self.two_coordinate_input[0],
			                                                      self.two_coordinate_input[3],
			                                                      self.two_coordinate_input[2],
			                                                      self.two_coordinate_input[1]])

	def test_calculate_number_of_requested_images_two_coordinate_input_same_latitude(self):
		with self.assertRaises(Exception):
			self.application.request_manager.calculate_locations([self.two_coordinate_input[0],
			                                                      self.two_coordinate_input[1],
			                                                      self.two_coordinate_input[0],
			                                                      self.two_coordinate_input[3]])

	def test_calculate_number_of_requested_images_two_coordinate_input_same_longitude(self):
		with self.assertRaises(Exception):
			self.application.request_manager.calculate_locations([self.two_coordinate_input[0],
			                                                      self.two_coordinate_input[1],
			                                                      self.two_coordinate_input[2],
			                                                      self.two_coordinate_input[1]])

	def test_calculate_number_of_requested_images_two_coordinate_input_same_longitude(self):
		number_of_images = self.application.request_manager\
			.calculate_locations(self.location_input
		)
		self.assertEqual(9, len(number_of_images))

	def test_single_request(self):
		request_manager = self.request_manager
		request_manager.top_down_provider = Mock()

		request_manager.top_down_provider.get_and_store_location((52.010442, 4.357480), 1.0, 400, 600)

		self.request_manager.top_down_provider.get_and_store_location.assert_called_once_with(
			(52.010442, 4.357480), 1.0, 400, 600
		)
