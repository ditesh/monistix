#!/usr/bin/env python
"""Test runner"""

import sys
import tests
import config
import ConfigParser
import traceback

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
		configValues = []

	try:
		tests = __import__("tests")
		module = getattr(tests, modulename)
		obj = getattr(module, modulename.capitalize() + "ProfileTest")(configValues)

	except:
		traceback.print_exc(file=sys.stdout)
		print >> sys.stderr, "Unable to correctly import module (tests/" + modulename + ".py)"
		return 1

	try:
		obj.run()

	except IOError:
		print >> sys.stderr, "Unable to correctly run module (tests/" + modulename + ".py), checking configuration"
		return 1


if __name__ == "__main__":
	sys.exit(main())
