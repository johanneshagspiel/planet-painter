import math
from pathlib import Path
import requests
from PIL import Image

class ahn_entity:
	temp_path = Path(__file__).parents[2]
	images_folder_path = Path.joinpath(temp_path, 'resources','images')
	color_to_height = {(12, 52, 124) : -7.5,
	                   (12, 68, 132) : -6.5,
	                   (12, 84, 132) : -5.5,
	                   (12, 92, 132) : -4.5,
	                   (20, 108, 140) : -3.5,
	                   (28, 116, 140) : -2.75,
	                   (20, 132, 140) : -2.25,
	                   (28, 148, 148) : -1.75,
	                   (36, 148, 148) : -1.25,
	                   (36, 156, 140) : -0.75,
	                   (20, 164, 132) : -0.25,
	                   (28, 172, 124) : 0.25,
	                   (28, 180, 108) : 0.75,
	                   (20, 188, 100) : 1.25,
	                   (20, 188, 84) : 1.75,
	                   (12, 196, 68) : 2.25,
	                   (4, 204, 52) : 3, #2.5-3, 3-3.5
	                   (4, 220, 4) : 4, #3.5-4, 4-4.5
	                   (44, 228, 4) : 4.75,
	                   (68, 228, 4) : 5.5,
	                   (100, 236, 4) : 6.5,
	                   (124, 236, 4) : 7.5,
	                   (148, 244, 4) : 8.5,
	                   (180, 244, 4) : 9.5,
	                   (204, 244, 4) : 11,
	                   (236, 252, 4) : 13,
	                   (252, 252, 4) : 15,
	                   (252, 244, 4) : 17,
	                   (252, 228, 4) : 19,
	                   (244, 212, 4) : 25, #20-25, 25-30
	                   (252, 196, 12) : 32.5,
		               (244, 188, 4) : 37.5,
		               (244, 180, 20) : 42.5,
		               (244, 164, 20) : 47.5,
		               (236, 164, 20) : 55,
		               (244, 156, 20) : 65,
		               (228, 140, 28) : 75,
		               (228, 132, 36) : 85,
		               (220, 124, 36) : 95,
		               (212, 108, 44) : 125,#100-125, 125-150
		               (204, 100, 52) : 162.5,
	                   (204, 92, 52) : 187.5,
	                   (196, 84, 60) : 250, #200-250, 250-300
	                   }

	def __init__(self):
		self.request_number = 0

	def get_and_store_location(self, x, y, name):

		bounding_box_coordinates = self.calculate_bounding_box(x, y, 20, 640, 640)

		xmin = str(bounding_box_coordinates[0])
		ymin = str(bounding_box_coordinates[1])
		xmax = str(bounding_box_coordinates[2])
		ymax = str(bounding_box_coordinates[3])
		width = str(640)
		height = str(640)

		#response = requests.get("https://geodata.nationaalgeoregister.nl/ahn3/wms?request=GetMap&service=wms&CRS=EPSG:4326&bbox=51.998903,4.373492,52.001003,4.374203&width=650&height=650&layers=ahn3_05m_dtm&styles=ahn3:ahn3_05m_detail&format=image/png&version=1.30")

		response = requests.get("https://geodata.nationaalgeoregister.nl/ahn3/wms?request=GetMap&service=wms"
		                        "&CRS=EPSG:4326&"
		                        "bbox="+ xmin + "," + ymin + "," + xmax + "," + ymax +
		                        "&width=" + width +
		                        "&height=" + height +
		                        "&layers=ahn3_05m_dsm"
		                        "&styles=ahn3:ahn3_05m_detail"
		                        "&format=image/png"
		                        "&version=1.30")

		filename = name
		to_store = Path.joinpath(self.images_folder_path, filename)

		with open(to_store, 'wb') as output:
			_ = output.write(response.content)

		#self.increase_request_number()

	def calculate_bounding_box(self, x, y, zoom, image_size_x, image_size_y):
		right = self.calc_next_location_latitude(x, y, zoom, image_size_x / 2, True)
		left = self.calc_next_location_latitude(x, y, zoom, image_size_x / 2, False)
		up = self.calc_next_location_longitude(x, y, zoom, image_size_y / 2, True)
		down = self.calc_next_location_longitude(x, y, zoom, image_size_y / 2, False)

		self.check_in_netherlands(left, down)
		self.check_in_netherlands(right, up)

		return [left, down, right, up]

	def check_in_netherlands(self, x, y):
		if(x < 50.671799068129744 or x > 53.61086457823865
			or y < 3.197334098049271 or y > 7.275203841667622):
			print("Height information is only available in the Netherlands - Sorry!")

	def calc_next_location_latitude(self, latitude, longitude, zoom, image_size_x, direction):
		metersPerPx = 156543.03392 * math.cos(latitude * math.pi / 180) / math.pow(2, zoom)
		next_center_distance_meters = metersPerPx * image_size_x
		if(direction == True):
			new_latitude = latitude + (next_center_distance_meters / 6378137) * (
				180 / math.pi)
		else:
			new_latitude = latitude - (next_center_distance_meters / 6378137) * (
					180 / math.pi)
		return new_latitude

	def calc_next_location_longitude(self, latitude, longitude, zoom, image_size_y, direction):
		metersPerPx = 156543.03392 * math.cos(latitude * math.pi / 180) / math.pow(2, zoom)
		next_center_distance_meters = metersPerPx * image_size_y
		if (direction == True):
			new_longitude = longitude + (next_center_distance_meters / 6378137) * (
				180 / math.pi) / math.cos(latitude * math.pi / 180)
		else:
			new_longitude = longitude - (next_center_distance_meters / 6378137) * (
				180 / math.pi) / math.cos(latitude * math.pi / 180)
		return new_longitude

	def load_images_map(self, x, y):
		down = self.calc_next_location_latitude(x,y,20,640,False)
		up = self.calc_next_location_latitude(x,y,20,640,True)
		right = self.calc_next_location_longitude(x,y,20,640,True)
		left = self.calc_next_location_longitude(x,y,20,640,False)

		up_left = self.get_and_store_location(up, left,"up_left.png")
		up_center = self.get_and_store_location(up, y,"up_center.png")
		up_right = self.get_and_store_location(up, right, "up_right.png")
		center_left = self.get_and_store_location(x, left, "center_left.png")
		center_center = self.get_and_store_location(x, y, "center_center.png")
		center_right = self.get_and_store_location(x, right, "center_right.png")
		down_left = self.get_and_store_location(down, left, "down_left.png")
		down_center = self.get_and_store_location(down, y, "down_center.png")
		down_right = self.get_and_store_location(down, right, "down_right.png")

	def increase_request_number(self):
		old_usage = self.request_number
		self.request_number = old_usage + 1
