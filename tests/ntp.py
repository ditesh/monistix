import sys
import profiles

class NtpProfileTest:

	def __init__(self, config):
		self.config = config

	def run(self):

		try:
			profile = profiles.ntp.NTPProfile(self.config)
			return profile.getData()

		except:
			raise
