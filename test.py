"""Testing management of data monitoring """

__author__ = "Ditesh Shashikant Gathani"
__copyright__ = "Copyright (C) 2010 Ditesh Shashikant Gathani"
__license__ = "GPL"
__version__ = "0.1"
__email__ = "ditesh@gathani.org"

import monitor, sys, traceback

def main(argv=None):

	if argv is None:
		argv = sys.argv

	try:
		md = monitor.Dispatcher()
		md.dispatch()
		md.sync()
		return 0

	except:
		traceback.print_exc(file=sys.stdout)
		return 1

if __name__ == "__main__":
	sys.exit(main())
