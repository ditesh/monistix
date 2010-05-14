#!/bin/env python

import os
import sys
import time

class SomeTail:

	def __init__(self, filename):
		self.position = 0
		self.filename = filename

	def tail(self):

		if not os.path.exists(self.filename):
			print >> sys.stderr, "File specified does not exist"
			return 1

		try:
			filesize = os.path.getsize(self.filename)

			if (filesize < self.position):
				self.position= 0

			fp = open(self.filename, "r")
			fp.seek(self.position)

			while True:

				line = fp.readline()
				self.position = fp.tell()

				if line == "":
					break

				else:
					print line

			fp.close()

		except Exception, e:
			print e
			return 1

		return 0

if __name__ == "__main__":

	tail = SomeTail(sys.argv[1])

	while True:
		tail.tail()
		print "Going to sleep for a bit ..."
		time.sleep(10)

