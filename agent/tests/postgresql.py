import plugins

class PostgresqlPluginTest:

	def __init__(self, config):
		self.config = config

	def run(self):

		try:
			plugin = plugins.postgresql.PostgreSQLPlugin(self.config)
			return plugin.getData()

		except:
			raise
