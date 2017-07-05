# -*- coding: utf-8 -*-
import pymongo
import scrapy
import re
import os
import sys
from scrapy.selector import Selector
from selenium import webdriver
from sSpider.items import SspiderItem



class XspiderSpider(scrapy.Spider):
	name = "xspider"
	allowed_domains = []
	start_urls = []


	def __init__(self):
		'''初始化url列表及domain列表'''
		if self.getMark()==1:
			"""1代表获取主站点url地址"""
			for i in self.connectMongoDB.site.find({"mark":self.getSiteName()}):
				self.allowed_domains.append(re.split(r'\/',i['url'])[2])		
				self.start_urls.append(i['url'])
		elif self.getMark()==2:
			"""2代表从主站点开始爬取详情页链接"""
			for i in self.connectMongoDB.url_list.find({"mark":self.getSiteName()}):
				self.allowed_domains.append(re.split(r'\/',i['url'])[2])
				self.start_urls.append(i['url'])
		else:
			"""如果是3或者其他非1，2的数字则代表开始爬取详情页内容"""
			for i in self.connectMongoDB.url_list.find().skip(self.getCount()).limit(1000):
				self.allowed_domains.append(re.split(r'\/',i['url'])[2])
				self.start_urls.append(i['url'])

	def connectMongoDB(self):
		'''链接mongoDB数据库方法'''
		client=pymongo.MongoClient("localhost",27017)
		db=client.opalus
		return db
	
	def browser(self):
		'''调用浏览器phantomjs方法'''
		js=re.sub(r"\n","",os.popen("which phantomjs").read())
		browser=webdriver.PhantomJS(executable_path=js,service_log_path="/dev/null")
		return browser

	def getMark(self):
		'''获取mark标识,用于爬取链接和爬取内容的爬虫启动'''
		for i in self.connectMongoDB().url_list.find({"_id":"spider001"}):
			mark=i['mark']
		return mark

	def getSiteName(self):
		'''获取站点标识名称'''
		for i in self.connectMongoDB().url_list.find({"_id":"spider001"}):
			site_name=i['name']
		return site_name
	
	def getCount(self):
		"""获取url列表的分片范围"""
		for i in self.connectMongoDB().url_list.find({"_id":"spider001"}):
			count=i['count']
		return count

	def getSiteUrl(self,url):
		"""获取当前请求的url的站点标识"""
		for i in self.connectMongoDB().url_list.find({"url":url}):
			mark=i['name']
		return mark

	def getRule(self,mark):
		'''根据url所属站点获取该站点的规则'''
		rule={}
		for i in self.connectMongoDB().site.find({"mark":self.getSiteUrl(response.url)}):
			rule_list=i['code']
		for i in re.split(',',rule_list):
			rule[re.split(":",i)[0]]=re.split(":",i)[1]
		return rule
			
	def parse(self, response):
		'''对返回请求对象的解析方法'''
		browser=self.browser()
		browser.get(response.url)		#浏览器请求链接
		browser.implicitly_wait(20)		#JS加载等待时间
		html=browser.page_source		#获取源码
		item=SspiderItem()		#生成字典(字典的键由items.py文件定义)
		items=[]
		for i in self.getRule(self.getDetailsMark()).keys():		#从字典中提取规则
			try:
				item[i]=eval(self.getRule()[i])		#执行字典中的规则并获取数据
			except SyntaxError:		
				exec(self.getRule()[i])
		items.append(item)	
