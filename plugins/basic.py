"""Basic plugin provides OS specific data:

* CPU use
* Memory use
* Filesystem
"""
__author__ = "Ditesh Shashikant Gathani"
__copyright__ = "Copyright (C) 2010 Ditesh Shashikant Gathani"
__license__ = "GPL"
__version__ = "0.1"
__email__ = "ditesh@gathani.org"

import psutil
import syslog
import subprocess
from base import *

class BasicPlugin(BasePlugin):

	def __init__(self, config):
		self.config = config

	def getData(self):

		cpu = {}
		newcpu = {}
		processes = {}
		memory = self.getMemData()

		if "error" in memory:
			return memory

		filesystemBlocks = self.getFilesystemData(blocks=True)

		if "error" in filesystemBlocks:
			return filesystemBlocks

		filesystemInodes = self.getFilesystemData(inodes=True)

		if "error" in filesystemInodes:
			return filesystemInodes

		netstat= self.getNetstatData()

		if "error" in netstat:
			return netstat 

		networkData = self.getNetworkData()

		if "error" in networkData:
			return networkData

		cpuData = psutil.cpu_times()

		cpu["user"] = cpuData.user
		cpu["system"] = cpuData.system
		cpu["idle"] = cpuData.idle
		cpu["nice"] = cpuData.nice
		cpu["iowait"] = cpuData.iowait
		cpu["irq"] = cpuData.irq
		cpu["softirq"] = cpuData.softirq

		for item in cpu:
			cpu[item] = round(cpu[item], 2)
			newcpu[item] = round(cpu[item], 2)

		try:
			data = open("/proc/stat", "r").read()
			lines = data.split("\n")

			for line in lines:

				items = line.split()

				if "processes" in line:
					processes["total"] = items[1].strip()

				elif "procs_running" in line:
					processes["running"] = items[1].strip()

				elif "procs_blocked" in line:
					processes["blocked"] = items[1].strip()

		except:
			returnValue = {}
			returnValue["error"] = "Unable to read /proc/stat"
			returnValue["errorcode"] = 1
			syslog.syslog(syslog.LOG_WARNING, returnValue["error"])
			return returnValue

		return { "cpu": cpu, "memory": memory, "processes": processes, "filesystem_blocks": filesystemBlocks, "filesystem_inodes": filesystemInodes, "netstat": netstat, "network_data": networkData }


	def getMemData(self):

		returnValue = {}

		try:
			data = open("/proc/meminfo", "r").read()

		except:
			returnValue = {}
			returnValue["error"] = "Unable to read /proc/meminfo"
			returnValue["errorcode"] = 1
			syslog.syslog(syslog.LOG_WARNING, returnValue["error"])
			return returnValue

		lines = data.split("\n")

		for line in lines[:-1]:
			items = line.split()
			returnValue[items[0].strip(":")] = items[1].strip()

		return returnValue

	def getFilesystemData(self, blocks=False, inodes=False):

		returnValue = {}

		try:
			if blocks:
				lines = subprocess.Popen(["/bin/df", "-aP"], stdout=subprocess.PIPE).communicate()[0].split("\n")
			else:
				lines = subprocess.Popen(["/bin/df", "-aPi"], stdout=subprocess.PIPE).communicate()[0].split("\n")

		except OSError:
			returnValue = {}
			returnValue["error"] = "Unable to execute /bin/df"
			returnValue["errorcode"] = 1
			syslog.syslog(syslog.LOG_WARNING, returnValue["error"])
			return returnValue

		for line in lines[1:-1]:
			data = {}
			items = line.split()
			data["blocks"] = items[1]
			data["used"] = items[2]
			data["available"] = items[3]
			data["used_percentage"] = items[4]
			data["mounted_on"] = items[5]

			returnValue[items[0]] = data

		return returnValue

	def getNetstatData(self):

		returnValue = {}
		returnValue["active"] = 0
		returnValue["passive"] = 0
		returnValue["failed"] = 0
		returnValue["resets"] = 0
		returnValue["established"] = 0

		try:
			lines = subprocess.Popen(["/bin/netstat", "-s"], stdout=subprocess.PIPE).communicate()[0].split("\n")

		except OSError:
			returnValue = {}
			returnValue["error"] = "Unable to execute /bin/netstat"
			returnValue["errorcode"] = 1
			syslog.syslog(syslog.LOG_WARNING, returnValue["error"])
			return returnValue


		for line in lines:

			items = line.split()

			if "active connections openings" in line:
				returnValue["active"] = items[0]

			elif "passive connection openings" in line:
				returnValue["passive"] = items[0]

			elif "failed connection attempts" in line:
				returnValue["failed"] = items[0]

			elif "connection resets" in line:
				returnValue["resets"] = items[0]

			elif "connections established" in line:
				returnValue["established"] = items[0]

		return returnValue

	def getNetworkData(self):

		returnValue = {}

		try:
			data = open("/proc/net/dev", "r").read()

		except:
			returnValue = {}
			returnValue["error"] = "Unable to read /proc/net/dev"
			returnValue["errorcode"] = 1
			syslog.syslog(syslog.LOG_WARNING, returnValue["error"])
			return returnValue

		lines = data.split("\n")

		for line in lines[2:-1]:
			items = line.split()
			returnValue[items[0].strip(":")] = {
								"bytes_received": items[1],
								"packets_received": items[2],
								"errors_received": items[3],
								"frames_received": items[6],
								"bytes_sent": items[9],
								"packets_sent": items[10],
								"errors_sent": items[11],
								"frames_sent": items[14]
							}

		return returnValue
