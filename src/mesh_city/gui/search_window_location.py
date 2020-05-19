"""
See :class:`~SearchWindowLocation`
"""

from pathlib import Path
from tkinter import Button, Entry, Label, Toplevel


class SearchWindowLocation:
	"""
	A pop-up type GUI element that the user can fill in to make a location-type request.
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

		Label(top, text="Which location are you interested in downloading ?").grid(row=0, column=3)

		self.latitude = Label(top, text="Latitude:")
		self.latitude.grid(row=1, column=1)
		self.longitude = Label(top, text="Longitude:")
		self.longitude.grid(row=2, column=1)

		self.lat_entry = Entry(top, width=20)
		self.lat_entry.grid(row=1, column=3)
		self.long_entry = Entry(top, width=20)
		self.long_entry.grid(row=2, column=3)

		self.address_info_1 = Label(self.top, text="Please enter the address in this form:")
		self.address_info_1.grid(row=3, column=4)
		self.address_info_2 = Label(
			self.top, text="{house number} {street} {postcode} {city} {country}"
		)
		self.address_info_2.grid(row=4, column=4)

		self.search_button = Button(top, text="Search", command=self.cleanup)
		self.search_button.grid(row=3, column=3)
		self.type_button = Button(
			top, text="Address", command=lambda: self.change_search_type(True)
		)
		self.type_button.grid(row=1, column=4)

	def change_search_type(self, first_time):
		"""
		Changes the search type from address-based to coordinate-based or the other way around.
		:param first_time: A flag indicating whether this is the first time the type button is pressed
		:return: None
		"""
		if self.latitude['text'] == "Latitude:":
			self.latitude['text'] = "Address:"
			self.long_entry.grid_forget()
			self.type_button.configure(text="Coordinates")
			self.longitude['text'] = ""
			first_time = False

		if (self.latitude['text'] == "Address:") & first_time:
			self.latitude.config(text="Latitude:")
			self.long_entry.grid(row=2, column=3)
			self.type_button.configure(text="Address")
			self.longitude['text'] = "Longitude:"

	def cleanup(self):
		"""
		Makes the location-type request and cleans up after itself by tearing down the GUI and
		effectively returning control to the main screen.
		:return: None
		"""
		self.value = [float(self.lat_entry.get()), float(self.long_entry.get())]
		self.application.request_manager.make_request_for_block(self.value)
		self.main_screen.currently_active_tile = self.application.request_manager.active_tile_path
		self.main_screen.currently_active_request = Path(self.main_screen.currently_active_tile
														).parents[0]
		self.main_screen.update_image()
		self.top.destroy()
