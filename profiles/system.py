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
import subprocess

try:
	import psutil

except ImportError:
	raise

class SystemProfile:

	def __init__(self): pass

	def getData(self):

		uname = os.uname()
		pythonVersion = sys.version 
		hostname = socket.gethostname()
		cpuData = subprocess.Popen(["/usr/bin/lscpu"], stdout=subprocess.PIPE).communicate()[0]
		pciData = subprocess.Popen(["/sbin/lspci"], stdout=subprocess.PIPE).communicate()[0]

		fp = open("/proc/partitions", "r")
		diskData = fp.read()
		fp.close()

		self.getOS()

		return { "uname": uname, "python_version": pythonVersion, "hostname": hostname, "cpu_data": cpuData, "pci_data": pciData, "disk_data": diskData, "os_name": self.osName, "os_version": self.osVersion}

	def getOS(self):

		self.osName = ""
		self.osVersion = 0

		filenames = [	"/etc/redhat-release",
				"/etc/SuSE-release"]

		for filename in filenames:

			if os.path.isfile(filename):

				fp = open(filename, "r")
				data = fp.read()
				fp.close()

				if (data.find("Fedora") >= 0):
					self.osName = "Fedora"
					self.osVersion = data[15:16]

				elif (data.find("Red Hat Enterprise Linux") >= 0):
					self.osName = "Red Hat Enterprise Linux"
					self.osVersion = data[42:44]
