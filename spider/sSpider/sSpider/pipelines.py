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
			id=self.connectMongoDB().url_list.distinct("_id",{"url":item['url']})
			if id:
				self.connectMongoDB().url_list.update({"_id":id[0]},{"$set":post_item})
				time.sleep(2)
			else:
				self.connectMongoDB().url_list.save(post_item)
				time.sleep(2)
		elif item['url_type_mark']==20:
			id=self.connectMongoDB().url_list.distinct("_id",{"url":item['url']})
			if id:
				self.connectMongoDB().url_list.update({"_id":id[0]},{"$set":post_itema})
				time.sleep(2)
			else:
				self.connectMongoDB().url_list.save(post_item)
				time.sleep(2)
		elif item['url_type_mark']=="content":
			id=self.connectMongoDB().url_list.distinct("_id",{"title":item['title']})
			if id:
				self.connectMongoDB().url_list.update({"_id":id[0]},{"$set":post_item})
				time.sleep(2)
			else:
				self.connectMongoDB().url_list.save(post_item)
				time.sleep(2)
			###
			img_path='/'.join(re.split(r"\/",os.path.abspath(os.path.dirname(inspect.getfile(inspect.currentframe()))))[:-1])+"/images/"
			for i in item['content']:
				if i['type']==2:
					self.downloadImages(i['value'],img_path)
				else:
					pass
			###
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
		img_types=['jpeg','bmp','gif','tiff','png','psd','swf','svg','jpg']
		data=urllib.request.urlopen(url).read()
		image_name=re.split(r"\/",url)[-2]
		img_type="."+re.split(r"wx_fmt=",url)[-1]
		img_type1=re.split(r"\/",url)[-1]
		if "&" in img_type:
			image_type=re.split(r"&",img_type)[0]
		elif "." in img_type1:
			image_type='.'+re.split(r"\.",img_type1)[-1]
		else:
			image_type="."+"jpeg"
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
