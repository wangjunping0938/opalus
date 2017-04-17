# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

import time
import os.path
import urllib
import os

class UrlJdzcPipeline(object):
	def process_item(self, item, spider):
		today = time.strftime('%Y%m%d',time.localtime())
		fileName = today + '.txt'
		filePath = os.path.abspath(os.path.join(os.path.dirname(''),os.path.pardir)) + "/"
		File = filePath + fileName
		with open(File,'a') as fp:
			fp.write(item['url_list'] + '\n')
		return item
