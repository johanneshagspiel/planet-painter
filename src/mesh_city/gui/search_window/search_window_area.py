"""
See :class:`.SearchWindowLocationArea`
"""

from tkinter import Button, Entry, Label, Toplevel

from mesh_city.gui.search_window.preview_window import PreviewWindow


class SearchWindowLocationArea:
	"""
	A pop-up type GUI element that the user can fill in to make an area-type request.
	.. todo:: Make a pop-up class that this inherits from.
	"""

	def __init__(self, master, application, main_screen):
		"""
		Initializes the GUI elements of the pop-up and sets up callbacks
		:param master: The Tk root.
		:param application: The application object that is used to make requests.
		:param main_screen: The main screen object the popups interacts with.
		"""
		self.main_screen = main_screen
		self.master = master
		self.value = ""
		self.application = application
		top = self.top = Toplevel(master)

		Label(top, text="Which area are you interested in downloading ?").grid(row=0, column=3)

		self.min_lat = Label(top, text="Min Latitude:")
		self.min_lat.grid(row=1, column=1)
		self.min_log = Label(top, text="Min Longitude:")
		self.min_log.grid(row=2, column=1)
		self.max_lat = Label(top, text="Max Latitude:")
		self.max_lat.grid(row=3, column=1)
		self.max_log = Label(top, text="Max Longitude:")
		self.max_log.grid(row=4, column=1)

		self.min_lat_entry = Entry(top, width=20)
		self.min_lat_entry.grid(row=1, column=3)
		self.min_long_entry = Entry(top, width=20)
		self.min_long_entry.grid(row=2, column=3)
		self.max_lat_entry = Entry(top, width=20)
		self.max_lat_entry.grid(row=3, column=3)
		self.max_long_entry = Entry(top, width=20)
		self.max_long_entry.grid(row=4, column=3)

		self.temp_1 = Label(self.top, text="Please enter address information in this form:")
		self.temp_1.grid(row=5, column=4)
		self.temp_2 = Label(self.top, text="{house number} {street} {postcode} {city} {country}")
		self.temp_2.grid(row=6, column=4)

		Button(top, text="Search", command=self.cleanup).grid(row=5, column=3)

		self.type_button_min = Button(
			top, text="Address", command=lambda: self.change_search_type(True, "min")
		)
		self.type_button_min.grid(row=1, column=4)

		self.type_button_max = Button(
			top, text="Address", command=lambda: self.change_search_type(True, "max")
		)
		self.type_button_max.grid(row=3, column=4)

	def change_search_type(self, first_time, name):
		"""
		Changes the search type from address-based to coordinate-based or the other way around.
		:param first_time: A flag indicating whether this is the first time the type button is pressed
		:param name: The name indicating which of the points of the rectangle-defined area is to
		have a different typ.
		:return:
		"""

		if name == "min":
			if self.min_lat["information_general"] == "Min Latitude:":
				self.min_lat["information_general"] = "Address:"
				self.min_long_entry.grid_forget()
				self.type_button_min.configure(text="Coordinates")
				self.min_log["information_general"] = ""
				first_time = False

			if (self.min_lat["information_general"] == "Address:") & first_time:
				self.min_lat["information_general"] = "Min Latitude:"
				self.min_long_entry.grid(row=2, column=3)
				self.type_button_min.configure(text="Address")
				self.min_log["information_general"] = "Min Longitude:"

		if name == "max":
			if self.max_lat["information_general"] == "Max Latitude:":
				self.max_lat["information_general"] = "Address:"
				self.max_long_entry.grid_forget()
				self.type_button_max.configure(text="Coordinates")
				self.max_log["information_general"] = ""
				first_time = False

			if (self.max_lat["information_general"] == "Address:") & first_time:
				self.max_lat["information_general"] = "Max Latitude:"
				self.max_long_entry.grid(row=4, column=3)
				self.type_button_max.configure(text="Address")
				self.max_log["information_general"] = "Max Longitude:"

	def cleanup(self):
		"""
		Makes the area-type request and cleans up after itself by tearing down the GUI and
		effectively returning control to the main screen.
		"""
		self.value = [
			float(self.min_lat_entry.get()),
			float(self.min_long_entry.get()),
			float(self.max_lat_entry.get()),
			float(self.max_long_entry.get()),
		]

		PreviewWindow(
			main_screen=self.main_screen,
			master=self.master,
			application=self.application,
			coordinates=self.value
		)
		self.top.destroy()
