#!/bin/bash
num=0
#while (( $num < 1 ))
#do
#	echo "hello"
#	sleep 1
#done	
#url=$(ps -A -o stat,pid,cmd |grep "url_spider" |grep -v grep |awk '{print $2}')
num=""
echo "test start"
while [ 1 -eq 1 ]
do
	t_num="a"
	if [ ! -n "$t_num" ];then
		echo "为空"
		sleep 2
		break
	else
		echo "不为空"
		sleep 2
		continue
	fi
done

echo "test success"
exit 2
