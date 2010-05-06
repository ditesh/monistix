#!/bin/sh

if [ "z${1}" = "zstart" ]; then

	echo -n "Starting slashproc daemon ..."
	python slashproc-daemon.py -p /var/run

	if [ $? -eq 0 ]; then

		echo " OK"

	else

		echo " FAILED (check syslog)"

	fi

elif [ "z${1}" = "zstop" ]; then

	if [ -f "/var/run/slashproc.pid" ]; then

		echo -n "Stopping slashproc daemon with SIGHUP signal ..."
		kill -SIGHUP `cat /var/run/slashproc.pid`
		echo " OK"

	else

		echo "Cannot stop slashproc daemon because its not running"

	fi

elif [ "z${1}" = "zstatus" ]; then

	if [ -f "/var/run/slashproc.pid" ]; then
		echo "slashproc daemon is running"

	else
		echo "slashproc daemon is not running"

	fi

else

	echo "slashproc: an instrumentation tool"
	echo "Copyright GNU GPL (2010) Ditesh Shashikant Gathani (ditesh@gathani.org)"
	echo
	echo "Options:"
	echo "	status: whether slashproc daemon is running"
	echo "	start: start the slashproc daemon"
	echo "	stop: stop the slashproc daemon"
	echo

fi
