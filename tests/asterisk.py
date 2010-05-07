import profiles

class AsteriskProfileTest:

	def __init__(self, config):
		self.config = config

	def run(self):

		try:
			profile = profiles.asterisk.AsteriskProfile(self.config)
			print(profile.getData())

		except:
			raise
