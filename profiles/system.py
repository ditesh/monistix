"""System profile provides system level data:

* Hardware installed
	- CPU
	- Memory
	- Network cards
	- Disks
* OS installed
* Python version
"""

__author__ = "Ditesh Shashikant Gathani"
__copyright__ = "Copyright (C) 2010 Ditesh Shashikant Gathani"
__license__ = "GPL"
__version__ = "0.1"
__email__ = "ditesh@gathani.org"

import os
import sys
import socket
import syslog
import subprocess

try:
	import psutil

except ImportError:
	raise

class SystemProfile:

	def __init__(self, config):
		self.config = config

	def getData(self):

		cpuData = {}
		pciData = {}
		diskData = []
		uname = os.uname()
		pythonVersion = sys.version 
		hostname = socket.gethostname()

		try:
			lines = subprocess.Popen(["/usr/bin/lscpu"], stdout=subprocess.PIPE).communicate()[0].split("\n")

		except OSError:

			returnValue = {}
			returnValue["error"] = "Unable to execute /usr/bin/lscpu"
			returnValue["errorcode"] = 1
			syslog.syslog(syslog.LOG_WARNING, returnValue["error"])
			return returnValue

		for line in lines:

			columns = line.split(":")

			try:
				cpuData[columns[0].strip()] = columns[1].strip()

			except IndexError: pass

		try:
			lines = subprocess.Popen(["/sbin/lspci"], stdout=subprocess.PIPE).communicate()[0].split("\n")

		except OSError:
			returnValue = {}
			returnValue["error"] = "Unable to execute /sbin/lspci"
			returnValue["errorcode"] = 1
			syslog.syslog(syslog.LOG_WARNING, returnValue["error"])
			return returnValue

		for line in lines:

			try:
				key = line[0:7]
				value = line[8:]
				pciData[key] = value

			except IndexError: pass

		try:
			fp = open("/proc/partitions", "r")
			lines = fp.read().split("\n")
			fp.close()

			for line in lines[2:-2]:
				columns = line.split()
				diskData.append(columns)

		except IOError:
			returnValue = {}
			returnValue["error"] = "Unable to read /proc/partitions"
			returnValue["errorcode"] = 1
			syslog.syslog(syslog.LOG_WARNING, returnValue["error"])
			return returnValue

		try:
			self.getOS()

		except IOError:
			returnValue = {}
			returnValue["error"] = "Unable to read /etc/*-release or /etc/*-version"
			returnValue["errorcode"] = 1
			syslog.syslog(syslog.LOG_WARNING, returnValue["error"])
			return returnValue

		return { "uname": uname, "python_version": pythonVersion, "hostname": hostname, "cpu_data": cpuData, "pci_data": pciData, "disk_data": diskData, "os_name": self.osName, "os_version": self.osVersion}


	def getOS(self):

		self.osName = ""
		self.osVersion = 0

		filenames = [	"/etc/redhat-release",
				"/etc/SuSE-release"]

		for filename in filenames:

			if os.path.isfile(filename):

				try:
					fp = open(filename, "r")
					data = fp.read()
					fp.close()

				except:
					raise

				if (data.find("Fedora") >= 0):
					self.osName = "Fedora"
					self.osVersion = data[15:16]

				elif (data.find("Red Hat Enterprise Linux") >= 0):
					self.osName = "Red Hat Enterprise Linux"
					self.osVersion = data[42:44]
