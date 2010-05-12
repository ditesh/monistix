import profiles

class SendmailProfileTest:

	def __init__(self, config):
		self.config = config

	def run(self):

		try:
			profile = profiles.sendmail.SendmailProfile(self.config)
			return profile.getData()

		except:
			raise
