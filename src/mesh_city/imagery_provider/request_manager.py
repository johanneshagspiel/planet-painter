"""
Module which contains code to interact with the top_down providers, organising the requests to
their APIs such that data for larger geographical areas can be made and the results of these
requests are stored on disk.
"""

import os
from pathlib import Path

from mesh_city.imagery_provider.request_creator import RequestCreator
from mesh_city.logs.log_entities.building_instructions_request import BuildingInstructionsRequest
from mesh_city.util.geo_location_util import GeoLocationUtil
from mesh_city.util.image_util import ImageUtil


class RequestManager:
	"""
	A class that is responsible for handling requests to different map providers. Based on
	tile_information of the user it calculates all the locations that need to be downloaded, downloads them
	stores them in tile system: 9 images together make up one tile. These 9 images are, after being downloaded,
	combined into one large image that is displayed on the map.
	:param user_info: information about the user
	:param quota_manager: quota manager associated with the user
	"""

	def __init__(self, user_entity, application, top_down_provider=None):
		self.user_entity = user_entity
		self.top_down_provider = top_down_provider
		self.application = application

		self.file_handler = application.file_handler
		self.log_manager = application.log_manager

		self.image_util = ImageUtil()
		self.geo_location_util = GeoLocationUtil()

		self.request_number = self.log_manager.get_request_number()

		self.normal_building_instructions = None
		self.temp_list = None

	def make_request_for_block(self, coordinates, zoom=None):
		"""
		Make a request in such a way, that the images are stored in the tile system, are logged in
		the log manager and they can be displayed on the map
		:param centre_coordinates: the location where the image should be downloaded
		:param zoom: the zoom level at which the image should be downloaded
		:return: nothing
		"""
		max_latitude = 0

		self.normal_building_instructions = []

		if len(coordinates) == 9:
			self.normal_building_instructions.append(0)

		if len(coordinates) > 9:
			temp = coordinates.pop(0)
			max_latitude = temp[0]
			self.normal_building_instructions.append(int(temp[1]))

		if zoom is None:
			zoom = self.top_down_provider.max_zoom

		request_number = self.log_manager.get_request_number()
		request_number_string = str(request_number)

		# a new folder is created for the request if it goes ahead
		new_folder_path = Path.joinpath(
			self.file_handler.folder_overview["image_path"], "request_" + request_number_string
		)
		os.makedirs(new_folder_path)

		# then a folder for the first tile is created
		# the tiles are named in such a way that their name form a coordinate system that can be used
		# in the gui to load adjacent tiles
		number_tile_downloaded = 0
		tile_number_latitude = 0
		tile_number_longitude = 0
		temp_tile_number_latitude = str(tile_number_latitude)
		temp_tile_number_longitude = str(tile_number_longitude)
		temp_tile_name = str(
			number_tile_downloaded
		) + "_tile_" + temp_tile_number_latitude + "_" + temp_tile_number_longitude
		new_folder_path = Path.joinpath(new_folder_path, temp_tile_name)
		os.makedirs(new_folder_path)

		number_requests = len(coordinates)
		print("Requestnumber: " + str(self.request_number))
		print("Total Images to download: " + str(number_requests))

		number_requests_temp = number_requests
		total_tile_numbers = number_requests / 9
		# stores the information whether or not this is the last tile of the request
		# if yes, information should be logged and no new folder should be created
		last_round = False
		if number_requests == 9:
			last_round = True

		self.temp_list = []

		counter = 1
		# download and store the information in the case of only one pair of tile_information

		if len(coordinates) == 9:
			for location in coordinates:
				if location[1] is None:
					number = str(counter)
					latitude = str(location[0][0])
					longitude = str(location[0][1])
					temp_name = str(number + "_" + longitude + "_" + latitude + ".png")
					temp_location_stored = str(
						self.top_down_provider.get_and_store_location(
						location[0][0], location[0][1], zoom, temp_name, new_folder_path
						)
					)
					self.temp_list.append(temp_location_stored)

					if latitude in self.file_handler.coordinate_overview.grid:
						new_to_store = self.file_handler.coordinate_overview.grid[latitude]
						new_to_store[longitude] = {"normal": temp_location_stored}
						self.file_handler.coordinate_overview.grid[latitude] = new_to_store
					else:
						self.file_handler.coordinate_overview.grid[latitude] = {
							longitude: {
							"normal": temp_location_stored
							}
						}
				else:
					self.temp_list.append(location[1])
				counter += 1

				if counter == 10 and last_round:

					self.normal_building_instructions.append(self.temp_list)

					self.file_handler.folder_overview["active_tile_path"] = new_folder_path
					self.file_handler.folder_overview["active_image_path"] = new_folder_path
					self.file_handler.folder_overview["active_request_path"
														] = new_folder_path.parents[0]

					self.log_manager.write_log(self.file_handler.coordinate_overview)

					temp_path_request = Path.joinpath(
						new_folder_path.parents[0],
						"building_instructions_request_" + str(request_number) + ".json"
					)
					temp_building_instructions_request = BuildingInstructionsRequest(
						temp_path_request
					)
					temp_building_instructions_request.instructions[
						"normal"] = self.normal_building_instructions
					self.log_manager.create_log(temp_building_instructions_request)

					temp_request_creator = RequestCreator(application=self.application)
					temp_request_creator.follow_instructions(
						"normal", temp_building_instructions_request
					)

		# download and store the information in case a whole area was asked for
		if len(coordinates) > 9:
			for location in coordinates:

				if location[1] is None:
					number = str(counter)
					latitude = str(location[0][0])
					longitude = str(location[0][1])
					temp_name = str(number + "_" + longitude + "_" + latitude + ".png")
					temp_location_stored = str(
						self.top_down_provider.get_and_store_location(
						location[0][0],
						location[0][1],
						self.top_down_provider.max_zoom,
						temp_name,
						new_folder_path
						)
					)
					self.temp_list.append(temp_location_stored)

					if latitude in self.file_handler.coordinate_overview.grid:
						new_to_store = self.file_handler.coordinate_overview.grid[latitude]
						new_to_store[longitude] = {"normal": temp_location_stored}
						self.file_handler.coordinate_overview.grid[latitude] = new_to_store
					else:
						self.file_handler.coordinate_overview.grid[latitude] = {
							longitude: {
							"normal": temp_location_stored
							}
						}
				else:
					self.temp_list.append(location[1])
				counter += 1

				if counter == 10 and not last_round:
					number_tile_downloaded += 1

					tile_number_latitude += 1
					if tile_number_latitude == max_latitude:
						tile_number_latitude = 0
						tile_number_longitude += 1

					tile_number_new = str(tile_number_latitude) + "_" + str(tile_number_longitude)
					tile_name_new = str(number_tile_downloaded) + "_tile_" + tile_number_new
					new_folder_path = Path.joinpath(new_folder_path.parents[0], tile_name_new)
					os.makedirs(new_folder_path)

					self.normal_building_instructions.append(self.temp_list)
					self.temp_list = []

					print(str(number_tile_downloaded) + "/" + str(total_tile_numbers))

					counter = 1
					number_requests_temp = number_requests_temp - 9
					if number_requests_temp == 9:
						last_round = True

				if counter == 10 and last_round:
					number_tile_downloaded += 1
					tile_number = str(tile_number_latitude) + "_" + str(tile_number_longitude)
					self.image_util.concat_images(new_folder_path, counter, tile_number)

					self.file_handler.folder_overview["active_tile_path"] = new_folder_path
					self.file_handler.folder_overview["active_image_path"] = new_folder_path
					self.file_handler.folder_overview["active_request_path"
														] = new_folder_path.parents[0]

					self.normal_building_instructions.append(self.temp_list)
					temp_path_request = Path.joinpath(
						new_folder_path.parents[0],
						"building_instructions_request_" + str(request_number) + ".json"
					)
					temp_building_instructions_request = BuildingInstructionsRequest(
						temp_path_request
					)
					temp_building_instructions_request.instructions[
						"normal"] = self.normal_building_instructions
					self.log_manager.create_log(temp_building_instructions_request)

					self.log_manager.write_log(self.file_handler.coordinate_overview)

					temp_request_creator = RequestCreator(application=self.application)
					temp_request_creator.follow_instructions(
						"normal", temp_building_instructions_request
					)

					print(str(number_tile_downloaded) + "/" + str(total_tile_numbers))

		return new_folder_path

	def calculate_centre_coordinates_two_coordinate_input_block(
		self, first_coordinate, second_coordinate, zoom
	):
		"""
		CREATES BLOCKS

		Method which calculates and retrieves the number of images that are necessary have a
		complete imagery set of a certain geographical area. This area is defined by a bounding box.
		The function checks whether the first coordinate inputted is "smaller" than the second
		inputted coordinate.
		:param bottom_left: the bottom left coordinate of the bounding box.
		:param top_right: the bottom left coordinate of the bounding box.
		:param zoom: the level of zoom (meters per pixel) the returned images will be.
		:return: a list of coordinates, first entry indicates the number of steps between blocks.
		"""

		(bottom_lat, left_long), (top_lat,
			right_long) = self.geo_location_util.get_bottom_left_top_right_coordinates(
			first_coordinate, second_coordinate
			)

		# normalise coordinate input before adding it to coordinate list
		latitude_first_image, longitude_first_image = self.geo_location_util.normalise_coordinates(
			bottom_lat, left_long, zoom)
		current_latitude, current_longitude = latitude_first_image, longitude_first_image

		coordinates_list = []
		num_of_images_horizontal = 0
		num_of_images_vertical = 0

		# iterate from left to right, bottom to top
		# to support the tile system, the total number of images to download needs to be divisible by
		# 9 as one tile is 9 images
		while current_latitude <= top_lat or (num_of_images_vertical % 3) != 0:
			num_of_images_horizontal = 0
			while current_longitude <= right_long or (num_of_images_horizontal % 3) != 0:
				x_cor_current_tile, y_cor_current_tile = self.geo_location_util.degree_to_tile_value(
					current_latitude, current_longitude, zoom
				)
				coordinates_list.append(
					((current_latitude, current_longitude), (x_cor_current_tile, y_cor_current_tile))
				)
				current_longitude = self.geo_location_util.calc_next_location_longitude(
					current_latitude, current_longitude, zoom, True
				)
				num_of_images_horizontal += 1

			current_longitude = longitude_first_image
			current_latitude = self.geo_location_util.calc_next_location_latitude(
				current_latitude, current_longitude, zoom, True
			)
			num_of_images_vertical += 1

		num_of_images_total = num_of_images_horizontal * num_of_images_vertical

		temp_result = (num_of_images_total, num_of_images_horizontal,
			num_of_images_vertical), coordinates_list

		# here, the results need to be rearranged so that the order of coordinates returned corresponds
		# to one tile after the other. Currently the output is : 0,0 - 1,0 - 2,0 - 3,0 -4,0
		# for the tile system, the output needs to be : 0,0 - 1,0 - 2,0 - 0,1 -1,1 - 1,2 etc.
		result = temp_result[1]
		max_entry = temp_result[0][0]
		max_latitude = temp_result[0][1]
		max_longitude = temp_result[0][1]

		counter = 0
		pointer = 0
		level = 0
		ordered_result = [(max_latitude / 3, max_longitude / 3)]
		run = True

		while run:
			ordered_result.append(result[pointer][0])
			pointer += 1

			# if we moved 3 points to the right, we are at the end of one tile
			if (pointer % 3) == 0:
				# if we are two levels up, we are at the top right end of a tile
				if level == 2:
					# in case this is also at the right hand end of the area we are interested in,
					# so now we want to go further up
					if (pointer % max_latitude) == 0:
						level = 0
					# here we are not at the very right hand of the area we are interested in, so we
					# again have to move down and then to the right
					else:
						pointer -= (2 * max_latitude)
						level -= 2
				# else this means we are on either level zero or one and thus we can go up one more level
				else:
					pointer = pointer - 3 + max_latitude
					level += 1

			counter += 1
			if counter == max_entry:
				run = False

		return ordered_result

	def calculate_locations(self, coordinates, zoom=None):
		"""
		This method calculates all the locations to be downloaded for one request
		:param coordinates: the central tile_information around which the other image
		:param zoom:
		:return: a list of coordinates.
		"""
		if zoom is None:
			zoom = self.top_down_provider.max_zoom
		if zoom < 1:
			zoom = 1
		if zoom > self.top_down_provider.max_zoom:
			zoom = self.top_down_provider.max_zoom

		# if the request made is for one location
		if len(coordinates) == 2:
			latitude = coordinates[0]
			longitude = coordinates[1]
			# normalise coordinate input before adding it to coordinate list
			latitude, longitude = self.geo_location_util.normalise_coordinates(
				latitude=latitude, longitude=longitude, zoom=zoom
			)

			bottom = self.geo_location_util.calc_next_location_latitude(
				latitude=latitude, longitude=longitude, zoom=zoom, direction=False
			)
			top = self.geo_location_util.calc_next_location_latitude(
				latitude=latitude, longitude=longitude, zoom=zoom, direction=True
			)
			right = self.geo_location_util.calc_next_location_longitude(
				latitude=latitude, longitude=longitude, zoom=zoom, direction=True
			)
			left = self.geo_location_util.calc_next_location_longitude(
				latitude=latitude, longitude=longitude, zoom=zoom, direction=False
			)

			coordinates_list = [
				(bottom, left), (bottom, longitude), (bottom, right), (latitude, left),
				(latitude, longitude), (latitude, right), (top, left), (top, longitude), (top, right),
			]  # pylint: disable=invalid-name

			return coordinates_list

		# if the request concerns a two coordinate input for an area
		if len(coordinates) == 4:
			return self.calculate_centre_coordinates_two_coordinate_input_block(
				(coordinates[0], coordinates[1]), (coordinates[2], coordinates[3]), zoom
			)

		raise Exception(
			"Something went wrong with the input, as it doesn't return something "
			"when it should have "
		)

	def check_coordinates(self, coordinates):
		"""
		Method to check whether or not the coordinates are already downloaded
		:param coordinates: the coordinates to check
		:return: a list indicating whether the coordinates are already downloaded or not
		"""
		temp_list = []
		counter = 0
		first_round = len(coordinates) > 9

		for location in coordinates:
			if first_round:
				temp_list.append(location)
				first_round = False
			else:
				latitude = str(location[0])
				longitude = str(location[1])

				if latitude in self.file_handler.coordinate_overview.grid:
					if longitude in self.file_handler.coordinate_overview.grid[latitude]:
						temp_list.append(
							(
							(latitude, longitude),
							self.file_handler.coordinate_overview.grid[latitude][longitude]["normal"]
							)
						)
					else:
						temp_list.append(((latitude, longitude), None))
						counter += 1
				else:
					temp_list.append(((latitude, longitude), None))
					counter += 1

		temp_list.insert(0, counter)
		return temp_list
