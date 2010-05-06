import profiles

class MysqlProfileTest:

	def __init__(self, config):
		self.config = config

	def run(self):

		try:
			profile = profiles.mysql.MysqlProfile(self.config)
			print(profile.getData())

		except:
			raise
