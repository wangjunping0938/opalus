#!/bin/env python
#-*- coding:utf-8 -*-
#'''该脚本用于启动获取站点子页面url的爬虫'''
import pymongo
import os
import time
import inspect



def connectMongoDB():
	'''链接数据库'''
	client=pymongo.MongoClient("localhost",27017)
	db=client.opalus
	return db

	
script_path=os.path.abspath(os.path.dirname(inspect.getfile(inspect.currentframe())))
connectMongoDB().url_list.save({"_id" : "spider001", "start_mark" : None, "start_site_mark" : None, "url_count" : None})
for i in connectMongoDB().site.find():
	mark=i['mark']
	connectMongoDB().url_list.update({"_id":"spider001"},{"$set":{"start_mark":1,"start_site_mark":mark}})
	time.sleep(5)
	os.system("sh"+" "+script_path+"/startspider.sh"+" "+mark+" "+"&")
	time.sleep(10)
	
		
