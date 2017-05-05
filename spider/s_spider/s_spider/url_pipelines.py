# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
import time
import pymongo
from s_spider.items import SSpiderItem
from pymongo import *

class SSpiderPipeline(object):
	def process_item(self, item, spider):
		data = dict(item)
		client = pymongo.MongoClient('localhost',27017)
		db = client.opalus
		coll = db.url_list
		coll.save(data)
		time.sleep(1)

		return item


