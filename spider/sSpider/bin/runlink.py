#!/bin/env python
#-*- coding:utf-8 -*-
#'''该脚本用于启动获取站点详情页url的爬虫'''
import pymongo
import os
import time
import inspect



def connectMongoDB():
	'''链接数据库'''
	client=pymongo.MongoClient("localhost",27017)
	db=client.opalus
	return db


def checkData():
	'''检测子页面url数量'''
	count=connectMongoDB().url_list.count({"url_type_mark":10})
	return count

		
if checkData()>0:
	script_path=os.path.abspath(os.path.dirname(inspect.getfile(inspect.currentframe())))
	for i in connectMongoDB().url_list.distinct('site_mark',{"url_type_mark":10}):
		connectMongoDB().url_list.update({"_id":"spider001"},{"$set":{"start_mark":2,"start_site_mark":i}})
		time.sleep(2)
		os.system("sh"+" "+script_path+"/startspider.sh"+" "+i+" "+"&")
		time.sleep(5)
else:
	pass
