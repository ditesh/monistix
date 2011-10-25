"""MySQL plugin provides MySQL server instrumentation data"""

__author__ = "Ditesh Shashikant Gathani"
__copyright__ = "Copyright (C) 2010 Ditesh Shashikant Gathani"
__license__ = "GPL"
__version__ = "0.1"
__email__ = "ditesh@gathani.org"

import os
import syslog
import subprocess
from base import *

class MysqlPlugin(BasePlugin):

	def __init__(self, config):

		self.config = config

		self["port"] = 3306
		self["username"] = None
		self["password"] = None
		self["hostname"] = "127.0.0.1"
		self["mysqlAdminPath"] = "/usr/bin/mysqladmin"

		self.configure(["hostname", "port", "username", "password", "mysqlAdminPath"])

		if not os.path.exists(self["mysqlAdminPath"]):
			raise IOError

	def getData(self):

		returnValue = {}

		args = [self["mysqlAdminPath"]]
		args.append("-h")
		args.append(self["hostname"])

		if self["username"] != None:
			args.append("-u")
			args.append(self["username"])

		if self["password"] != None:
			args.append("-p" + self["password"])

		args.append("-P")
		args.append(self["port"])

		args.append("extended")
		args.append("status")

		try:
			values = subprocess.Popen(args, stdout=subprocess.PIPE, stderr=subprocess.PIPE).communicate()

		except OSError:
			returnValue = {}
			returnValue["error"] = "Unable to execute " + self["mysqlAdminPath"]
			returnValue["errorcode"] = 1
			syslog.syslog(syslog.LOG_WARNING, returnValue["error"])
			return returnValue

		if "error" in values[1]:
			returnValue = {}
			returnValue["error"] = "Got an error when running " + self["mysqlAdminPath"] + ": '" + values[1] + "'"
			returnValue["errorcode"] = 1
			syslog.syslog(syslog.LOG_WARNING, returnValue["error"])
			return returnValue

		lines = values[0].split("\n")[3:-3]

		for line in lines:

			line = line.split("|")
			returnValue[line[1].strip().lower()] = line[2].strip()

		return returnValue
