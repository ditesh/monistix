import plugins

class MysqlPluginTest:

	def __init__(self, config):
		self.config = config

	def run(self):

		try:
			plugin = plugins.mysql.MysqlPlugin(self.config)
			return plugin.getData()

		except:
			raise
