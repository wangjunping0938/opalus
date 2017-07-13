#!/bin/bash
script_path=$(cd "$(dirname "$0")";cd ../;pwd)
time_now=$(date "+%Y-%m-%d-%T")
log_name=$1
echo $time_now >> $script_path/log/"$log_name".log
nohup scrapy crawl xspider >> $script_path/log/"$log_name".log 2>&1 &
echo -e "\n\n" >> $script_path/log/"$log_name".log
