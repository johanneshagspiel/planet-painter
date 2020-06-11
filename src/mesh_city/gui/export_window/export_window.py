"""
A module containing the export window class
"""

import os
from pathlib import Path
from tkinter import Button, Checkbutton, filedialog, IntVar, Label, Toplevel

from mesh_city.request.google_layer import GoogleLayer
from mesh_city.request.trees_layer import TreesLayer


class ExportWindow:
	"""
	The window where the user can select what they want to export as well as where to export that to
	"""

	def __init__(self, master, application):
		"""
		First asks the user which request to export
		:param master: the master tkinter application
		:param application: the global application context
		"""
		self.master = master
		self.value = ""
		self.application = application
		self.top = Toplevel(master)
		self.image_path = self.application.file_handler.folder_overview['image_path']

		self.top_label = Label(self.top, text="Which request do you want to export?")
		self.top_label.grid(row=0)
		active_request_id = self.application.current_request.request_id
		temp_text = "Active Request: Request " + str(active_request_id)
		self.request_buttons = []
		self.request_buttons.append(
			Button(
			self.top,
			text=temp_text,
			width=20,
			height=3,
			command=lambda: self.load_request(self.application.current_request),
			bg="grey"
			)
		)
		for (index, request) in enumerate(self.application.request_manager.requests):
			if request.request_id != active_request_id:
				self.request_buttons.append(
					Button(
					self.top,
					text="Request " + str(request.request_id),
					width=20,
					height=3,
					command=lambda: self.load_request(request),
					bg="grey"
					)
				)
		for (index, request_button) in enumerate(self.request_buttons):
			request_button.__grid(row=index + 1, column=0)

	def load_request(self, request):
		"""
		Loads the request. Then asks the user which features of this request to export
		:param name_directory: the directory where the request is stored
		:return: nothing (the window is updated to now show which features to export)
		"""
		for button in self.request_buttons:
			button.grid_forget()
		self.top_label.forget()

		self.application.set_current_request(request=request)
		self.top_label.configure(text="What do you want to export?")
		self.int_variable_list = []
		for (index, layer) in enumerate(request.layers):
			self.int_variable_list.append(IntVar())
			text = ""
			if isinstance(layer, GoogleLayer):
				text = "Google Imagery"
			elif isinstance(layer, TreesLayer):
				text = "Tree detections CSV"
			Checkbutton(self.top, text=text,
				variable=self.int_variable_list[index]).grid(row=index + 1)

		Button(self.top, text="Confirm",
			command=lambda: self.cleanup(request)).grid(row=len(request.layers) + 1)

	def cleanup(self, request):
		"""
		Asks the user to select a folder to export to. Then copies all the files into this folder
		:return: nothing (the desired images are exported to a folder)
		"""
		layer_mask = []
		has_export = False
		for (layer, element) in zip(request.layers, self.int_variable_list):
			if element.get() == 1:
				has_export = True
			layer_mask.append(element.get() == 1)

		if has_export:
			export_directory = Path(filedialog.askdirectory())
			self.application.export_request_layers(
				request=request, layer_mask=layer_mask, export_directory=export_directory
			)
		self.top.destroy()
