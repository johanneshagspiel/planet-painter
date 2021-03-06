# pylint: disable=C0114,R0201,missing-class-docstring,missing-function-docstring

import unittest

from mesh_city.util.geo_location_util import GeoLocationUtil


class TestGeoLocationUtil(unittest.TestCase):

	def setUp(self):
		self.geo_location_util = GeoLocationUtil()
		# correct ground resolutions (meters per pixel) at the Equator for zoom levels 0 to 23
		# level 0 being 156543.03392
		self.ground_resolutions = [
			156543.03392,
			78271.5170,
			39135.7585,
			19567.8792,
			9783.9396,
			4891.9698,
			2445.9849,
			1222.9925,
			611.4962,
			305.7481,
			152.8741,
			76.4370,
			38.2185,
			19.1093,
			9.5546,
			4.7773,
			2.3887,
			1.1943,
			0.5972,
			0.2986,
			0.1493,
			0.0746,
			0.0373,
			0.0187
		]

	def test_calc_meters_per_px(self):
		for zoom in range(23):
			answer_resolution = self.ground_resolutions[zoom]
			calculated_resolution = self.geo_location_util.calc_meters_per_px(0, zoom)
			self.assertAlmostEqual(answer_resolution, calculated_resolution, 4)

	def test_calc_next_location_latitude_true(self):
		answer_latitude = 50.000452662598086
		calculated_latitude = self.geo_location_util.calc_next_location_latitude(50, 5, 20, True)
		self.assertEqual(answer_latitude, calculated_latitude)

	def test_calc_next_location_latitude_false(self):
		answer_latitude = 49.99956992835618
		calculated_latitude = self.geo_location_util.calc_next_location_latitude(50, 5, 20, False)
		self.assertEqual(answer_latitude, calculated_latitude)

	def test_calc_next_location_longitude_true(self):
		answer_longitude = 5.000502777099626
		calculated_latitude = self.geo_location_util.calc_next_location_longitude(50, 5, 20, True)
		self.assertEqual(answer_longitude, calculated_latitude)

	def test_calc_next_location_longitude_false(self):
		answer_longitude = 4.999129486084001
		calculated_latitude = self.geo_location_util.calc_next_location_longitude(50, 5, 20, False)
		self.assertEqual(answer_longitude, calculated_latitude)

	def test_degree_to_tile_value_illegal_lat_input(self):
		self.assertRaises(ValueError, self.geo_location_util.degree_to_tile_value, 86, 5, 20)

	def test_degree_to_tile_value_illegal_long_input(self):
		self.assertRaises(ValueError, self.geo_location_util.degree_to_tile_value, 50, 181, 20)

	def test_tile_value_to_degree_illegal_y_input(self):
		self.assertRaises(ValueError, self.geo_location_util.tile_value_to_degree, 1, 9, 3)

	def test_tile_value_to_degree_illegal_x_input(self):
		self.assertRaises(ValueError, self.geo_location_util.tile_value_to_degree, -1, 16, 5)

	def test_degree_to_tile_value(self):
		closest_tiles_without_normalisation = 269426, 177809
		closest_tiles_with_normalisation = 269425, 177808
		calculated_answer = self.geo_location_util.degree_to_tile_value(
			50.000236394207846, 4.9994659423828125, 20
		)
		self.assertNotEqual(calculated_answer, closest_tiles_without_normalisation)
		self.assertEqual(calculated_answer, closest_tiles_with_normalisation)

	def tile_value_to_degree(self):
		answer1 = (50.00001571117412, 4.999809265136719)
		answer2 = (49.99979502712741, 5.000152587890625)
		calculated_answer1 = self.geo_location_util.tile_value_to_degree(538851, 355619, 20)
		calculated_answer2 = self.geo_location_util.tile_value_to_degree(538852, 355620, 20)
		self.assertEqual(answer1, calculated_answer1)
		self.assertEqual(answer2, calculated_answer2)

	def test_normalise_coordinates(self):
		answer_coordinates = 50.00001571117412, 4.999809265136719
		calculated_coordinates = self.geo_location_util.normalise_coordinates(50, 5, 20)
		self.assertEqual(answer_coordinates, calculated_coordinates)

	def test_get_top_left_bottom_right_coordinates(self):
		answer_coordinates = (50, 5), (40, 6)
		calculated_coordinates = self.geo_location_util.get_top_left_bottom_right_coordinates(
			(40, 6), (50, 5)
		)
		self.assertEqual(answer_coordinates, calculated_coordinates)

	def test_get_bottom_left_top_right_coordinates(self):
		answer_coordinates = (40, 5), (50, 6)
		calculated_coordinates = self.geo_location_util.get_bottom_left_top_right_coordinates(
			(40, 6), (50, 5)
		)
		self.assertEqual(answer_coordinates, calculated_coordinates)

	def test_transform_coordinates_to_mercator(self):
		correct_answer = 498025.45779206586, 6784206.663964961
		latitude, longitude = 51.91187323961059, 4.473838806152344
		calculated_answer = self.geo_location_util.transform_coordinates_to_mercator(
			latitude, longitude
		)
		self.assertEqual(correct_answer, calculated_answer)

	def test_calc_map_units_per_px_cor(self):
		correct_answer = (0.0746455354347404, -0.07464553543923103)
		latitude, longitude = 51.91187323961059, 4.473838806152344
		calculated_answer = self.geo_location_util.calc_map_units_per_px_cor(
			latitude=latitude, longitude=longitude, image_height=1024, image_width=1024, zoom=20
		)
		self.assertEqual(correct_answer, calculated_answer)

	def test_calc_map_units_per_px_grid(self):
		correct_answer = (0.0746455354347404, -0.07464553543923103)
		x_cor_grid, y_cor_grid = self.geo_location_util.degree_to_tile_value(
			51.91187323961059,
			4.473838806152344,
			20
		)
		calculated_answer = self.geo_location_util.calc_map_units_per_px_grid(
			x_cor_grid=x_cor_grid, y_cor_grid=y_cor_grid, image_height=1024, image_width=1024, zoom=20
		)
		self.assertEqual(correct_answer, calculated_answer)

	def test_pixel_to_geo_coor(self):
		x_cor_grid, y_cor_grid = 273066, 177808
		px_x_min, px_y_min, px_x_max, px_y_max = 723.70697, 343.9098816, 906.179688, 528.7900391
		# px_x = px_x_min + ((px_x_max - px_x_min) / 2)
		# px_y = px_y_min + ((px_y_max - px_y_min) / 2)

		calculated_lat, calculated_long = self.geo_location_util.pixel_to_geo_coor(x_cor_grid, y_cor_grid, px_x_min, px_y_min, px_x_max, px_y_max)
		correct_lat, correct_long = 50.0004896827903, 7.500088698
		self.assertAlmostEqual(correct_lat, calculated_lat)
		self.assertAlmostEqual(correct_long, calculated_long)
