# Manage configuration

import httplib, ConfigParser, os
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

	def read(self):
		try:
			config.readfp(open(os.path.join(self.filePath, "client.conf")))

		except IOError as (errno, strerror):
			raise

		key = config.get("client", "key")
		server = config.get("client", "server")

		self.key = key
		self.server = server

	# Get list of services
	def getServices(self):

		conn = httplib.HTTPConnection(self.server)
		conn.request("GET", "/?key=" + self.key)
		resp = conn.getresponse()

		# Write to /etc/monitor/services.conf
		if resp.status == 200:

			data = resp.read

			try:
				configFile = open(os.path.join(self.filePath, "services.conf"), "w")
				configFile.write(data)

			except ConfigParser.NoSectionError:
				raise ConfigParser.NoSectionError

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
				raise

		else:
			raise IOError
