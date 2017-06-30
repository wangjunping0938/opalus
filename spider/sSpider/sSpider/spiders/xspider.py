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


	#1.初始化url列表及domain列表
	def __init__(self):
		if isinstance(self.getUrlListMark(),int)==True
			for i in self.getDetailsUrl(getUrlListMark)
			self.allowed_domains.append(re.split(r'\/',i)[2])		#self.getMark()返回一个url列表查询范围
			self.start_urls.append(i)
		else:
			self.allowed_domains.append(re,split(r'\/',self.getStartUrl(self.getUrlListMark())[0])[2])
			self.start_urls.append(self.getStartUrl(self.getUrlListMark())[0])

	#2.链接mongoDB数据库方法
	def connnectMongoDB(self):
		pymongo.MongoClient("127.0.0.1",27017)
		db=client.opalus
		return db
	
	#3.调用浏览器方法
	def browser(self):
		js=re.sub(r'\n','',os.popen('which phantomjs').read())
		browser=webdriver.Phantomjs(executable_path=js,service_log_path="/dev/null")
		return browser

	#3.获取mark标记值,该值代表获取url地址数量的范围,也代表从那获取起始地址
	def getUrlListMark(self):
		for i in self.connnectMongoDB().url_list.find({"title":"url地址范围基础值"}):
			mark=i['mark']
		return mark

	#4.获取该url对应的标识,该值代表url属于那个站点,根据该值调用该站点的规则
	def getUrlMark(self):
		if response.url in self.connnectMongoDB().site.distinct('url'):
			mark=self.connnectMongoDB().site.distinct("url",{"url":response.url})
		else
			mark=self.connnectMongoDB().url_list.distinct("url",{"url":response,url})
		return mark

	#4.获取站点主页url方法,该url是站点的起始地址
	def getStartUrl(self,mark):		#mark由getMark函数获取,代表url的列表范围
		url=[]
		for i in self.connnectMongoDB().site.find({"mark":mark},{"url":1,"id":0})
			url.append(i['url']
		return url

	#5.获取详情页url方法,该url是站点的详情页即内容所在的链接地址
	def getDetailsUrl(self,mark):
		url=[]
		for i in self.connnectMongoDB().url_list.find().skip(mark).limit(500):
			url.append(i['url'])
		return url	
			
	#5.获取爬取规则
	def getRule(self,mark):
		rule={}
		for i in self.connnectMongoDB().site.find({"mark":mark},{'code':1,'_id':0}):
			rule_list=i['code']
		for i in re.split(',',rule_list):
			rule[re.split(':',i)[0]]=re.split(':',i)[1]
		return rule		#返回的是一个字典,里面包含关键字对应的规则
	
	
	#.对返回请求对象的解析方法	
    def parse(self, response):
		browser=self.browser()
		browser.get(response.url)
		browser.implicitly_wait(20)
		html=browser.page_source
		item=SspiderItem()
		items=[]
		for i in self.getRule(self.getUrlMark()).keys():		#键从获取的规则字典中获取
			try:
				item[i]=eval(self.getRule()[i])		#键对应的规则返回值
			except SyntaxError:
				exec(self.getRule()[i])
		items.append(item)	
