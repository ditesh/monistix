"""Module to encapsulate all monitoring data related code"""

__author__ = "Ditesh Shashikant Gathani"
__copyright__ = "Copyright (C) 2010 Ditesh Shashikant Gathani"
__license__ = "GPL"
__version__ = "0.1"
__email__ = "ditesh@gathani.org"

import os
import sys
import json
import time
import config
import syslog
import hashlib
import httplib
import plugins 
import traceback
from configobj import ConfigObj

"""Module loader and dispatcher"""
class Dispatcher:

	def __init__(self):

		self.services = {}

		try:
			self.configuration = config.MonitorConf()
			self.configuration.readServicesConfig()
			self.configuration.readClientConfig()

		except:
			raise

		self.ms = Store(self.configuration.key, self.configuration.server, self.configuration.cache)

		for host, services in self.configuration.services:

			try:

				if host == "all":

					if configuration.services[host]["enabled"] != "1":
						syslog.syslog(syslog.LOG_WARNING, "Modules not enabled on global level, will not continue")
						raise

				else:

					if "hostname" in services:
						hostname = configuration.services[host]["hostname"]
						del services["hostname"]

					else:
						syslog.syslog(syslog.LOG_WARNING, "Not importing plugins for host " + host + " as hostname is not specified")
						continue

					if "enabled" not in services or services["enabled"] != "1":
						syslog.syslog(syslog.LOG_WARNING, "Not importing plugins for host " + host + " as host is not enabled")
						continue

					del services["enabled"]

					for plugin, configValues in services:

						if "enabled" not in configValue or configValues["enabled"] != "1":
							syslog.syslog(syslog.LOG_WARNING, "Not importing plugin for host " + host + " as its not enabled")
							continue

						if "plugin" not in configValues:
							syslog.syslog(syslog.LOG_WARNING, "Not importing plugin for host " + host + " as its not specified")
							continue

						module = getattr(profiles, configValues["plugin"])
						obj = getattr(module, configValues["plugin"].capitalize() + "Plugin")

						self.services[host][plugin] = obj()


			except (ImportError, AttributeError):
				syslog.syslog(syslog.LOG_WARNING, "Unable to correctly import module profiles/" + service + ".py")

		if len(self.services) == 0:
			syslog.syslog(syslog.LOG_WARNING, "No modules imported, will not continue")
			raise

	def dispatch(self):

		for hostname, plugins in self.services:
			for plugin in plugins:
				startTimestamp = time.time()
				data = plugin.getData()
				timeTaken = time.time() - startTimestamp
				self.ms.store(hostname, plugin.getName(), data, timeTaken)


	def sync(self):

		try:
			self.ms.sync()

		except:
			raise


"""Per instance store"""
class Store:

	def __init__(self, key, server, cache):

		self.data = []
		self.key = key
		self.server = server
		self.cache = cache

	def store(self, service, data, timeTaken):

		self.data.append({

				"hash": hashlib.sha512(str(time.time())).hexdigest(),
				"timestamp": time.time(),
				"time_taken": timeTaken,
				"data": {service: data}

			})


	def sync(self):

		try:
			data = json.dumps(self.data)
			self.sendUpstream(data)
			self.data = []

			self.sendCacheUpstream()

		except:

			syslog.syslog(syslog.LOG_WARNING, "Unable send monitoring data upstream (" + self.server + "), attempting to save to disk")

			try:
				self.save()

			except:
				raise

	def sendUpstream(self, data):

		key = self.key
		server = self.server

		try:
			params = urllib.urlencode(data)
			headers = {"Content-type": "application/x-www-form-urlencoded", "Accept": "text/plain"}

			try:
				conn = httplib.HTTPConnection(server)
				conn.request("POST", "/data?key=" + self.key)
				resp = conn.getresponse()

			except:
				syslog.syslog(syslog.LOG_WARNING, "Unable to connect to server, attempting to save monitoring data")

				try:
					self.save(data)

				except:
					syslog.syslog(syslog.LOG_WARNING, "Error: unable to save monitoring data")
					raise

				raise httplib.HTTPException

		except:
			raise httplib.HTTPException()


	def sendCacheUpstream(self):

		dir = os.listdir(self.cache)

		for file in dir:
			try:
				fp = open(os.path.join(self.cache, file), "r")
				data = fp.read()
				fp.close()

				try:
					sendUpstream(data)

					try:
						os.remove(file)

					except IOError:
						continue

				except httplib.HTTPException:
					break			# don't bother if its not possible to connect

			except IOError: continue


	def save(self):

		data = json.dumps(self.data)
		filePath = os.path.join(self.cache, str(time.time()) + ".json")

		try:
			fp = open(filePath, "w")
			fp.write(data)
			fp.close()

		except:
			syslog.syslog(syslog.LOG_WARNING, "Unable to save monitoring data, cannot write to cache path (" + filePath + "), check permission and path")
			raise

		# empty out data once file has been successfully written
		self.data = []
