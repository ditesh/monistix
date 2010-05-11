import sys
import profiles
from libs.exceptions import *

class AsteriskProfileTest:

	def __init__(self, config):
		self.config = config

	def run(self):

		try:
			profile = profiles.asterisk.AsteriskProfile(self.config)
			return profile.getData()

		except InvalidConfiguration as e:
			print >> sys.stderr, e
			raise

		except:
			raise
