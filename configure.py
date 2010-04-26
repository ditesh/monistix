# Get configuration information from server
# Author: Ditesh Shashikant Gathani
# License: GPL v3

import sys, traceback, configuration
from string import *
from optparse import OptionParser

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
	sys.exit(1)

if len(options.key) > 0:

	try: 
		configObj.reconfigure(options.key)
		print "Success: Configured successfully. Run this script again to get list of configured services."
		sys.exit(0)

	except IOError:
		print >> sys.stderr, "Error: Unable to connect to server, please ensure network connectivity"
		sys.exit(1)

	except:
		print >> sys.stderr, "Error: Unable to set configuration options, please ensure key is correct."
		sys.exit(1)

	try:
		configObj.read()

	except IOError:
		print >> sys.stderr, "Error: Unable to open configuration file or invalid configuration file. Try reconfiguring."
		sys.exit(1)

else: 

	try: 
		configObj.read()
		configObj.getServices()
		print "Success: got list of configured services, all done!"
		sys.exit(0)

	except:
		print >> sys.stderr, "Error: Invalid configuration file or unable to get list of services. Try reconfiguring."
		sys.exit(1)

