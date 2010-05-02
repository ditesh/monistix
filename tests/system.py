import profiles

class SystemProfileTest:

	def __init__(self): pass

	def run(self):
		sp = profiles.system.SystemProfile()
		print(sp.getData())
