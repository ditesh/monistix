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
import httplib
import config

"""Module loader and dispatcher"""
class Dispatcher:

	def __init__(self):

		self.services = {}

		try:
			self.monitorConf = config.MonitorConf()
			self.monitorConf.readServicesConfig()
			self.monitorConf.readClientConfig()

		except:
			raise

		self.ms = Store(self.monitorConf.key, self.monitorConf.server, self.monitorConf.cache)

		for service in self.monitorConf.services.sections():

			try:
				module = __import__(service)
				obj = getattr(module, service.capitalize() + "Profile")
				self.services[service] = obj()

			except:
				print >> sys.stderr, "Unable to correctly import module " + service + ".py"

	def dispatch(self):

		for service in self.services:
			data = self.services[service].getData()
			self.ms.store(service, data)

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

	def store(self, key, value):

		self.data.append({key: value})


	def sync(self):

		try:
			self.sendUpstream()

		except:

			print >> sys.stderr, "Unable send monitoring data upstream (" + self.server + "), attempting to save to disk"

			try:
				self.save()

			except:
				raise

	def sendUpstream(self):

		key = self.key
		server = self.server
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



	def save(self):

		data = json.dumps(self.data)
		filePath = os.path.join(self.cache, str(time.time()) + ".json")

		try:
			fp = open(filePath, "w")
			fp.write(data)
			fp.close()

		except:
			print >> sys.stderr, "Unable save monitoring data, cannot write to cache path (check permission and path)"
			raise
