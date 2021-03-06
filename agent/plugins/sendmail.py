"""Sendmail plugin provides data on Sendmail mail queues"""

__author__ = "Ditesh Shashikant Gathani"
__copyright__ = "Copyright (C) 2010 Ditesh Shashikant Gathani"
__license__ = "GPL"
__version__ = "0.1"
__email__ = "ditesh@gathani.org"

import os
import glob
import syslog
import subprocess
from base import *

class SendmailPlugin(BasePlugin):

	def __init__(self, config):

		self.config = config

		self["mtaPath"] = "/var/spool/mqueue"
		self["mspPath"] = "/var/spool/mqueue-client"
		self["mailstatsPath"] = "/usr/sbin/mailstats"

		self.configure(["mta_path", "msp_path", "mailstats_path"])

		if not os.path.exists(self["mtaPath"]):
			syslog.syslog(syslog.LOG_WARNING, "Unable to find MTA path (" + self["mtaPath"] + ")")
			raise IOError

	def getData(self):

		returnValue = {}

		mta = glob.glob(self["mtaPath"])
		returnValue["totals"] = len(mta)

		if os.path.exists(self["mspPath"]):
			msp = glob.glob(self["mspPath"])
			returnValue["total_in_queue"] += len(msp)

		try:
			lines = subprocess.Popen([self["mailstatsPath"], "-P"], stderr=subprocess.PIPE, stdout=subprocess.PIPE).communicate()[0].split("\n")

		except OSError:
			raise

		if len(lines) == 1:
			returnValue = {}
			returnValue["error"] = "No permission to get mailstats"
			returnValue["errorcode"] = 1
			syslog.syslog(syslog.LOG_WARNING, returnValue["error"])
			return returnValue

		for line in lines:

			items = line.split()

			if items[0] == "T":

				returnValue["sent"] = items[1]
				returnValue["traffic_sent"] = items[2]
				returnValue["received"] = items[3]
				returnValue["traffic_received"] = items[4]
				returnValue["rejected"] = items[5]
				returnValue["discarded"] = items[6]
				break

		return returnValue
