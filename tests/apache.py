import profiles

class ApacheProfileTest:

	def __init__(self, config):
		self.config = config

	def run(self):

		try:
			profile = profiles.apache.ApacheProfile(self.config)
			print(profile.getData())

		except:
			raise
