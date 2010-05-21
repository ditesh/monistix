import plugins

class SendmailPluginTest:

	def __init__(self, config):
		self.config = config

	def run(self):

		try:
			plugin = plugins.sendmail.SendmailPlugin(self.config)
			return plugin.getData()

		except:
			raise
