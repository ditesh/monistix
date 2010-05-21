"""PostgreSQL plugin provides PostgreSQL server instrumentation data"""

__author__ = "Ditesh Shashikant Gathani"
__copyright__ = "Copyright (C) 2010 Ditesh Shashikant Gathani"
__license__ = "GPL"
__version__ = "0.1"
__email__ = "ditesh@gathani.org"

import os
import sys
import syslog
import subprocess
from base import *

class PostgreSQLPlugin(BasePlugin):

	def __init__(self, config):

		self.config = config

		self["port"] = None
		self["username"] = None
		self["password"] = None
		self["hostname"] = "127.0.0.1"
		self["psqlPath"] = "/usr/bin/psql"

		self.configure(["hostname", "port", "username", "password", "psql_path"])

		if not os.path.exists(self["psqlPath"]):
			raise IOError

	def getData(self):

		data = {}
		returnValue = {}

		args = [self["psqlPath"]]
		args.append("-h")
		args.append(self["hostname"])

		if self["username"] != None:
			args.append("-U")
			args.append(self["username"])

		if self["password"] != None:
			args.append("-P" + self.password)

		if self["port"] != None:
			args.append("-p")
			args.append(self["port"])

		args.append("-d")
		args.append("template1")

		args.append("-q")
		args.append("-t")

		# liberally stolen from munin postgresql plugin (great software)
		args.append("-c")
		connections = self.getMetaValue(args, "SELECT tmp.state,COALESCE(count,0) FROM (VALUES ('active'),('waiting'),('idle'),('idletransaction'),('unknown')) AS tmp(state) LEFT JOIN (SELECT CASE WHEN waiting THEN 'waiting' WHEN current_query='<IDLE>' THEN 'idle' WHEN current_query='<IDLE> in transaction' THEN 'idletransaction' WHEN current_query='<insufficient privilege>' THEN 'unknown' ELSE 'active' END AS state, count(*) AS count FROM pg_stat_activity WHERE procpid != pg_backend_pid() GROUP BY CASE WHEN waiting THEN 'waiting' WHEN current_query='<IDLE>' THEN 'idle' WHEN current_query='<IDLE> in transaction' THEN 'idletransaction' WHEN current_query='<insufficient privilege>' THEN 'unknown' ELSE 'active' END) AS tmp2 ON tmp.state=tmp2.state ORDER BY 1")

		if "error" in connections:
			return connections

		users = self.getMetaValue(args, "SELECT usename,count(*) FROM pg_stat_activity WHERE procpid != pg_backend_pid() GROUP BY usename ORDER BY 1")

		if "error" in users:
			return users 

		locks = self.getMetaValue(args, "SELECT lower(mode),count(*) FROM pg_locks WHERE database IS NOT NULL GROUP BY lower(mode) ORDER BY 1")

		if "error" in locks:
			return locks

		cache = self.getMetaValue(args, "SELECT sum(blks_read) AS blks_read,sum(blks_hit) AS blks_hit FROM pg_stat_database")

		if "error" in cache:
			return cache 

		checkpoints = self.getMetaValue(args, "SELECT checkpoints_timed,checkpoints_req FROM pg_stat_bgwriter")

		if "error" in checkpoints:
			return checkpoints

		queryLength = self.getMetaValue(args, "SELECT 'query',COALESCE(max(extract(epoch FROM CURRENT_TIMESTAMP-query_start)),0) FROM pg_stat_activity WHERE current_query NOT LIKE '<IDLE%' UNION ALL SELECT 'transaction',COALESCE(max(extract(epoch FROM CURRENT_TIMESTAMP-xact_start)),0) FROM pg_stat_activity")

		if "error" in queryLength:
			return queryLength 

		scans = self.getMetaValue(args, "SELECT COALESCE(sum(seq_scan),0) AS sequential, COALESCE(sum(idx_scan),0) AS index FROM pg_stat_user_tables")

		if "error" in scans:
			return scans

		size = self.getMetaValue(args, "SELECT datname,pg_database_size(oid) FROM pg_database order by 1")

		if "error" in size:
			return size

		transactions = self.getMetaValue(args, "SELECT 'commit',sum(pg_stat_get_db_xact_commit(oid)) FROM pg_database UNION ALL SELECT 'rollback',sum(pg_stat_get_db_xact_rollback(oid)) FROM pg_database")

		if "error" in transactions:
			return transactions

		returnValue["users "] = users
		returnValue["locks"] = locks
		returnValue["cache"] = cache
		returnValue["connections"] = connections
		returnValue["checkpoints"] = checkpoints
		returnValue["query_length"] = queryLength
		returnValue["scans"] = scans
		returnValue["size"] = size
		returnValue["transactions"] = transactions

		return returnValue


	def getMetaValue(self, args, sql):

		data = {}
		args.append(sql)

		values = subprocess.Popen(args, stdout=subprocess.PIPE, stderr=subprocess.PIPE).communicate()
		args.pop()

		if "failed" in values[1]:
			returnValue = {}
			returnValue["error"] = "Unable to execute " + self["psqlPath"] + " (possibly unable to authenticate)"
			returnValue["errorcode"] = 1
			syslog.syslog(syslog.LOG_WARNING, returnValue["error"])
			return returnValue

		elif "could not connect to server" in values[1]:
			returnValue = {}
			returnValue["error"] = "Unable to connect to server (is server down or refusing connections?)"
			returnValue["errorcode"] = 1
			syslog.syslog(syslog.LOG_WARNING, returnValue["error"])
			return returnValue


		lines = values[0].split("\n")

		for line in lines[:-2]:
			line = line.split("|")
			data[line[0].strip().lower()] = line[1].strip()

		return data
