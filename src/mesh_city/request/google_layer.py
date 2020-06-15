"""
See :class:`.GoogleLayer`
"""

from typing import List

from mesh_city.request.layer import Layer
from mesh_city.request.tile import Tile


class GoogleLayer(Layer):
	"""
	A layer class representing the google imagery that was downloaded.
	"""

	def __init__(self, width: int, height: int, tiles: List[Tile]) -> None:
		self.tiles = tiles
		super().__init__(width, height)