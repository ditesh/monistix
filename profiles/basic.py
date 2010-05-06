"""Basic profile provides OS specific data:

* CPU use
* Memory use
* Filesystem
"""
__author__ = "Ditesh Shashikant Gathani"
__copyright__ = "Copyright (C) 2010 Ditesh Shashikant Gathani"
__license__ = "GPL"
__version__ = "0.1"
__email__ = "ditesh@gathani.org"

try:
	import psutil

except ImportError:
	raise

class BasicProfile:

	def __init__(self): pass

	def getData(self):

		cpu = {}
		newcpu = {}
		mem = {}
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

		mem["total"] = psutil.TOTAL_PHYMEM
		mem["available"] = psutil.avail_phymem()
		mem["used"] = psutil.used_phymem()
		mem["total_virtmem"] = psutil.total_virtmem()
		mem["avail_virtmem"] = psutil.avail_virtmem()
		mem["used_virtmem"] = psutil.used_virtmem()

		for item in mem:
			mem[item] = round(mem[item], 2)

		return { "cpu": cpu, "memory": mem }
