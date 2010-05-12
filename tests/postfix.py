import profiles

class PostfixProfileTest:

	def __init__(self, config):
		self.config = config

	def run(self):

		try:
			profile = profiles.postfix.PostfixProfile(self.config)
			return profile.getData()

		except:
			raise
