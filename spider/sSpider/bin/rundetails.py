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


script_path=os.path.abspath(os.path.dirname(inspect.getfile(inspect.currentframe())))
link_count=connectMongoDB().url_list.count({"url_type_mark":20})//1000
for i in range(link_count+1):
	connectMongoDB().url_list.update({"_id":"spider001"},{"$set":{"start_mark":3,"name":"","count":i*1000}})
	time.sleep(2)
	os.system("sh"+" "+script_path+"/startspider.sh details_content"+" "+"&")
	time.sleep(5)
	

