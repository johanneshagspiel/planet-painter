# pylint: disable=C0114,R0201,missing-class-docstring,missing-function-docstring

import unittest
from pathlib import Path

from mesh_city.request.entities.request import Request
from mesh_city.request.entities.tile import Tile
from mesh_city.request.layers.image_layer import ImageLayer
from mesh_city.request.request_manager import RequestManager


class TestRequestManager(unittest.TestCase):

	def test_add_to_grid(self):
		request_manager = RequestManager(image_root=Path(""))
		google_layer = ImageLayer(
			width=1, height=1, tiles=[Tile(path=Path("dummy_path"), x_grid_coord=0, y_grid_coord=0)]
		)
		request = Request(
			request_id=42,
			x_grid_coord=0,
			y_grid_coord=0,
			num_of_horizontal_images=1,
			num_of_vertical_images=1,
			zoom=20,
			layers=[google_layer],
			name="test"
		)
		request_manager.add_request(request=request)
		self.assertTrue(request_manager.is_in_grid(x_coord=0, y_coord=0))

	def test_add_to_grid_no_layer(self):
		request_manager = RequestManager(image_root=Path(""))
		request = Request(
			request_id=42,
			x_grid_coord=0,
			y_grid_coord=0,
			num_of_horizontal_images=1,
			num_of_vertical_images=1,
			zoom=20,
			name="test"
		)
		request_manager.add_request(request=request)
		self.assertFalse(request_manager.is_in_grid(x_coord=0, y_coord=0))

	def test_not_in_grid(self):
		request_manager = RequestManager(image_root=Path(""))
		with self.assertRaises(ValueError):
			request_manager.get_tile_from_grid(x_coord=1, y_coord=1)

	def test_get_image_root(self):
		self.assertEqual(RequestManager(image_root=Path("")).get_image_root(), Path(""))
