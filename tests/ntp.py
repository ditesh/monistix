import sys
import plugins

class NtpPluginTest:

	def __init__(self, config):
		self.config = config

	def run(self):

		try:
			plugin = plugins.ntp.NTPPlugin(self.config)
			return plugin.getData()

		except:
			raise
