# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
import time
import os.path
import urllib
import requests
import re
import os
import sys


class SspiderPipeline(object):
    def process_item(self, item, spider):
		post_item=dict(item)
		item_count=len(post_item)
		if item_count==4:
			self.connectMongoDB().url_list.save({"url":item['url']},{"$set":{post_item}})
			time.sleep(2)
			return item
		else:
			url="http://www.opalustest.com/api/product/update"
			requests.post(url,item)
			try:
				if item['o_cover_url']:
					for i in item['o_cover_url']:
						if os.path.exists(i)
							pass
						else:
							data=urllib.request.urlopen(item['cover_url'][item['o_cover_url'].index(i)]).read()
							with open(i,'wb') as f:
								fp.write(data)
				else:
					pass
			except KeyError:
				pass
			time.sleep(2)
			return item

	def connectMongoDB(self):
		client=pymongo.MongoClient("localhost",27017)
		db=client.opalus
		return db
