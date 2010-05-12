import profiles

class SystemProfileTest:

	def __init__(self, config):
		self.config = config

	def run(self):

		try:
			profile = profiles.system.SystemProfile(self.config)
			return profile.getData()

		except:
			raise
