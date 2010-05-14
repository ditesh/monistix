#!/bin/env python

import os
import sys
import time

def main(argv=None):

	if argv == None:
		argv = sys.argv

	if len(argv) != 2:
		print >> sys.stderr, "No file specified"
		return 1

	filename = argv[1]

	try:

		for i in range(100):
			fp = open(filename, "a")
			fp.write("this is line " + str(i) + "\n")
			fp.close()
			time.sleep(1)

	except Exception, e:
		print e
		print >> sys.stderr, "Unable to write to " + filename
		return 1

	return 0

if __name__ == "__main__":
	sys.exit(main())
