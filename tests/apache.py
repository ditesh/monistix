import plugins

class ApachePluginTest:

	def __init__(self, config):
		self.config = config

	def run(self):

		try:
			plugin = plugins.apache.ApachePlugin(self.config)
			return plugin.getData()

		except:
			raise
