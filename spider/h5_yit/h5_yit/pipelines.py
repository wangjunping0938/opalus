# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

import time
import os
import urllib
import requests
import re
import pymongo
from urllib.parse import quote

class H5YitPipeline(object):
	def process_item(self, item, spider):
		url = "http://opalus.test.com/api/product/update"
		postItem = dict(item)
		requests.post("http://opalus.test.com/api/product/update",item)
		try:
			#img_path = os.path.abspath(os.path.join(os.path.dirname(''),os.path.pardir)) + "/images/"
			cover = item['o_cover_url']
			image =  cover
			if os.path.exists(image):
				pass
			else:
				if item['title']:
					data = urllib.request.urlopen(quote(item['cover_url'],safe='/:?=')).read()
					with open(image,'wb') as f:
						f.write(data)
				else:
					pass
		except KeyError:
			pass
		time.sleep(0.1)	
		return item
