import sys
import plugins
from libs.exceptions import *

class AsteriskPluginTest:

	def __init__(self, config):
		self.config = config

	def run(self):

		try:
			plugin = plugins.asterisk.AsteriskPlugin(self.config)
			return plugin.getData()

		except InvalidConfiguration as e:
			print >> sys.stderr, e
			raise

		except:
			raise
