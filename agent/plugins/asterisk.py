"""Asterisk plugin provides Asterisk specific instrumentation data"""

__author__ = "Ditesh Shashikant Gathani"
__copyright__ = "Copyright (C) 2010 Ditesh Shashikant Gathani"
__license__ = "GPL"
__version__ = "0.1"
__email__ = "ditesh@gathani.org"

import socket 
import syslog
import httplib
from base import *
from libs.exceptions import *

class AsteriskPlugin(BasePlugin):

	def __init__(self, config):

		self.buffer = 4096
		self.config = config

		self["port"] = 5038
		self["username"] = None
		self["password"] = None
		self["hostname"] = "localhost"

		self.configure(["hostname", "port", "username", "password"])

		if self["username"] == None or self["password"] == None:
			syslog.syslog(syslog.LOG_WARNING, "Invalid configuration")
			raise InvalidConfiguration("Asterisk username and/or password not specified")

		try:
			self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
			self.socket.connect((self["hostname"], self["port"]))
			self.socket.recv(self.buffer)	# a hack
			self.socket.send(self.getLoginText())
			data = self.getSocketData()

			if "Authentication failed" in data:
				syslog.syslog(syslog.LOG_WARNING, "Unable to authenticate to ami://" + self["hostname"] + ":" + str(self["port"]))
				raise socket.error

			return

		except socket.error:
			raise

		except:
			syslog.syslog(syslog.LOG_WARNING, "Unable to connect to ami://" + self["hostname"] + ":" + str(self["port"]))
			raise

	def getData(self):

		returnValue = {}
		returnValue["all_channels"] = self.getChannels()
		returnValue["sip_peers"] = self.getSIPPeers()
		returnValue["sip_channels"] = self.getSIPChannels()
#		returnValue["zap_channels"] = self.getZapChannels()
#		returnValue["meetme"] = self.getMeetme()
#		returnValue["voicemail_users"] = self.getVoicemailUsers()

		self.socket.close()
		return returnValue

	def getChannels(self):

		zap = 0
		sip = 0
		iax2 = 0
		returnValue = {}
		returnValue["channels"] = []

		try:
			self.sendCommand('core show channels')
			data = self.getSocketData()

			if "Permission denied" in data:
				returnValue = {}
				returnValue["error"] = "No permission to run command 'core show channels' on ami://" + self["hostname"] + ":" + str(self["port"])
				returnValue["errorcode"] = 1
				syslog.syslog(syslog.LOG_WARNING, returnValue["error"])
				return returnValue

			lines = data.split("\n")

			if len(lines) > 4:

				for line in lines[1:-3]:

					data = {}
					items = line.split()

					if "Zap" in items[0]:
						zap += 1

					elif "SIP" in items[0]:
						sip += 1

					elif "IAX2" in items[0]:
						iax2 += 1

					data["channel"] = items[0]
					data["location"] = items[1]
					data["state"] = items[2]
					data["application_data"] = items[3]

					returnValue["channels"].append(data)

				returnValue["active_channels"] = lines[-3].split(" ")[0].strip()
				returnValue["active_calls"] = lines[-2].split(" ")[0].strip()
				returnValue["calls_processed"] = lines[-1].split(" ")[0].strip()

			else:
				returnValue["active_channels"] = 0
				returnValue["active_calls"] = 0
				returnValue["calls_processed"] = 0

			returnValue["zap"] = zap
			returnValue["sip"] = sip
			returnValue["iax2"] = iax2

		except:
			returnValue = {}
			returnValue["error"] = "Unable to run command 'core show channels' on ami://" + self["hostname"] + ":" + str(self["port"])
			returnValue["errorcode"] = 1
			syslog.syslog(syslog.LOG_WARNING, returnValue["error"])
			return returnValue

		return returnValue

	def getSIPPeers(self):

		returnValue = {}
		returnValue["peers"] = []

		try:
			self.sendCommand('sip show peers')
			data = self.getSocketData()
			lines = data.split("\n")

			if len(lines) > 2:

				for line in lines[1:-1]:

					data = {}
					items = line.split()

					data["name"] = items[0]
					data["host"] = items[1]
					data["dynamic"] = items[2]
					data["nat"] = ""

					if items[-3] == "Y":
						data["nat"] = items[3]

