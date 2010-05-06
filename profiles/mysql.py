"""MySQL profile provides MySQL server instrumentation data"""

__author__ = "Ditesh Shashikant Gathani"
__copyright__ = "Copyright (C) 2010 Ditesh Shashikant Gathani"
__license__ = "GPL"
__version__ = "0.1"
__email__ = "ditesh@gathani.org"

import os
import syslog
import subprocess

class MysqlProfile:

	def __init__(self, config):

		self.port = None
		self.config = config
		self.username = None
		self.password = None
		self.mysqladminPath = "/usr/bin/mysqladmin"

		for val in config:

			(key, value) = val

			if key == "username":
				self.username = value

			if key == "password":
				self.password = value

			if key == "port":
				self.port = value

		if not os.path.exists(self.mysqladminPath):
			raise IOError

	def getData(self):

		returnValue = {}

		args = [self.mysqladminPath]

		if self.username != None:
			args.append("-u")
			args.append(self.username)

		if self.password != None:
			args.append("-p" + self.password)

		if self.port != None:
			args.append("-P")
			args.append(self.port)

		args.append("extended")
		args.append("status")

		try:
			values = subprocess.Popen(args, stdout=subprocess.PIPE, stderr=subprocess.PIPE).communicate()

		except OSError:
			returnValue = {}
			returnValue["error"] = "Unable to execute " + self.mysqladminPath
			returnValue["errorcode"] = 1
			syslog.syslog(syslog.LOG_WARNING, returnValue["error"])
			return returnValue

		if "error" in values[1]:
			returnValue = {}
			returnValue["error"] = "Unable to execute " + self.mysqladminPath
			returnValue["errorcode"] = 1
			syslog.syslog(syslog.LOG_WARNING, returnValue["error"])
			return returnValue

		lines = values[0].split("\n")[3:-3]

		for line in lines:

			line = line.split("|")
			returnValue[line[1].strip().lower()] = line[2].strip()
			print line[1].lower()

		return returnValue
