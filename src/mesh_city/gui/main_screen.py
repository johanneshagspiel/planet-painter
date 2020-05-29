"""
See :class:`.MainScreen`
"""

from tkinter import Button, mainloop, Tk, Frame, Text, END, DISABLED, WORD, NORMAL
from mesh_city.gui.export_window.export_window import ExportWindow
from mesh_city.gui.canvas_image.canvas_image import CanvasImage
from mesh_city.gui.detection_window.detection_window import DetectionWindow
from mesh_city.gui.generate_window.generate_window import GenerateWindow
from mesh_city.gui.layers_window.layers_window import LayersWindow
from mesh_city.gui.load_window.load_window import LoadWindow
from mesh_city.gui.search_window.search_window_start import SearchWindowStart
from mesh_city.gui.start_window.start_window import StartWindow

class MainScreen:
	"""
	The main screen of the application where the map is shown as well as as all the function one
	can do on the map such as loading requests or looking at different layers
	"""

	def __init__(self, application):
		"""
		Setting up the main screen
		:param application: the global application context
		"""

		self.application = application
		self.master = Tk()

		self.master.title("Mesh City")
		self.master.geometry("910x665")

		self.master.withdraw()
		self.window = StartWindow(self.master, application)
		self.master.wait_window(self.window.top)
		self.master.deiconify()

		self.active_layers = []

		self.padding_x = 60
		self.padding_y = 5
		self.image_height = 646
		self.image_width = 646

		self.left_bar = Frame(self.master, width=52, height=665, background="white")
		self.left_bar.grid(row=0, column=0, sticky='nsew')
		self.left_bar.grid_propagate(0)

		self.search_button = Button(
			self.left_bar, text="Search", width=6, height=3, command=self.search_window, bg="grey"
		)
		self.search_button.grid(row=0, column=0)

		self.load_button = Button(
			self.left_bar, text="Load", width=6, height=3, command=self.load_window, bg="grey"
		)
		self.load_button.grid(row=1, column=0)

		self.detect_button = Button(
			self.left_bar, text="Detect", width=6, height=3, command=self.detect_window, bg="grey"
		)
		self.detect_button.grid(row=2, column=0)

		self.layers_button = Button(
			self.left_bar, text="Layers", width=6, height=3, command=self.layers_window, bg="grey"
		)
		self.layers_button.grid(row=3, column=0)

		self.generate_button = Button(
			self.left_bar, text="Generate", width=6, height=3, command=self.generate_window, bg="grey"
		)
		self.generate_button.grid(row=4, column=0)

		self.export_button = Button(
			self.left_bar, text="Export", width=6, height=3, command=self.export_window, bg="grey"
		)
		self.export_button.grid(row=5, column=0)

		temp_image_path = next(
			self.application.file_handler.folder_overview["active_image_path"].glob("concat_image_*")
		)

		self.canvas_image = CanvasImage(self.master, temp_image_path)
		self.new_canvas_image = None
		self.canvas_image.grid(row=0, column=1, sticky='nsew')

		self.right_frame = Frame(self.master, width=185, background="white")
		self.right_frame.grid(row=0, column=2, sticky='nsew')
		self.right_frame.grid_propagate(0)

		self.information_general = Text(self.right_frame, width=26, height=30, wrap=WORD)
		self.information_general.configure(font=("TkDefaultFont", 9, "normal"))
		self.information_general.grid(row=0, column=0, sticky="w")
		self.information_general.insert(END, "General")
		#self.information_general.config(state=DISABLED)
		self.information_general.bind("<Double-1>", lambda event: "break")
		self.information_general.bind("<Button-1>", lambda event: "break")
		self.information_general.config(cursor="")

		self.information_selection = Text(self.right_frame, width=26, height=14, wrap=WORD)
		self.information_selection.configure(font=("TkDefaultFont", 9, "normal"))
		self.information_selection.grid(row=1, column=0, sticky="w")
		self.information_selection.insert(END, "Selection")
		#self.information_selection.config(state=DISABLED)
		self.information_selection.bind("<Double-1>", lambda event: "break")
		self.information_selection.bind("<Button-1>", lambda event: "break")
		self.information_selection.config(cursor="")

		self.master.columnconfigure(1, weight=1)
		self.master.rowconfigure(0, weight=1)
		self.master.rowconfigure(1, weight=1)
		self.master.rowconfigure(2, weight=1)

		mainloop()

	def export_window(self):
		"""
		Creates an export window
		:return: Nothing (creates an export window)
		"""
		ExportWindow(self.master, self.application)

	def layers_window(self):
		"""
		Creates a layers window object
		:return: Nothing
		"""
		LayersWindow(self.master, self.application, self)

	def load_window(self):
		"""
		Creates a load request window object
		:return: Nothing
		"""
		LoadWindow(self.master, self.application, self)

	def search_window(self):
		"""
		Creates a search window object
		:return: Nothing
		"""
		SearchWindowStart(self.master, self.application, self)

	def detect_window(self):
		"""
		Creates a detect window object
		:return:
		"""
		DetectionWindow(self.master, self.application, self)

	def generate_window(self):
		"""
		Creates a generate window object
		:return:
		"""
		GenerateWindow(self.master, self.application, self)

	def update_image(self):
		"""
		Calls methods needed to updates the image seen on the map
		:return: Nothing
		"""
		temp_image_path = next(self.application.file_handler.folder_overview["active_image_path"].glob("concat_image_*"))

		self.new_canvas_image = CanvasImage(self.master, temp_image_path)
		self.new_canvas_image.grid(row=0, column=1, sticky='nsew')

	def update_text(self):
		temp_info_path = next(self.application.file_handler.folder_overview["active_information_path"].glob("concat_information*"))
		temp_information_log = self.application.log_manager.read_log(temp_info_path, "information")

		tree_amount = temp_information_log.information["Amount"]
		tree_amount_text = "Amount of trees detected:\n" + str(tree_amount)

		self.information_general.delete('1.0', END)
		self.information_general.insert(END, tree_amount_text)


