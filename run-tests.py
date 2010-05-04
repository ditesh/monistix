#!/usr/bin/env python
"""Test runner"""

import sys
import tests
import traceback

def main(argv=None):

	if argv == None:
		argv = sys.argv

	try:
		modulename = argv[1]

	except IndexError:
		print >> sys.stderr, "No module specified"
		return 1

	try:
		tests = __import__("tests")
		module = getattr(tests, modulename)
		obj = getattr(module, modulename.capitalize() + "ProfileTest")()

	except:
		traceback.print_exc(file=sys.stdout)
		print >> sys.stderr, "Unable to correctly import module (tests/" + modulename + ".py)"
		return 1

	obj.run()

if __name__ == "__main__":
	sys.exit(main())
