#!/bin/env python
#-*- coding:utf-8 -*-
import pymongo
import os
import time

def connectMongoDB():
	client=pymongo.MongoClient("localhost",27017)
	db=client.opalus
	return db

script_path=os.path.abspath(".")		#获取脚本当前路径
for i in connectMongoDB().site.find():
	mark=i['mark']
	connectMongoDB().url_list.save({"_id":"spider001","mark":1,"name":mark})
	time.sleep(1)
	os.system("sh"+" "+script_path+"/startspider.sh")
	time.sleep(2)
	
		
