#!/bin/env python
#-*- coding:utf-8 -*-

import pymongo
import os
import time

def connectMongoDB():
	client=pymongo.MongoClient("localhost",27017)
	db=client.opalus
	return db

def checkData():
	count=connectMongoDB().url_list.count({"mark":"link"})
	return count
		
if checkData()>0:
	script_path=os.path.abspath(".")
	for i in connectMongoDB().url_list.distinct('name',{"mark":"link"}):
		connectMongoDB().url_list.save({"_id":"spider001","mark":2,"name":i})
		time.sleep(1)
		os.system("sh"+" "+script_path+"/startspider.sh")
		time.sleep(2)
else:
	pass
