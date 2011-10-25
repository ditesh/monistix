"""Courier plugin provides data on Courier mail queues"""

__author__ = "Ditesh Shashikant Gathani"
__copyright__ = "Copyright (C) 2010 Ditesh Shashikant Gathani"
__license__ = "GPL"
__version__ = "0.1"
__email__ = "ditesh@gathani.org"

import os
import glob
import syslog
from base import *

class CourierPlugin(BasePlugin):

	def __init__(self, config):

		self.config = config
		self["maillogPath"] = "/var/log/mail.log"

		self.configure(["maillog_path", "mailqueue_path"])

		if not os.path.exists(self["maillogPath"]):
			syslog.syslog(syslog.LOG_WARNING, "Unable to find maillog (" + self["maillogPath"] + ")")
			raise IOError

		if not os.path.exists(self["maillogPath"]):
			syslog.syslog(syslog.LOG_WARNING, "Unable to find mailqueue (" + self["mailqueuePath"] + ")")
			raise IOError

		self.maillogTailPosition = 0

	def getData(self):

		returnValue = {}
		queue = self.getQueueCount()

		if "error" in queue:
			return queue

		returnValue["total"] = queue["total"]

		try:
			
			filesize = os.path.getsize(self["maillogPath"])

			if (filesize < self.maillogTailPosition):
				self.maillogTailPosition = 0

			fp = open(self["maillogPath"], "r")
			fp.seek(self.maillogTailPosition)

			while True:

				line = fp.readline()
				self.maillogTailPosition = fp.tell()

				if line == "":
					break

				if "delivered" in line:
					delivered += 1

				elif "rejected" in line:
					rejected += 1

		except:
			returnValue = {}
			returnValue["error"] = "Unable to connect to read maillog file " + self["maillogPath"]
			returnValue["errorcode"] = 1
			syslog.syslog(syslog.LOG_WARNING, returnValue["error"])
			return returnValue

		return { "delivered": delivered, "rejected": rejected }


	def getQueueCount(self):

		returnValue = {}

		try:
			files = glob.glob(self["mailqueuePath"])

		except:
			returnValue = {}
			returnValue["error"] = "Unable to get list of files from the mail queue (" + self["mailqueuePath"] + ")"
			returnValue["errorcode"] = 1
			syslog.syslog(syslog.LOG_WARNING, returnValue["error"])
			return returnValue

		returnValue["total"] = len(files)
		return returnValue
