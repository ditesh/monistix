import profiles

class BasicProfileTest:

	def __init__(self): pass

	def run(self):
		profile = profiles.basic.BasicProfile()
		print(profile.getData())
