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
		postItem = dict(item)
		url = "http://opalus.taihuoniao.com/api/product/update"
		requests.post("http://opalus.taihuoniao.com/api/product/update",item)
		try:
			image = item['o_cover_url']
			if os.path.exists(image):
				pass
			else:
				data = urllib.request.urlopen(item['cover_url']).read()
				with open(image,'wb') as f:
					f.write(data)
		except KeyError:
			pass
		time.sleep(1)
		return item


