"""Module to encapsulate all configuration related code"""

__author__ = "Ditesh Shashikant Gathani"
__copyright__ = "Copyright (C) 2010 Ditesh Shashikant Gathani"
__license__ = "GPL"
__version__ = "0.1"
__email__ = "ditesh@gathani.org"

import httplib
import ConfigParser
import os
config = ConfigParser.ConfigParser()

class MonitorConf:

	def __init__(self, filePath = "/etc/monitor"):

		self.filePath = filePath

		# sanity checks
		if not os.path.exists(filePath):
			raise IOError

		if not (os.access(filePath, os.R_OK or os.W_OK)):
			raise IOError

		if not (os.access(os.path.join(filePath, 'client.conf'), os.R_OK and os.W_OK)):
			raise IOError

		if not (os.access(os.path.join(filePath, 'services.conf'), os.R_OK and os.W_OK)):
			raise IOError

		if not os.path.exists(os.path.join(filePath, 'client.conf')):
			try:
				open(os.path.join(filePath, 'client.conf'), 'w').close() 
			except:
				raise IOError

		if not os.path.exists(os.path.join(filePath, 'services.conf')):
			try:
				open(os.path.join(filePath, 'services.conf'), 'w').close() 
			except:
				raise IOError

	# Read configuration file
	def readClientConfig(self):

		try:
			config.readfp(open(os.path.join(self.filePath, "client.conf")))

		except IOError:
			raise

		try:
			self.key = config.get("client", "key")

		except ConfigParser.NoOptionError:
			self.key = ""
			
		try:
			self.server = config.get("client", "server")

		except ConfigParser.NoOptionError:
			self.server = ""
		
		try:
			self.cache = config.get("client", "cache")

		except ConfigParser.NoOptionError:
			self.cache = ""

	# Read configuration file
	def readServicesConfig(self):

		try:
			config.readfp(open(os.path.join(self.filePath, "services.conf")))

		except IOError:
			raise

		self.services = config


	# Get list of services
	def getServices(self):

		try:
			conn = httplib.HTTPConnection(self.server)
			conn.request("GET", "/services.php?key=" + self.key)
			resp = conn.getresponse()

		except:
			raise httplib.HTTPException

		# Write to /etc/monitor/services.conf
		if resp.status == 200:

			try:
				open(os.path.join(self.filePath, "services.conf"), "w").write(resp.read())
				return

			except:
				raise IOError

		else:
			raise Exception


	# Validate the account
	def reconfigure(self, key, server):

		self.key = key
		self.server = server

		try:
			conn = httplib.HTTPConnection(server)
			conn.request("GET", "/?key=" + self.key);
			resp = conn.getresponse()

		except:
			raise httplib.HTTPException

		if resp.status == 200:

			try:
				open(os.path.join(self.filePath, "client.conf"), "w").write(resp.read())
				return

			except:
				raise IOError

		else:
			raise Exception
