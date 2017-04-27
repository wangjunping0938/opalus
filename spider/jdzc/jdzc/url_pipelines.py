# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

import time
import os.path
import urllib
import pymongo
import requests
import re
from jdzc.items import JdzcItem
from selenium import webdriver
from scrapy.selector import Selector
from pymongo import *
import sys

class JdzcPipeline(object):
	def process_item(self, item, spider):
		data = dict(item)
		client = pymongo.MongoClient('localhost',27017)
		db = client.opalus
		coll = db.url_list
		url = item['url']
		url_list = coll.distinct("url",{"site_from":1})
		if url in url_list:
			pass
		else:
			coll.save(data)
		time.sleep(1)

		return item


