#!/bin/env python
#-*- coding:utf-8 -*-

import pymongo
import os
import time

def connectMongoDB():
	client=pymongo.MongoClient("localhost",27017)
	db=client.opalus
	return db

script_path=os.path.abspath(".")
link_count=connectMongoDB().url_list.count({"mark":"details"})//1000
#link_count=10
for i in range(link_count+1):
	connectMongoDB().url_list.save({"_id":"spider001","mark":3,"name":" ","count":i*1000})
	time.sleep(1)
	os.system("sh"+" "+script_path+"/startspider.sh")
	time.sleep(2)
	

