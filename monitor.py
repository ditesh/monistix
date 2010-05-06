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
import hashlib
import httplib
import profiles
import traceback

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

		for service in self.configuration.services.sections():

			try:
				module = getattr(profiles, service)
				obj = getattr(module, service.capitalize() + "Profile")

				try:
					configValues = configuration.services.items(service)

				except ConfigParser.NoSectionError:
					configValues = []

				self.services[service] = obj(configValues)

			except (ImportError, AttributeError):
				print >> sys.stderr, "Unable to correctly import module profiles/" + service + ".py"

		if len(self.services) == 0:
			print >> sys.stderr, "No modules imported, will not continue"
			raise

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

	def store(self, service, data):

		self.data.append({

				"hash": hashlib.sha512(str(time.time())).hexdigest(),
				"timestamp": time.time(),
				"data": {service: data}

			})


	def sync(self):

		try:
			data = json.dumps(self.data)
			self.sendUpstream(data)
			self.data = []

			self.sendCacheUpstream()

		except:

			print >> sys.stderr, "Unable send monitoring data upstream (" + self.server + "), attempting to save to disk"

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
				print >> sys.stderr, "Error: unable to connect to server, attempting to save monitoring data"

				try:
					self.save(data)

				except:
					print >> sys.stderr, "Error: unable to save monitoring data"
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
			print >> sys.stderr, "Unable save monitoring data, cannot write to cache path (" + filePath + "), check permission and path"
			raise

		# empty out data once file has been successfully written
		self.data = []
