"""Postfix profile provides data mail queues"""

__author__ = "Ditesh Shashikant Gathani"
__copyright__ = "Copyright (C) 2010 Ditesh Shashikant Gathani"
__license__ = "GPL"
__version__ = "0.1"
__email__ = "ditesh@gathani.org"

import os
import subprocess

class PostfixProfile:

	def __init__(self, config):

		self.config = config
		self.qshapePath = "/usr/sbin/qshape"

		for val in config:

			(key, value) = val

			if key == "qshape_path":
				self.qshapePath = value

		if not os.path.exists(self.qshapePath):
			raise IOError

	def getData(self):

		returnValue = {}

		for item in ["active", "deferred", "bounce", "corrupt", "incoming", "hold"]:
			returnValue[item] = self.getQueueData(item)

		return returnValue

	def getQueueData(self, queue):

		returnValue = {}

		lines = subprocess.Popen([self.qshapePath, queue], stdout=subprocess.PIPE).communicate()[0].split("\n")
		returnValue["totals"] = lines[1:].split()

		for line in lines[2:]:

			columns = line.split()

			try:
				returnValue[columns[0].strip()] = columns[1:]

			except IndexError: continue

		return returnValue
