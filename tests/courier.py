import plugins

class CourierPluginTest:

	def __init__(self, config):
		self.config = config

	def run(self):

		try:
			plugin = plugins.courier.CourierPlugin(self.config)
			return plugin.getData()

		except:
			raise
