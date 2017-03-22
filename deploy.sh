#!/bin/bash
if [ ! -n "$1" ]
then
    echo "Usages: sh deploy.sh [start|stop|restart]"
    exit 0
fi

# 加载python环境
source env/bin/activate
FLASK_ENV=production

if [ $1 = start ]
then
    psid=`ps aux | grep "uwsgi" | grep -v "grep" | wc -l`
    if [ $psid -gt 4 ]
    then
        echo "uwsgi is running!"
        exit 0
    else
        uwsgi ./uwsgi.ini --no-site --vhost
        echo "Start uwsgi service [OK]"
    fi
    

elif [ $1 = stop ];then
    killall -9 uwsgi
    echo "Stop uwsgi service [OK]"
elif [ $1 = restart ];then
    killall -9 uwsgi
    uwsgi --ini ./uwsgi.ini --no-site --vhost
    echo "Restart uwsgi service [OK]"

else
    echo "Usages: sh uwsgiserver.sh [start|stop|restart]"
fi

