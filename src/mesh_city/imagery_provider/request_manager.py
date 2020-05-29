"""
Module which contains code to interact with the top_down providers, organising the requests to
their APIs such that data for larger geographical areas can be made and the results of these
requests are stored on disk.
"""

import csv
import os
from pathlib import Path


class RequestManager:
	"""
	A class that is responsible for handling requests to different map providers. Based on
	coordinates of the user it calculates all the locations that need to be downloaded, downloads them
	stores them in tile system: 9 images together make up one tile. These 9 images are, after being downloaded,
	combined into one large image that is displayed on the map.
	:param user_info: information about the user
	:param quota_manager: quota manager associated with the user
	"""

	def __init__(
		self, log_manager, image_util, geo_location_util, file_handler, top_down_provider=None,
	):
		self.top_down_provider = top_down_provider
		self.log_manager = log_manager
		self.image_util = image_util
		self.geo_location_util = geo_location_util
		self.file_handler = file_handler

		self.images_folder_path = file_handler.folder_overview["image_path"]
		self.request_number = 1

	def make_single_request(self, centre_coordinates, zoom, height=None, width=None):
		"""
		Test method to make and store one image. Does not support the tile system and the image can
		not be displayed on the map.
		:param centre_coordinates: the location where the satellite image should be downloaded
		:param zoom: the zoom level at which the image should be downloaded
		:param height: height of the resulting image
		:param width: width of the resulting image
		:return:
		"""
		self.top_down_provider.get_and_store_location(
			latitude=centre_coordinates[0],
			longitude=centre_coordinates[1],
			zoom=zoom,
			height=height,
			width=width,
			filename=str(centre_coordinates[0]) + ", " + str(centre_coordinates[1]) + ".png",
			new_folder_path=self.images_folder_path,
		)

	def make_request_two_coordinates(self, first_coordinate, second_coordinate, zoom=None):
		"""
		Takes as input two coordinates for a bounding box, a zoom level to specify how zoomed in the
		the images need to be and saves the retrieved images in a semi-structured way on disk.
		:param first_coordinate:
		:param second_coordinate:
		:param zoom:
		:return:
		"""
		if zoom is None:
			zoom = self.top_down_provider.max_zoom
		if zoom < 1:
			zoom = 1
		if zoom > self.top_down_provider.max_zoom:
			zoom = self.top_down_provider.max_zoom

		coordinates_info = self.calculate_centre_coordinates_two_coordinate_input(
			first_coordinate, second_coordinate, zoom
		)

		print("Requestnumber: " + str(self.request_number))
		print("Total Images to download: " + str(coordinates_info[0][0]))
		print("Total number of horizontal images: " + str(coordinates_info[0][1]))
		print("Total number of vertical images: " + str(coordinates_info[0][2]))

		coordinates_list = coordinates_info[1]
		self.make_request_list_of_coordinates(coordinates_list, zoom)

	def make_request_list_of_coordinates(self, coordinates_list, zoom):
		"""
		Makes a number of API requests based on the input of a coordinate list.
		:param coordinates_list: list of coordinates, and image positions in the global grid.
		format: (latitude, longitude), (horizontal, vertical)
		horizontal and vertical signal the images position in the world grid
		coordinates_list = coordinates_info[1]
		:param zoom: which level of zoom the imagery should have
		:return: saves all images on disk, and creates an CSV document with metadata.
		"""

		new_folder_path = Path.joinpath(
			self.file_handler.folder_overview["image_path"][0], "request_" + str(self.request_number)
		)
		os.makedirs(new_folder_path)

		# saves metadata to an CSV file
		csv_filename = Path.joinpath(new_folder_path, "imagery_metadata.csv")
		with open(csv_filename, "w") as csvfile:
			fieldnames = [
				"image_number", "horizontal_position", "vertical_position", "latitude", "longitude"
			]
			csv_writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
			csv_writer.writeheader()

			image_number = 0
			for info in coordinates_list:
				latitude = info[0][0]
				longitude = info[0][1]
				horizontal_position = info[1][0]
				vertical_position = info[1][1]
				image_number = image_number + 1

				file_name = str(
					str(image_number) + "_" + str(horizontal_position) + "," + str(vertical_position) +
					"_" + str(latitude) + "," + str(longitude) + ".png"
				)
				self.top_down_provider.get_and_store_location(
					latitude=latitude,
					longitude=longitude,
					zoom=zoom,
					filename=file_name,
					new_folder_path=new_folder_path
				)
				csv_writer.writerow(
					{
					"image_number": str(image_number),
					"horizontal_position": str(horizontal_position),
					"vertical_position": str(vertical_position),
					"latitude": str(latitude),
					"longitude": str(longitude),
					}
				)

	def calculate_number_of_requested_images_two_coordinate_input(
		self, first_coordinate, second_coordinate, zoom
	):
		"""
		Calculates the number of images that will be requested through the API when requesting a
		bounding box with these two coordinates
		:param first_coordinate: of the bounding box.
		:param second_coordinate: of the bounding box.
		:param zoom: the level of zoom (meters per pixel) the returned images will be.
		:return: number of images that will be requested
		"""
		return self.calculate_centre_coordinates_two_coordinate_input(
			first_coordinate, second_coordinate, zoom
		)[0][0]

	def calculate_centre_coordinates_two_coordinate_input(
		self, first_coordinate, second_coordinate, zoom
	):
		"""
		Method which calculates and retrieves the number of images that are necessary to have a
		complete imagery set of a certain geographical area. This area is defined by a bounding box.
		:param first_coordinate: of the bounding box.
		:param second_coordinate:  of the bounding box.
		:param zoom: the level of zoom (meters per pixel) the returned images will be.
		:return: a pair which contains as its first value a tuple with the total number of images,
		and the number of images along the axis, and as second value a list of the centre
		coordinates of each image, and its horizontal and vertical position in the grid of images.
		The coordinate list has the following format:
		((current_latitude, current_longitude), (horizontal, vertical))
		The overall returned format is:
		((num_of_images_total, num_of_images_horizontal, num_of_images_vertical), coordinates_list)
		"""

		(top_lat, left_long), (bottom_lat,
			right_long) = self.geo_location_util.get_top_left_bottom_right_coordinates(
			first_coordinate, second_coordinate
			)

		# start the request in the top left corner
		latitude_first_image, longitude_first_image = self.geo_location_util.normalise_coordinates(top_lat, left_long, zoom)
		current_latitude, current_longitude = latitude_first_image, longitude_first_image

		coordinates_list = []
		num_of_images_horizontal = 0
		num_of_images_vertical = 0

		# iterate from left to right, top to bottom
		while current_latitude > bottom_lat or num_of_images_horizontal == 0:
			while current_longitude < right_long or num_of_images_vertical == 0:
				x_cor_current_tile, y_cor_current_tile = self.geo_location_util.degree_to_tile_value(
					current_latitude, current_longitude, zoom
				)
				coordinates_list.append(
					((current_latitude, current_longitude), (x_cor_current_tile, y_cor_current_tile))
				)
				current_longitude = self.geo_location_util.calc_next_location_longitude(
					current_latitude, current_longitude, zoom, True
				)
				if current_latitude == latitude_first_image:
					num_of_images_vertical += 1

			current_longitude = longitude_first_image
			current_latitude = self.geo_location_util.calc_next_location_latitude(
				current_latitude, current_longitude, zoom, False
			)
			num_of_images_horizontal += 1

		num_of_images_total = num_of_images_horizontal * num_of_images_vertical

		return (num_of_images_total, num_of_images_horizontal,
			num_of_images_vertical), coordinates_list

	def make_request_for_block(self, centre_coordinates, zoom=None):
		"""
		Make a request in such a way, that the images are stored in the tile system, are logged in
		the log manager and they can be displayed on the map
		:param centre_coordinates: the location where the image should be downloaded
		:param zoom: the zoom level at which the image should be downloaded
		:return: nothing
		"""

		if zoom is None:
			zoom = self.top_down_provider.max_zoom

		request_number = self.log_manager.get_request_number()
		request_number_string = str(request_number)

		# a new folder is created for the request if it goes ahead
		new_folder_path = Path.joinpath(
			self.file_handler.folder_overview["image_path"][0], "request_" + request_number_string
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
		new_folder_path = Path.joinpath(
			new_folder_path,
			str(number_tile_downloaded) + "_tile_" + temp_tile_number_latitude + "_" +
			temp_tile_number_longitude
		)
		os.makedirs(new_folder_path)

		# in the case an area should be downloaded, the first thing returned will be the max longitude
		# and latitude
		if len(centre_coordinates) > 9:
			temp = centre_coordinates.pop(0)
			max_latitude = temp[0]

		number_requests = len(centre_coordinates)
		print("Request number: " + str(self.request_number))
		print("Total Images to download: " + str(number_requests))

		number_requests_temp = number_requests
		total_tile_numbers = number_requests / 9
		# stores the information whether or not this is the last tile of the request
		# if yes, information should be logged and no new folder should be created
		last_round = False
		if number_requests == 9:
			last_round = True

		counter = 1
		# download and store the information in the case of only one pair of coordinates
		if len(centre_coordinates) == 9:
			for location in centre_coordinates:
				number = str(counter)
				x_position = str(location[0])
				y_position = str(location[1])
				temp_name = str(number + "_" + x_position + "_" + y_position + ".png")
				self.top_down_provider.get_and_store_location(
					latitude=location[0],
					longitude=location[1],
					zoom=zoom,
					filename=temp_name,
					new_folder_path=new_folder_path
				)
				counter += 1

				if counter == 10 and last_round:
					tile_number = str(tile_number_latitude) + "_" + str(tile_number_longitude)
					self.image_util.concat_images(new_folder_path, counter, tile_number)

					self.file_handler.folder_overview["active_tile_path"][0] = new_folder_path
					self.file_handler.folder_overview["active_image_path"][0] = new_folder_path
					self.file_handler.folder_overview["active_request_path"][
						0] = new_folder_path.parents[0]

		# download and store the information in case a whole area was asked for
		if len(centre_coordinates) > 9:

			for location in centre_coordinates:
				number = str(counter)
				x_position = str(location[0])
				y_position = str(location[1])
				temp_name = str(number + "_" + x_position + "_" + y_position + ".png")
				self.top_down_provider.get_and_store_location(
					latitude=location[0],
					longitude=location[1],
					zoom=self.top_down_provider.max_zoom,
					filename=temp_name,
					new_folder_path=new_folder_path
				)
				counter += 1

				if counter == 10 and not last_round:
					number_tile_downloaded += 1
					tile_number_old = str(tile_number_latitude) + "_" + str(tile_number_longitude)
					self.image_util.concat_images(new_folder_path, counter, tile_number_old)
					tile_number_latitude += 1
					if tile_number_latitude == max_latitude:
						tile_number_latitude = 0
						tile_number_longitude += 1
					tile_number_new = str(tile_number_latitude) + "_" + str(tile_number_longitude)
					new_folder_path = Path.joinpath(
						new_folder_path.parents[0],
						str(number_tile_downloaded) + "_tile_" + tile_number_new
					)
					print(str(number_tile_downloaded) + "/" + str(total_tile_numbers))
					os.makedirs(new_folder_path)
					counter = 1
					number_requests_temp = number_requests_temp - 9
					if number_requests_temp == 9:
						last_round = True

				if counter == 10 and last_round:
					number_tile_downloaded += 1
					tile_number = str(tile_number_latitude) + "_" + str(tile_number_longitude)
					self.image_util.concat_images(new_folder_path, counter, tile_number)

					self.file_handler.folder_overview["active_tile_path"][0] = new_folder_path
					self.file_handler.folder_overview["active_image_path"][0] = new_folder_path
					self.file_handler.folder_overview["active_request_path"][
						0] = new_folder_path.parents[0]
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


