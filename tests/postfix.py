import plugins

class PostfixPluginTest:

	def __init__(self, config):
		self.config = config

	def run(self):

		try:
			plugin = plugins.postfix.PostfixPlugin(self.config)
			return plugin.getData()

		except:
			raise
