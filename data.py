"""Module to encapsulate all monitoring data related code"""

__author__ = "Ditesh Shashikant Gathani"
__copyright__ = "Copyright (C) 2010 Ditesh Shashikant Gathani"
__license__ = "GPL"
__version__ = "0.1"
__email__ = "ditesh@gathani.org"

import sys
import json
import time
import httplib
import configuration

"""Monitoring module loader and """
class MonitoringDispatcher:

	def __init__(self):

		self.services = {}

		try:
			self.monitorConf = configuration.MonitorConf()
			self.monitorConf.readServicesConfig()
			self.monitorConf.readClientConfig()

		except:
			raise

		self.ms = MonitoringStore(self.monitorConf.key, self.monitorConf.server)

		for service in self.monitorConf.services.sections():

			try:
				module = __import__(service)
				obj = getattr(module, service.capitalize() + "Profile")
				self.services[service] = obj()

			except:
				print >> sys.stderr, "Unable to correctly import " + service + ".py"

	def getData(self):

		for service in self.services:
			data = self.services[service].getData()
			self.ms.store(service, data)


"""Per instance store"""
class MonitoringStore:

	def __init__(self, key, server):
		self.data = []
		self.key = key
		self.server = server

	def store(self, name, value):
		obj.store(value)
		self.data.push(obj)

	def sendUpstream(self):

		key = config.get("client", "key")
		server = config.get("client", "server")
		data = json.dumps(self.data)

		try:
			params = urllib.urlencode(data)
			headers = {"Content-type": "application/x-www-form-urlencoded", "Accept": "text/plain"}

			try:
				conn = httplib.HTTPConnection(server)
				conn.request("POST", "/data?key=" + self.key)
				resp = conn.getresponse()

			except:
				print >> sys.stderr, "Error: unable to connect to server, attempting to save monitoring data"

				try:
					self.save(data)

				except:
					print >> sys.stderr, "Error: unable to save monitoring data"
					raise

				raise httplib.HTTPException

		except:
			raise httplib.HTTPException



	def save(self, data):

		cache = config.get("client", "cache")
		filePath = os.path.join(cache, time()+".json")

		if os.access(filePath, os.R_OK or os.W_OK):

			try:
				fp = open(filePath, "w")
				fp.write(data)
				fp.close()

			except:
				raise

		else:
			print sys.stderr, "Unable save monitoring data, cannot write to cache path (check permission and path)"
