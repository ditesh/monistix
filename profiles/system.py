"""System Profile gets system level information:

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
		cpuData = subprocess.call("/usr/bin/lscpu")
		pciData = subprocess.call("/usr/bin/lspci")
		diskData = open("/proc/partitions", "r").read().close()
		

		return { "uname": uname, "python_version": pythonVersion, "hostname": hostname, "cpu_data": cpuData, "pci_data": pciData, "disk_data": diskData, "os_name": self.osData, "os_version": self.osVersion}

	def getOS(self):

		filenames = [
				"/etc/redhat-release",
				"/etc/SuSE-release"]

		for filename in filenames:

			if os.path.is_file(filename)

				data = open(filename, "r").read().write()

				if (data.find("Fedora") > 0):
					osName = "Fedora"
					osVersion = data[15:16]

				else if (data.find("Red Hat Enterprise Linux") > 0):
					osName = "Red Hat Enterprise Linux"
					osVersion = data[42:44]


		if (str(os) == 0):
			osName = data
			osVersion = 0

		self.osName = osName
		self.osVersion = osVersion
