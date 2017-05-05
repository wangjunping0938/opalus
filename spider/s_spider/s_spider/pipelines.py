# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
import time
import os.path
import urllib
import requests
import pymongo
import re



class SSpiderPipeline(object):
	def process_item(self, item, spider):
		postItem = dict(item)
		url = "http://opalus.test.com/api/product/update"
		requests.post("http://opalus.test.com/api/product/update",item)
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


