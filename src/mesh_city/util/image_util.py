"""
See :class:`.ImageUtil`
"""

from pathlib import Path

from PIL import Image


class ImageUtil:
	"""
	Collection of functions related to assembling map tile images.
	"""

	# def __init__(self, application):
	# 	self.application = application
	# 	self.file_handler = self.application.file_handler

	temp_path = Path(__file__).parents[1]
	path_to_temp = Path.joinpath(temp_path, "resources", "temp")

	def concat_images_list(self, image_list):

		up_left = Image.open(image_list[0])
		up_center = Image.open(image_list[1])
		up_right = Image.open(image_list[2])
		center_left = Image.open(image_list[3])
		center_center = Image.open(image_list[4])
		center_right = Image.open(image_list[5])
		down_left = Image.open(image_list[6])
		down_center = Image.open(image_list[7])
		down_right = Image.open(image_list[8])

		level_0 = self.get_concat_horizontally(
			self.get_concat_horizontally(up_left, up_center), up_right
		)
		level_1 = self.get_concat_horizontally(
			self.get_concat_horizontally(center_left, center_center), center_right
		)
		level_2 = self.get_concat_horizontally(
			self.get_concat_horizontally(down_left, down_center), down_right
		)

		temp_concat_image = self.get_concat_vertically(self.get_concat_vertically(level_2, level_1),
			level_0)

		return temp_concat_image

	def combine_images_list(self, image_list, iteration_amount):

		temp_list = []
		temp_entry = None
		counter = 0

		for number in range(0, len(image_list)):

			if counter == 0:
				temp_entry = image_list[number]
				counter += 1
			else:
				new_temp_1 = image_list[number]
				new_temp = self.get_concat_horizontally(temp_entry, new_temp_1)
				temp_entry = new_temp
				counter += 1

			if counter % iteration_amount == 0:
				temp_list.insert(0, temp_entry)
				counter = 0

		first_Round = True
		temp_entry = None
		for number in range(0, len(temp_list)):

			if first_Round is True:
				temp_entry = temp_list[number]
				first_Round = False
			else:
				new_temp = self.get_concat_vertically(temp_entry, temp_list[number])
				temp_entry = new_temp

		return temp_entry

	def concat_images(self, new_folder_path, request, tile_number):
		"""
		Combines nine tile images into one.
		:param new_folder_path: The directory containing the tile images
		:param request: The number of the request
		:param tile_number: The lat/long identification of this tile
		:return: Nothing
		"""

		up_left = Image.open(next(new_folder_path.glob("1_*")))
		up_center = Image.open(next(new_folder_path.glob("2_*")))
		up_right = Image.open(next(new_folder_path.glob("3_*")))
		center_left = Image.open(next(new_folder_path.glob("4_*")))
		center_center = Image.open(next(new_folder_path.glob("5_*")))
		center_right = Image.open(next(new_folder_path.glob("6_*")))
		down_left = Image.open(next(new_folder_path.glob("7_*")))
		down_center = Image.open(next(new_folder_path.glob("8_*")))
		down_right = Image.open(next(new_folder_path.glob("9_*")))
		images = [
			up_left,
			up_center,
			up_right,
			center_left,
			center_center,
			center_right,
			down_left,
			down_center,
			down_right
		]
		result = self.concat_image_grid(3, 3, images)
		temp_name = "request_" + str(request) + "_tile_" + tile_number
		result.save(Path.joinpath(new_folder_path, "concat_image_" + temp_name + ".png"))

	@staticmethod
	def concat_image_grid(width, height, images):
		"""
		Combines a given array of images into a concatenated grid of images.
		:param width: The width of the grid
		:param height: The height of the grid
		:param images: The images to concatenate. There should be width*height images to fill the grid,
	    and images should be a flattened matrix from left to right, top to bottom.
		:return: Nothing
		"""
		if len(images) != width * height:
			raise ValueError(
				"Not enough images were supplied to concatenate an image grid of the specified size"
			)
		result = images[0]
		for x_coord in range(1, width):
			result = ImageUtil.get_concat_horizontally(result, images[x_coord])
		for y_coord in range(1, height):
			new_layer = images[y_coord * width]
			for x_coord in range(1, width):
				new_layer = ImageUtil.get_concat_horizontally(
					new_layer, images[y_coord * width + x_coord]
				)
			result = ImageUtil.get_concat_vertically(result, new_layer)
		return result

	@staticmethod
	def get_concat_horizontally(image_1, image_2):
		request_string = str(request)
		temp_name = "request_" + request_string + "_tile_" + tile_number
		temp_path = Path.joinpath(new_folder_path, "concat_image_" + temp_name + ".png")

		self.get_concat_vertically(self.get_concat_vertically(level_2, level_1),
			level_0).save(temp_path)

		return temp_path

	def get_concat_horizontally(self, image_1, image_2):
		"""
		Combines two tile images horizontally.
		:param image_1: The left image.
		:param image_2: The right image.
		:return: The combined image.
		"""
		temp = Image.new("RGB", (image_1.width + image_2.width, image_1.height))
		temp.paste(image_1, (0, 0))
		temp.paste(image_2, (image_1.width, 0))
		return temp

	@staticmethod
	def get_concat_vertically(image_1, image_2):
		"""
		Combines two tile images vertically.
		:param image_1: The top image.
		:param image_2: The bottom image.
		:return: Nothing.
		"""
		temp = Image.new("RGB", (image_1.width, image_1.height + image_2.height))
		temp.paste(image_1, (0, 0))
		temp.paste(image_2, (0, image_1.height))
		return temp
