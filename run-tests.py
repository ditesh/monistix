#!/usr/bin/env python
"""Test runner"""

import os
import sys
import json
import tests
import syslog
import traceback
import libs.config as config
from configobj import ConfigObj
from optparse import OptionParser

syslog.openlog("slashproc")

def main(argv=None):

	if argv == None:
		argv = sys.argv

	parser = OptionParser()
	parser.add_option("-H", "--hostname", dest="hostname", default="localhost", help="Hostname")
	parser.add_option("-p", "--plugin", dest="plugin", default="all", help="Test specified plugin")
	parser.add_option("-c", "--config", dest="config", default="/etc/monistix", help="Path to configuration dir to test configuration settings")
	parser.add_option("-f", "--failures", dest="failures", action="store_true", default=False, help="Only show failures (useful for debugging)")

	(options, args) = parser.parse_args()
	plugin = options.plugin
	hostname = options.hostname
	configPath = options.config
	failuresOnly = options.failures

	if len(hostname) == 0:
		print >> sys.stderr, "No hostname specified"
		return(1)

	if len(plugin) == 0 and len(config) == 0:
		print >> sys.stderr, "No plugin or configuration file specified"
		return(1)

	if len(configPath) > 0 and not os.path.exists(configPath):
		print >> sys.stderr, "No such configuration path exists: " + configPath
		return(1)

	try:
		configuration = config.MonitorConf(configPath)
		configuration.readServicesConfig()
		configuration.readClientConfig()

	except:
		raise

	successes = 0
	failures = 0

	if plugin == "config":
		classname = "ConfigTest"

	elif plugin == "all":

		import plugins

		pluginList = dir(plugins)

		for plugin in pluginList:

			# Skipping abstract plugin
			if plugin == "base":
				continue

			if "_" not in plugin:
				returnValue = runPlugin(configuration, hostname, plugin, None, failuresOnly)

				if returnValue == 0:
					successes += 1
				else:
					failures += 1
		
		return(printResult(successes, failures))

	else:
		classname = None

	returnValue = runPlugin(configuration, hostname, plugin, classname, failuresOnly)

	if returnValue == 0:
		successes += 1
	else:
		failures += 1

	return(printResult(successes, failures))

def printResult(successes, failures):

	print >> sys.stdout
	print >> sys.stdout, "Summary:"
	print >> sys.stdout, "Total plugins: " + str(successes + failures)
	print >> sys.stdout, "Successes: " + str(successes)
	print >> sys.stdout, "Failures: " + str(failures)
	print >> sys.stdout

	if failures > 0:
		return(1)

	return(0)


def runPlugin(configuration, hostname, plugin, classname=None, failuresOnly=False):

	configValues = []

	if plugin in configuration.services[hostname]:
		configValues = configuration.services[hostname][plugin]

	else:
		print >> sys.stderr
		print >> sys.stderr, "Plugin " + plugin + ": incorrect or missing configuration"
		return(1)

	if "enabled" not in configuration.services[hostname][plugin] or configuration.services[hostname][plugin]["enabled"]!= '1':
		print >> sys.stderr
		print >> sys.stderr, "Plugin " + plugin + ": not enabled in configuration file"
		return(1)

	if classname == None:
		classname = plugin.capitalize() + "PluginTest"

	try:
		del configValues["enabled"]
		configValues["hostname"] = hostname
		tests = __import__("tests")
		obj = getattr(getattr(tests, plugin), classname)(configValues)

	except:
		print >> sys.stderr
		print >> sys.stderr, "Plugin " + plugin + ": unable to correctly import tests/" + plugin + ".py"
		return(1)

	try:

		if not failuresOnly:
			print >> sys.stdout
			print >> sys.stdout, "Running plugin " + plugin

		data = obj.run()

		if not failuresOnly:
			print json.dumps(data, indent=4)

		return(0)

	except  IOError:
		print >> sys.stderr
		print >> sys.stderr, "Plugin " + plugin + ": unable to correctly run tests/" + plugin + ".py (misconfiguration is a common reason)"
		return(1)


if __name__ == "__main__":
	sys.exit(main())
