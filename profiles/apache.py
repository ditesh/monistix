"""Apache HTTPD profile provides HTTP server instrumentation data"""

__author__ = "Ditesh Shashikant Gathani"
__copyright__ = "Copyright (C) 2010 Ditesh Shashikant Gathani"
__license__ = "GPL"
__version__ = "0.1"
__email__ = "ditesh@gathani.org"

import syslog
import httplib

class ApacheProfile:

	def __init__(self, config):

		self.host = "localhost"
		self.port = 80
		self.config = config
		self.username = None
		self.password = None

		for val in config:

			(key, value) = val

			if key == "host":
				self.host = value

			if key == "port":
				self.port = value

			if key == "username":
				self.username = value

			if key == "password":
				self.password = value

	def getData(self):

		returnValue = {}

		try:
			conn = httplib.HTTPConnection(self.host + ":" + str(self.port))
			conn.request("GET", "/server-status?auto")
			resp = conn.getresponse()

			if resp.status == 200:

				data = resp.read().split("\n")

				for line in data:

					try:
						items = line.split(":")
						returnValue[items[0].strip().lower().replace(" ", "_")] = items[1].strip()

					except IndexError: continue

		except httplib.HTTPException:
			returnValue = {}
			returnValue["error"] = "Unable to connect to " + self.host + ":" + str(self.port) + "/server-status?auto"
			returnValue["errorcode"] = 1
			syslog.syslog(syslog.LOG_WARNING, returnValue["error"])
			return returnValue

		return returnValue
