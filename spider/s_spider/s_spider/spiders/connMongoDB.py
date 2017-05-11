#!/bin/env python
# -*- coding: utf-8 -*-
import pymongo
import re

def connMongo():
	#链接数据库opalus库
	client = pymongo.MongoClient('localhost',27017)
	db = client.opalus
	return db

def startUrlList():
	#从site表获取起始url地址
	startUrlList = []
	start_url_list = StartUrlList()
	second_url_list = secondUrlList()
	details_url_list = detailsUrlList()
	if second_url_list and details_url_list:
		startUrlList = details_url_list
		return startUrlList
	elif second_url_list and not details_url_list:
		startUrlList = second_url_list
		return startUrlList
	elif not second_url_list and not details_url_list:
		startUrlList = start_url_list
		return startUrlList
	else:
		print ('start_url_list为空,没有起始地址可以添加')
		pass

def StartUrlList():
	#从site表获取起始url列表
	start_url_list = connMongo().site.distinct('url')
	if start_url_list:
		return start_url_list
	else:
		pass

def secondUrlList():
	#从url_list表获取二级页面url列表
	second_url_list = connMongo().url_list.distinct('url',{"title":'second'})
	if second_url_list:
		return second_url_list
	else:
		second_url_list = []
		return second_url_list

def detailsUrlList():
	#从url_list表获取详情页url列表
	details_url_list = connMongo().url_list.distinct('url',{"tags":"details"})
	if details_url_list:
		return details_url_list
	else:
		details_url_list = []
		return details_url_list

def domainList():
	#从site表获取域名列表
	domainList = []
	for i in connMongo().site.find({},{"url":1,"_id":0}):
		domainList.append(re.split(r'\/',i['url'])[2])
	return domainList

