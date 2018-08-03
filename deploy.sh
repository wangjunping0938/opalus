#!/bin/bash

### BEGIN SCRIPT INFO
# Description: uwsgi service startup management script.
### END SCRIPT INFO

# 加载python环境
current_path=$(cd $(dirname $0);pwd)
source $current_path/venv/bin/activate
export FLASK_ENV=production

case "$1" in
start)
	pids=`ps aux | grep "uwsgi" | grep -v "grep" | wc -l`
	if [ $pids -gt 4 ];then
		echo "uwsgi is running!"
		exit 0
	else
		uwsgi --ini $current_path/uwsgi.ini --vhost
		echo "Start uwsgi service [OK]"
	fi
;;
stop)
	killall -9 uwsgi
	echo "Stop uwsgi service [OK]"
;;
restart)
	sh $0 stop
	sh $0 start
;;
*)
    echo "Usages: sh uwsgiserver.sh [start|stop|restart]"
;;
esac
