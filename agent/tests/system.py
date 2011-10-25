import plugins

class SystemPluginTest:

	def __init__(self, config):
		self.config = config

	def run(self):

		try:
			plugin = plugins.system.SystemPlugin(self.config)
			return plugin.getData()

		except:
			raise
