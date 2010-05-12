#!/usr/bin/env python
"""Test runner"""

import sys
import json
import tests
import config
import syslog
import traceback
import ConfigParser

syslog.openlog("slashproc")

def main(argv=None):

	if argv == None:
		argv = sys.argv

	try:
		configuration = config.MonitorConf()
		configuration.readServicesConfig()
		configuration.readClientConfig()

	except:
		raise

	try:
		modulename = argv[1]

	except IndexError:
		print >> sys.stderr, "No module specified"
		return 1

	try:
		configValues = configuration.services.items(modulename)

	except ConfigParser.NoSectionError:
		print >> sys.stderr, "Incorrect or missing configuration for profile " + modulename
		return 1

	if configuration.services.get(modulename, "enabled") != '1':
		print >> sys.stderr, "Unable to run test, as module in not enabled in configuration file"
		return 1

	try:
		tests = __import__("tests")
		module = getattr(tests, modulename)
		obj = getattr(module, modulename.capitalize() + "ProfileTest")(configValues)

	except:
		traceback.print_exc(file=sys.stdout)
		print >> sys.stderr, "Unable to correctly import profile (tests/" + modulename + ".py)"
		return 1

	try:
		data = obj.run()
		print json.dumps(data, indent=4)

	except  IOError:
		print >> sys.stderr, "Unable to correctly run module (tests/" + modulename + ".py), check configuration"
		return 1


if __name__ == "__main__":
	sys.exit(main())
