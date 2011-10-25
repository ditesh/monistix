"""Base plugin for other plugins"""

__author__ = "Ditesh Shashikant Gathani"
__copyright__ = "Copyright (C) 2010 Ditesh Shashikant Gathani"
__license__ = "GPL"
__version__ = "0.1"
__email__ = "ditesh@gathani.org"

import string

class BasePlugin:

	logs = []
	data = {}

	"""This method is called to get plugin name.

	This method should be implemented by plugins, else a
	default name is computed and returned

	"""
	def getName(self):

		returnValue = str(self.__class__).replace("Plugin", "")

		if "." in returnValue:
			index = returnValue.rfind(".")

			if index != -1:
				return returnValue[index + 1:]

			return returnValue


	"""This method is called to get instrumentation data.

	This method must be implemented by plugins

	"""
	def getData(self):
		raise NotImplemented

	"""This method is called to set configuration data from config value set.

	This method can be overriden by plugins

	"""
	def configure(self, keys):

		for key in keys:
			if key in self.config:
				if "log" in key:
					self.logs[self.camelizeName(key)]["path"] = self.config[key]
				else:
					self[self.camelizeName(key)] = self.config[key]

	"""This method is called to get logs.

	The logic is as follows:

		1) If file position does not exist, open log file and set file position to start of file
		2) If file size is smaller then file position, its a good chance logs have been rotated (or just plain gone missing).
			a) Run log negotiation
				* Read log dir
				* Get list of files matching logfilename*
				* Get MD5
				* Submit to server
			b) Set file position to 0
		3) Read file from file position to end
		4) Save log data, close file pointer

	"""

	def getLogData(self):

		for logname in self["logs"]:

			path = self["logs"][logname]["path"]

			if "position" not in self["logs"][logname]:
				position = 0

			else:

				position = self["logs"][logname]["position"]

				try:
					filesize = os.path.getsize(path)

					if (filesize < position):
						position = 0

#						doLogNegotiation()

				except:
					raise

			try:
				fp = open(path, "r")
				fp.seek(position)
				self["logs"][logname]["position"] = fp.tell()

			except:
				raise

			while True:

				data = fp.readline()

				if data == "":
					break

				returnValue += data

			fp.close()

		return returnValue

	def camelizeName(self, key):

		pos = string.find(key, "_")

		if pos == -1 or pos == (len(key) - 1):
			return key

		return key[0:pos] + key[pos + 1:].capitalize()

	def __setitem__(self, key, value):
		self.data[key] = value


	def __getitem__(self, key):
		return self.data[key]
