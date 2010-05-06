#!/usr/bin/env python
"""Daemon which collects and subsequently sends or saves monitoring data"""

__author__ = "Ditesh Shashikant Gathani"
__copyright__ = "Copyright (C) 2010 Ditesh Shashikant Gathani"
__license__ = "GPL"
__version__ = "0.1"
__email__ = "ditesh@gathani.org"

import os
import sys
import time
import signal
import syslog
import monitor
import traceback
from optparse import OptionParser

# Basic sanity checks
try:
	md = monitor.Dispatcher()

except IOError:
	print >> sys.stderr, "Configuration path does not exist or insufficient permissions to read/write"
	sys.exit(1)

except:
	traceback.print_exc(file=sys.stdout)
	sys.exit(1)

UMASK = 0
WORKDIR = "/"
MAXFD = 1024

if (hasattr(os, "devnull")):
	REDIRECT_TO = os.devnull

else:
	REDIRECT_TO = "/dev/null"

def createDaemon():

	"""Detach a process from the controlling terminal and run it in the
	   background as a daemon.
	   """

	try:
		pid = os.fork()

	except OSError, e:
		raise Exception, "%s [%d]" % (e.strerror, e.errno)

	if (pid == 0):

		os.setsid()

		try:
			pid = os.fork()

		except OSError:
			raise

		if (pid == 0):
			os.chdir(WORKDIR)
			os.umask(UMASK)

		else:
			os._exit(0)

	else:
		os._exit(0)

	import resource
	maxfd = resource.getrlimit(resource.RLIMIT_NOFILE)[1]

	if (maxfd == resource.RLIM_INFINITY):
		maxfd = MAXFD

		for fd in range(0, maxfd):

			try:
				os.close(fd)

			except OSError:
				pass

			os.open(REDIRECT_TO, os.O_RDWR)

	os.dup2(0, 1)
	os.dup2(0, 2)

	return pid


def handler(signum, frame):
	global pidPath
	os.remove(pidPath)
	syslog.syslog(syslog.LOG_INFO, "SIGHUP caught, shutting down slashproc-daemon ...")
	sys.exit(0)

if __name__ == "__main__":

	syslog.openlog("slashproc")
	pid = os.getpid()

	parser = OptionParser()
	parser.add_option("-p", "--pid-path", dest="pid", default="/tmp",
			  help="Location of the PID file")

        (options, args) = parser.parse_args()
	pidPath = os.path.join(options.pid, "slashproc.pid")

	try:
		fp = open(pidPath, "w")
		fp.write(str(pid))
		fp.close()

	except:
		syslog.syslog(syslog.LOG_ERR, "Cannot create PID file in " + os.path.join(options.pid, "slashproc") + ", exiting ...")
		sys.exit(1)

	createDaemon()
	signal.signal(signal.SIGHUP, handler)

	while True:
		md.dispatch()
		md.sync()
		time.sleep(60)

	sys.exit(0)
