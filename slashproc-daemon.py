__author__ = "Ditesh Shashikant Gathani"
__copyright__ = "Copyright (C) 2010 Ditesh Shashikant Gathani"

__revision__ = "$Id$"
__version__ = "0.1"

# Standard Python modules.
import os               # Miscellaneous OS interfaces.
import sys              # System-specific parameters and functions.

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

		except OSError, e:
			raise Exception, "%s [%d]" % (e.strerror, e.errno)

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

	return(0)

if __name__ == "__main__":

	retCode = createDaemon()

	while true:

		
		sleep

	sys.exit(retCode)
