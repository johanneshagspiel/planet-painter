"""
See :class:`.Application`
"""

from pathlib import Path
from typing import List, Sequence

from PIL import Image

from mesh_city.detection.detection_observer import DetectionObserver
from mesh_city.detection.detection_pipeline import DetectionPipeline, DetectionType
from mesh_city.detection.information_string_builder import InformationStringBuilder
from mesh_city.gui.main_screen import MainScreen
from mesh_city.gui.request_renderer import RequestRenderer
from mesh_city.logs.log_manager import LogManager
from mesh_city.request.entities.request import Request
from mesh_city.request.request_exporter import RequestExporter
from mesh_city.request.request_maker import RequestMaker
from mesh_city.request.request_manager import RequestManager
from mesh_city.request.request_observer import RequestObserver
from mesh_city.scenario.scenario import Scenario
from mesh_city.scenario.scenario_exporter import ScenarioExporter
from mesh_city.scenario.scenario_pipeline import ScenarioPipeline
from mesh_city.scenario.scenario_renderer import ScenarioRenderer
from mesh_city.util.file_handler import FileHandler


class Application:
	"""
	The main application class. Encapsulates the program's state and acts as a type of hub.
	"""

	def __init__(self):
		self.file_handler = FileHandler()
		self.overlay_image = Image.open(
			self.file_handler.folder_overview["resource_path"].joinpath("trees-overlay.png")
		)
		self.log_manager = LogManager(file_handler=self.file_handler)
		self.request_maker = None
		self.user_entity = None
		self.current_request = None
		self.current_scenario = None
		self.request_manager = self.get_request_manager()
		self.request_maker = RequestMaker(request_manager=self.request_manager)
		self.request_observer = None
		self.main_screen = None
		bio_path = self.file_handler.folder_overview['biome_index']
		self.info_builder = InformationStringBuilder(bio_path)

	def get_main_screen(self) -> MainScreen:
		"""
		Gets the MainScreen instance of this Application
		:return: The MainScreen instance
		"""
		return self.main_screen

	def get_request_manager(self) -> RequestManager:
		"""
		Creates a RequestManager instance and makes it load both previous requests and references to downloaded
		imagery.

		:return: The RequestManager instance with requests and grid loaded from disk.
		"""

		request_manager = RequestManager(self.file_handler.folder_overview["image_path"])
		request_manager.load_data()
		return request_manager

	def set_user_entity(self, user_entity):
		"""
		Initialises the fields that need the user information.
		"""

		self.user_entity = user_entity

	def run_detection(self, request: Request, to_detect: Sequence[DetectionType]) -> None:
		"""
		Runs a detection based on the current request information and the layers that have to be
		detected.

		:param request: The request to run detections for
		:param to_detect: The detections to run
		:return: None
		"""
		detection_observer = DetectionObserver(self.main_screen.master)
		pipeline = DetectionPipeline(self.file_handler, self.request_manager, to_detect)
		pipeline.attach_observer(detection_observer)

		new_layers = pipeline.process(request)

		pipeline.detach_observer(detection_observer)

		for new_layer in new_layers:
			self.current_request.add_layer(new_layer)

	def create_scenario(self, request: Request, modification_list):
		"""
		Creates a scenario based on a request
		:param request: A Request
		:param modification_list: A para
		:param name:
		:return:
		"""
		pipeline = ScenarioPipeline(modification_list=modification_list)
		self.current_scenario = pipeline.process(request)
		self.load_scenario_onscreen(scenario=self.current_scenario)

	def make_location_request(self, latitude: float, longitude: float, name: str = None) -> None:
		"""
		Makes a location request and updates the application correspondingly.

		:param latitude: The latitude of the request
		:param longitude: The longitude of the request
		:return: None
		"""
		self.request_observer = RequestObserver(self.main_screen.master)
		self.request_maker.attach_observer(self.request_observer)

		finished_request = self.request_maker.make_location_request(
			latitude=latitude, longitude=longitude, name=name
		)

		self.request_maker.detach_observer(self.request_observer)

		self.process_finished_request(request=finished_request)

		self.log_manager.write_log(self.user_entity)

	@staticmethod
	def compute_appropriate_scaling(request: Request) -> int:
		"""
		Computes an appropriate scaling to use for rendering requests and scenario's
		:param request: The request to compute an appropriate scaling for
		:return: A scaling that should allow fast rendering of scenario's
		"""
		area_in_tiles = request.num_of_vertical_images * request.num_of_horizontal_images
		# A base scaling
		scaling: int = 2
		# Further lowering of resolution depending on the resolution of the request
		while area_in_tiles > 9:
			area_in_tiles /= 4
			scaling *= 2
		return scaling

	def make_area_request(
		self,
		bottom_latitude: float,
		left_longitude: float,
		top_latitude: float,
		right_longitude: float,
		name: str = None
	) -> None:
		"""
		Makes an area request and updates the application correspondingly.

		:param bottom_latitude: The bottom-most latitude value
		:param left_longitude: The leftmost longitude value
		:param top_latitude: The top-most latitude value
		:param right_longitude: The rightmost longitude value
		:return: None
		"""
		self.request_observer = RequestObserver(self.main_screen.master)
		self.request_maker.attach_observer(self.request_observer)

		finished_request = self.request_maker.make_area_request(
			bottom_latitude=bottom_latitude,
			left_longitude=left_longitude,
			top_latitude=top_latitude,
			right_longitude=right_longitude,
			name=name
		)

		self.request_maker.detach_observer(self.request_observer)

		self.process_finished_request(request=finished_request)

		self.log_manager.write_log(self.user_entity)

	def set_current_request(self, request: Request) -> None:
		"""
		Sets the current request to a new Request and updates the view accordingly.

		:param request:
		:return:
		"""
		self.current_request = request
		self.load_request_onscreen(request)
		self.main_screen.active_layers = ["Google Maps"]

	def load_request_specific_layers(self, request: Request, layer_mask: List[bool]) -> None:
		"""
		Loads specific layers of a request onto the screen.

		:param request: The request to load
		:param layer_mask: A boolean mask representing which layers to render.
		:return: None
		"""

		canvas_image = RequestRenderer.render_request(
			request=request,
			layer_mask=layer_mask,
			scaling=Application.compute_appropriate_scaling(request)
		)
		self.main_screen.set_canvas_image(canvas_image)

		layer_list = []
		for (index, element) in enumerate(layer_mask):
			if element is True:
				layer_list.append(self.current_request.layers[index])

		text_to_show = self.info_builder.process_request(request=self.current_request)
		self.main_screen.update_text(text_to_show)
		self.main_screen.render_dynamic_widgets()

	def export_request_layers(
		self, request: Request, layer_mask: List[bool], export_directory: Path
	) -> None:
		"""
		Export a set of layers from a Request.

		:param request: The request to export
		:param layer_mask: A boolean mask representing which layers to export.
		:param export_directory: A path to the root of where the layers should be exported to.
		:return: None
		"""

		request_exporter = RequestExporter(request_manager=self.request_manager)
		request_exporter.export_request_layers(
			request=request, layer_mask=layer_mask, export_directory=export_directory
		)

	def export_scenario(self, scenario: Scenario, export_directory: Path) -> None:
		"""
		Exports scenario's certain requests belonging to a request to an export directory.
		:param scenario: Which scenario to export
		:param export_directory: The directory to export the scenario to
		:return:
		"""

		request_exporter = ScenarioExporter(
			request_manager=self.request_manager, overlay_image=self.overlay_image
		)
		request_exporter.export_scenario(scenario=scenario, export_directory=export_directory)

	def load_request_onscreen(self, request: Request) -> None:
		"""
		Loads a request on screen.
		:param request: The request to load on screen.
		:return: None
		"""
		canvas_image = RequestRenderer.create_image_from_layer(
			request=request, layer_index=0, scaling=Application.compute_appropriate_scaling(request)
		)
		self.main_screen.set_canvas_image(canvas_image)
		text_to_show = self.info_builder.process_request(request=self.current_request)
		self.main_screen.update_text(text_to_show)
		self.main_screen.render_dynamic_widgets()

	def load_scenario_onscreen(self, scenario: Scenario) -> None:
		"""
		Shows a given scenario on screen.
		:param scenario: The scenario to load on screen
		:return: None
		"""
		canvas_image = ScenarioRenderer.render_scenario(
			scenario=scenario,
			scaling=Application.compute_appropriate_scaling(scenario.request),
			overlay_image=self.overlay_image
		)
		self.main_screen.set_canvas_image(canvas_image)

		text_to_show = self.info_builder.process_scenario(scenario=self.current_scenario)
		self.main_screen.update_text(text_to_show)
		self.main_screen.render_dynamic_widgets()

	def process_finished_request(self, request: Request) -> None:
		"""
		Adds a made request to the RequestManager of the Application sets the state of the Application
		accordingly with the made request becoming the current request.

		:param request: The request that was made
		:return: None
		"""

		self.request_manager.add_request(request)
		self.request_manager.serialize_requests()
		self.set_current_request(request=request)
		self.main_screen.render_dynamic_widgets()

	def start(self):
		"""
		Creates a MainScreen UI element and passes self as application context.

		:return: None
		"""

		self.main_screen = MainScreen(application=self)
		self.main_screen.run()
