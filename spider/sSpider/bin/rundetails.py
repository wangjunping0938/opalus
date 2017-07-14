#!/bin/env python
#-*- coding:utf-8 -*-
#'''该脚本用于启动获取url页面内容的爬虫'''
import pymongo
import os
import time
import inspect



def connectMongoDB():
	'''链接数据库'''
	client=pymongo.MongoClient("localhost",27017)
	db=client.opalus
	return db


def getUrlCount():
	count=connectMongoDB().url_list.count({"url_type_mark":20})
	num=int(count//1000)
	return num

script_path=os.path.abspath(os.path.dirname(inspect.getfile(inspect.currentframe())))
link_count=getUrlCount()
connectMongoDB().url_list.save({"_id" : "spider001", "start_mark" : None, "start_site_mark" : None, "url_count" : None})
for i in range(link_count+1):
	connectMongoDB().url_list.update({"_id":"spider001"},{"$set":{"start_mark":3,"start_site_mark":"","url_count":i*1000}})
	time.sleep(5)
	os.system("sh"+" "+script_path+"/startspider.sh details_content"+i+" "+"&")
	time.sleep(10)
	

