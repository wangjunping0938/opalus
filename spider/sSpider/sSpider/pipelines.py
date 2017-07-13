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
import pymongo
import inspect


class SspiderPipeline(object):
	def process_item(self, item, spider):
		post_item=dict(item)
		item_count=len(post_item)
		if item['url_type_mark']==10:
			self.connectMongoDB().url_list.save(post_item)
			time.sleep(2)
		elif item['url_type_mark']==20:
			self.connectMongoDB().url_list.save(post_item)
			time.sleep(2)
		elif item['url_type_mark']=="content":
			self.connectMongoDB().url_list.save(post_item)
			img_path='/'.join(re.split(r"\/",os.path.abspath(os.path.dirname(inspect.getfile(inspect.currentframe()))))[:-1])+"/images/"
			for i in item['content']:
				if i['type']==2:
					self.downloadImages(i['value'],img_path)
				else:
					pass
			video_path='/'.join(re.split(r"\/",os.path.abspath(os.path.dirname(inspect.getfile(inspect.currentframe()))))[:-1])+"/videos/"
			if "video" in item.keys():
				self.downloadVideos(item['video'],video_path)
			else:
				pass
			time.sleep(2)
		return item
	
	
	def connectMongoDB(self):
		'''链接数据库'''
		client=pymongo.MongoClient("localhost",27017)
		db=client.opalus
		return db


	def downloadImages(self,url,imgpath):
		'''下载图片'''
		data=urllib.request.urlopen(url).read()
		image_name=re.split(r"\/",url)[-2]
		img_type="."+re.split(r"wx_fmt=",url)[-1]
		if "&" in img_type:
			image_type=re.split(r"&",img_type)[0]
		else:
			image_type=img_type
		if os.path.exists(imgpath+image_name+image_type):
			pass
		else:
			with open(imgpath+image_name+image_type,'wb') as fp:
				fp.write(data)
	
	
	def downloadVideos(self,url,videopath):
		'''下载视频'''
		data=urllib.request.urlopen(url).read()
		video_name=re.split(r"=",url)[-1]
		if os.path.exists(videopath+video_name+".mp3"):
			pass
		else:
			with open(videopath+video_name+".mp3",'wb') as fp:
				fp.write(data)