#					data["acl"] = items[3]
					data["port"] = items[-2]
					data["status"] = items[-1]

					returnValue["peers"].append(data)

				items = lines[-1].split()
				returnValue["total_sip_peers"] = items[0]
				returnValue["monitored_online_sip_peers"] = items[4]
				returnValue["monitored_offline_sip_peers"] = items[6]
				returnValue["unmonitored_online_sip_peers"] = items[9]
				returnValue["unmonitored_offline_sip_peers"] = items[11]

			else:
				returnValue["total_sip_peers"] = 0
				returnValue["monitored_online_sip_peers"] = 0
				returnValue["monitored_offline_sip_peers"] = 0
				returnValue["unmonitored_online_sip_peers"] = 0
				returnValue["unmonitored_offline_sip_peers"] = 0

		except:
			returnValue = {}
			returnValue["error"] = "Unable to connect to ami://" + self["hostname"] + ":" + str(self["port"])
			returnValue["errorcode"] = 1
			syslog.syslog(syslog.LOG_WARNING, returnValue["error"])
			return returnValue

		return returnValue

	def getSIPChannels(self):

		returnValue = {}
		returnValue["peers"] = []

		try:
			self.sendCommand('sip show channels')
			data = self.getSocketData()
			lines = data.split("\n")

			if len(lines) > 2:

				for line in lines[1:-1]:

					data = {}
					items = line.split()

					data["peer"] = items[0]
					data["user"] = items[1]
					data["call_id"] = items[2]
					data["format"] = items[3] + " " + items[4]
					data["hold"] = items[5]
					data["last_message"] = items[6] + " " + items[7]

					returnValue["peers"].append(data)

				items = lines[-1].split()
				returnValue["active_sip_peers"] = items[0]

			else:
				returnValue["active_sip_peers"] = 0

		except:
			returnValue = {}
			returnValue["error"] = "Unable to connect to ami://" + self["hostname"] + ":" + str(self["port"])
			returnValue["errorcode"] = 1
			syslog.syslog(syslog.LOG_WARNING, returnValue["error"])
			return returnValue

		return returnValue

	def getMeetme(self):

		returnValue = {}

		try:

			commandText = self.getCommandOutput('meetme')
			self.socket.send(commandText)
			lines = self.socket.recv(self.buffer)

			if len(lines) > 2:

				for line in lines[1:-2]:

					data = {}
					items = line.split()

					data["conf_number"] = items[0]
					data["parties"] = items[1]
					data["marked"] = items[2]
					data["activity"] = items[3]
					data["creation"] = items[4]

					returnValue["users"].append(data)

				items = lines[-1].split()
				returnValue["meetme_users"] = items[6]

			else:
				returnValue["meetme_users"] = 0

		except socket.timeout:
			returnValue = {}
			returnValue["error"] = "Timeout when attempting to connect to ami://" + self["hostname"] + ":" + str(self["port"])
			returnValue["errorcode"] = 1
			syslog.syslog(syslog.LOG_WARNING, returnValue["error"])
			return returnValue

		except:
			returnValue = {}
			returnValue["error"] = "Unable to connect to ami://" + self["hostname"] + ":" + str(self["port"])
			returnValue["errorcode"] = 1
			syslog.syslog(syslog.LOG_WARNING, returnValue["error"])
			return returnValue

		return returnValue

	def getVoicemailUsers(self):

		returnValue = {}

		try:

			commandText = self.getCommandOutput('show voicemail users')
			self.socket.send(commandText)
			lines = self.getSocketData()

			if len(lines) > 2:

				numItems = len(items)

				for line in lines[1:-2]:

					data = {}
					items = line.split()

					data["context"] = items[0]
					data["mbox"] = items[1]
					data["user"] = items[2:numItems-4]
					data["newmsg"] = items[numItems-1]

					returnValue["users"].append(data)

			else:
				returnValue["users"] = {}

		except socket.timeout:
			returnValue = {}
			returnValue["error"] = "Timeout when attempting to connect to ami://" + self["hostname"] + ":" + str(self["port"])
			returnValue["errorcode"] = 1
			syslog.syslog(syslog.LOG_WARNING, returnValue["error"])
			return returnValue

		except:
			returnValue = {}
			returnValue["error"] = "Unable to connect to ami://" + self["hostname"] + ":" + str(self["port"])
			returnValue["errorcode"] = 1
			syslog.syslog(syslog.LOG_WARNING, returnValue["error"])
			return returnValue

		return returnValue

	def getLoginText(self):

		returnValue = ['Action: login']
		returnValue.append('Username: '+self["username"]);
		returnValue.append('Secret: '+self["password"]);
		returnValue.append('Events: off')
		returnValue.append('')
		returnValue.append('')

		return '\n'.join(returnValue)


	def sendCommand(self, command):

		returnValue = ['Action: command']
		returnValue.append('Command: '+command)
		returnValue.append('')
		returnValue.append('')

		commandText = '\n'.join(returnValue)
		self.socket.send(commandText)


	def getSocketData(self):

		data = ''
		
		while True:
 
			chunk = self.socket.recv(self.buffer)
			data = data + chunk
 
			if data[len(data)-4:] == "\r\n\r\n":
				break

		data = data[39:-19].strip()
		return data
