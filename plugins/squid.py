"""Squid plugin provides data on Squid proxy"""

__author__ = "Ditesh Shashikant Gathani"
__copyright__ = "Copyright (C) 2010 Ditesh Shashikant Gathani"
__license__ = "GPL"
__version__ = "0.1"
__email__ = "ditesh@gathani.org"

import os
import glob
import syslog

class SquidPlugin(BasePlugin):

	def __init__(self, config):

		self.config = config
		self["accesslogPath"] = "/var/log/squid/access.log"

		self.configure(["accesslog_path"])

		if not os.path.exists(self.accesslogPath):
			syslog.syslog(syslog.LOG_WARNING, "Unable to find access log path (" + self["accesslogPath"] +")")
			raise IOError

	def getData(self):

		returnValue = {}
		return returnValue
