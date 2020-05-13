from mesh_city.gui.self_made_map import SelfMadeMap
from mesh_city.imagery_provider.request_manager import RequestManager
from mesh_city.user.quota_manager import QuotaManager
from mesh_city.user.user_info_handler import UserInfoHandler


class Application:

	def __init__(self):
		self.user_info_handler = UserInfoHandler()
		self.self_made_map = SelfMadeMap(application=self)
		self.quota_manager = None
		self.request_manager = None
		self.user_info = None

		self.self_made_map()

	def update(self):
		self.user_info_handler.store_user_info(self.user_info)
		self.quota_manager = QuotaManager(self.user_info)
		self.request_manager = RequestManager(self.user_info, self.quota_manager)


