"""NTP plugin provides data on NTP peers"""

__author__ = "Ditesh Shashikant Gathani"
__copyright__ = "Copyright (C) 2010 Ditesh Shashikant Gathani"
__license__ = "GPL"
__version__ = "0.1"
__email__ = "ditesh@gathani.org"

import os
import socket
import syslog
import subprocess
from base import *

class NTPPlugin(BasePlugin):

	def __init__(self, config):

		self.config = config
		self["ntpqPath"] = "/usr/sbin/ntpq"

		self.configure(["ntpqPath"])

		if not os.path.exists(self["ntpqPath"]):
			syslog.syslog(syslog.LOG_WARNING, "Unable to find ntpq (" + self["ntpqPath"] +")")
			raise IOError

	def getData(self):

		returnValue = {}

		try:
			lines = subprocess.Popen([self["ntpqPath"], "-p"], stdout=subprocess.PIPE).communicate()[0].split("\n")

		except OSError:
			returnValue = {}
			returnValue["error"] = "Unable to execute " + self["ntpqPath"]
			returnValue["errorcode"] = 1
			syslog.syslog(syslog.LOG_WARNING, returnValue["error"])
			return returnValue

		for line in lines[2:]:

			if "*" in line:

				data = {}
				items = line.split()
				ip = items[0].strip("*")
				data["hostname"] = socket.getfqdn(ip)
				data["delay"] = items[-3]
				data["offset"] = items[-2]
				data["jitter"] = items[-1]
				returnValue[ip] = data

		return returnValue
