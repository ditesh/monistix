import profiles

class PostgresqlProfileTest:

	def __init__(self, config):
		self.config = config

	def run(self):

		try:
			profile = profiles.postgresql.PostgreSQLProfile(self.config)
			return profile.getData()

		except:
			raise
