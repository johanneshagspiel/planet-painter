from pathlib import Path

import rasterio
from rasterio.features import shapes


class RasterVectorConverter:

	@staticmethod
	def mask_to_vector(detection_mask: Path) -> [[[(float, float)]]]:

		with rasterio.open(detection_mask) as file:
			image = file.read()

		return [
			geometry["coordinates"] for geometry, value in shapes(source=image, mask=(image == 255))
		]

	@staticmethod
	def vector_to_bounding_boxes(polygons: [[[(float, float)]]]) -> [((int, int), (int, int))]:
		bounding_boxes = []
		for polygon in polygons:
			for coords_group in polygon:
				top, bottom, left, right = None, None, None, None
				for image_coord in coords_group:
					if top is None:
						top = image_coord[0]
					if bottom is None:
						bottom = image_coord[0]
					if left is None:
						left = image_coord[1]
					if right is None:
						right = image_coord[1]

					top = min(image_coord[0], top)
					bottom = max(image_coord[0], bottom)
					left = min(image_coord[1], left)
					right = max(image_coord[1], right)
				bounding_boxes.append(((top, left), (bottom, right)))
		return bounding_boxes
