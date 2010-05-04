import profiles

class SystemProfileTest:

	def __init__(self): pass

	def run(self):
		profile = profiles.system.SystemProfile()
		print(profile.getData())
