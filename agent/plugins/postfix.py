"""Postfix plugin provides data on mail queues"""

__author__ = "Ditesh Shashikant Gathani"
__copyright__ = "Copyright (C) 2010 Ditesh Shashikant Gathani"
__license__ = "GPL"
__version__ = "0.1"
__email__ = "ditesh@gathani.org"

import os
import re
import syslog
import subprocess
from base import *

class PostfixPlugin(BasePlugin):

	def __init__(self, config):

		self.config = config
		self["qshapePath"] = "/usr/sbin/qshape"
		self["maillogPath"] = "/var/log/maillog"

		self.configure(["qshape_path", "maillog_path"])

		if not os.path.exists(self.qshapePath):
			syslog.syslog(syslog.LOG_WARNING, "Unable to find qshape (" + self["qshapePath"] + ")")
			raise IOError

		if not os.path.exists(self.maillogPath):
			syslog.syslog(syslog.LOG_WARNING, "Unable to find maillog (" + self["maillogPath"] + ")")
			raise IOError

		self.maillogTailPosition = 0

	def getData(self):

		returnValue = {}

		for item in ["active", "deferred", "bounce", "corrupt", "incoming", "hold"]:
			try:
				returnValue[item] = self.getQueueData(item)

			except OSError:
				returnValue = {}
				returnValue["error"] = "Unable to execute " + self["qshapePath"]
				returnValue["errorcode"] = 1
				return returnValue

		try:
			returnValue = getMailStats()

		except IOError:
			returnValue = {}
			returnValue["error"] = "Unable to read " + self["maillogPath"]
			returnValue["errorcode"] = 1
			syslog.syslog(syslog.LOG_WARNING, returnValue["error"])
			return returnValue

		return returnValue


	def getMailVolume(self):

		volume = 0
		rejected = 0
		delivered = 0

		try:
			filesize = os.path.getsize(self["maillogPath"])

			if (filesize < self.maillogTailPosition):
				self.maillogTailPosition = 0

			fp = open(self.maillogPath, "r")
			fp.seek(self.maillogTailPosition)

			while True:

				line = fp.readline()
				self.maillogTailPosition = fp.tell()

				if line == "":
					break

				matches = re.search('.*?qmgr.*?from=.*?size=([0-9]+)', line)

				if matches != None:
					volume += int(matches.group(1))
					delivered += 1

				matches = re.search('.*?reject.*', line)

				if matches != None:
					rejected += 1

			fp.close()

		except:
			raise

		return { "volume": volume, "rejected": rejected, "delivered": delivered }


	def getQueueData(self, queue):

		returnValue = {}

		try:
			lines = subprocess.Popen([self["qshapePath"], queue], stdout=subprocess.PIPE).communicate()[0].split("\n")

		except OSError:
			raise

		returnValue["total_in_queue"] = lines[1:].split()

		for line in lines[2:]:

			columns = line.split()

			try:
				returnValue[columns[0].strip()] = columns[1:]

			except IndexError: continue

		return returnValue
