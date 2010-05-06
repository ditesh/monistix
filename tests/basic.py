import profiles

class BasicProfileTest:

	def __init__(self, config):
		self.config = config

	def run(self):

		try:
			profile = profiles.basic.BasicProfile(self.config)
			print(profile.getData())

		except:
			raise
