import os
import sys
import libs.config as config

class ConfigTest:

	def __init__(self, config):
		self.config = config

	def run(self):

		try:
			configuration = config.MonitorConf(os.path.join(os.getcwd(), "tests"))
			
		except IOError:
			print >> sys.stderr, "tests/client.conf or tests/services.conf is not readable/writable"
			raise

		try:
			configuration.readServicesConfig()
			configuration.readClientConfig()
			return configuration.services

		except:
			raise

