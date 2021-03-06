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

		for host in self.configuration.services:

			services = self.configuration.services[host]

			try:

				if host == "all":

					if self.configuration.services[host]["enabled"] != "1":
						syslog.syslog(syslog.LOG_WARNING, "Modules not enabled on global level, will not continue")
						raise

				else:

					self.services[host] = {}

					if "hostname" in services:
						hostname = self.configuration.services[host]["hostname"]
						del services["hostname"]

					else:
						syslog.syslog(syslog.LOG_WARNING, "Not importing plugins for host " + host + " as hostname is not specified")
						continue

					if "enabled" not in services or services["enabled"] != "1":
						syslog.syslog(syslog.LOG_WARNING, "Not importing plugins for host " + host + " as host is not enabled")
						continue

					del services["enabled"]

					for section in services:

						configValues = services[section]

						if "plugin" not in configValues:
							syslog.syslog(syslog.LOG_WARNING, "Not importing plugin for host " + host + " (section: " + section + ") as no plugin is specified")
							continue

						if "enabled" not in configValues or configValues["enabled"] != "1":
							syslog.syslog(syslog.LOG_WARNING, "Not importing plugin for host " + host + " (section: " + section + ", plugin: " + configValues["plugin"] + ") as its not enabled")
							continue

						module = getattr(plugins, configValues["plugin"])
						obj = getattr(module, configValues["plugin"].capitalize() + "Plugin")

						self.services[host][section] = obj(configValues)


			except (ImportError, AttributeError):
				traceback.print_exc(file=sys.stdout)
				syslog.syslog(syslog.LOG_WARNING, "Unable to correctly import plugins/" + configValues["plugin"] + ".py")

		noPlugins = True

		for host in self.services:

			if len(self.services[host]) > 0:
				noPlugins = False

		if noPlugins:
			syslog.syslog(syslog.LOG_WARNING, "No plugins imported, will not continue")
			raise Exception

	def dispatch(self):

		for hostname in self.services:

			plugins = self.services[hostname]

			for plugin in plugins:
				obj = plugins[plugin]
				startTimestamp = time.time()
				data = obj.getData()
				print obj.getName()
				timeTaken = time.time() - startTimestamp
				self.ms.store(hostname, obj.getName(), data, timeTaken)


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

	def store(self, hostname, service, data, timeTaken):

		self.data.append({

				"hash": hashlib.sha512(str(time.time())).hexdigest(),
				"hostname": hostname,
				"service": service,
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
