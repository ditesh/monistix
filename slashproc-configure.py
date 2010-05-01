#!/usr/bin/env python
"""Get/reset configuration information from server"""

__author__ = "Ditesh Shashikant Gathani"
__copyright__ = "Copyright (C) 2010 Ditesh Shashikant Gathani"
__license__ = "GPL"
__version__ = "0.1"
__email__ = "ditesh@gathani.org"

import sys, traceback, configuration, httplib
from string import *
from optparse import OptionParser

def main(argv=None):

	if argv is None:
		argv = sys.argv

	# Configuration options
	parser = OptionParser()
	parser.add_option("-r", "--reconfigure", dest="key", metavar="KEY", default="",
			  help="Creates new configuration files (overwrites previous configuration) based on KEY")
	parser.add_option("-s", "--server", dest="server", default="localhost",
			  help="Monitoring server")
	parser.add_option("-c", "--config-path", dest="config", default="/etc/monitor", 
			  help="Path to configuration directory")

	(options, args) = parser.parse_args()

	configPath = options.config;

	try:
		configObj = configuration.MonitorConf(configPath)

	except IOError:
		print >> sys.stderr, "Configuration directory (" + configPath + ") does not exist or insufficient permissions to read/write"
		return 1

	if len(options.key) > 0:

		try: 
			configObj.reconfigure(options.key, options.server)
			print "Success: Configured successfully. Run this script again to get list of configured services."
			return 0

		except httplib.HTTPException:
			print >> sys.stderr, "Error: Unable to connect to server, please ensure network connectivity"
			return 1

		except IOError:
			print >> sys.stderr, "Error: Unable to save configuration data. Please check file permissions"
			return 1

		except SystemExit: pass

		except:
			print >> sys.stderr, "Error: Unable to set configuration options, please ensure key is correct"
			return 1

	else: 

		try: 
			configObj.readClientConfig()
			configObj.getServices()
			print "Success: got list of configured services, all done!"
			return 0

		except httplib.HTTPException:
			print >> sys.stderr, "Error: Unable to connect to server, please ensure network connectivity"
			return 1

		except SystemExit: pass

		except:
			print >> sys.stderr, "Error: Invalid configuration file or unable to get list of services. Try reconfiguring"
			return 1

if __name__ == "__main__":
	sys.exit(main())
