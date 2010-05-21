import plugins

class BasicPluginTest:

	def __init__(self, config):
		self.config = config

	def run(self):

		try:
			plugin = plugins.basic.BasicPlugin(self.config)
			return plugin.getData()

		except:
			raise
