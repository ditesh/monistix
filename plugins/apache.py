"""Apache HTTPD plugin provides HTTP server instrumentation data"""

__author__ = "Ditesh Shashikant Gathani"
__copyright__ = "Copyright (C) 2010 Ditesh Shashikant Gathani"
__license__ = "GPL"
__version__ = "0.1"
__email__ = "ditesh@gathani.org"

import syslog
import httplib
from base import *

class ApachePlugin(BasePlugin):

	def __init__(self, config):

		self.config = config

		self["port"] = 80
		self["username"] = None
		self["password"] = None
		self["hostname"] = "127.0.0.1"

		self.configure(["hostname", "port", "username", "password"])


	def getData(self):

		returnValue = {}

		try:
			conn = httplib.HTTPConnection(self["hostname"] + ":" + str(self["port"]))
			conn.request("GET", "/server-status?auto")
			resp = conn.getresponse()

			if resp.status == 200:

				data = resp.read().split("\n")

				for line in data:

					try:
						items = line.split(":")
						returnValue[items[0].strip().lower().replace(" ", "_")] = items[1].strip()

					except IndexError: continue

		except:
			returnValue = {}
			returnValue["error"] = "Unable to connect to http://" + self["hostname"] + ":" + str(self["port"]) + "/server-status?auto"
			returnValue["errorcode"] = 1
			syslog.syslog(syslog.LOG_WARNING, returnValue["error"])
			return returnValue

		return returnValue
