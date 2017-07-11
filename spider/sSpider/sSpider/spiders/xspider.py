# -*- coding: utf-8 -*-
import pymongo
import scrapy
import re
import os
import sys
from urllib.request import unquote
from scrapy.selector import Selector
from selenium import webdriver
from sSpider.items import SspiderItem



class XspiderSpider(scrapy.Spider):
	name = "xspider"
	allowed_domains = []
	start_urls = []
	startmark=""

	def __init__(self):
		"""初始化起始url及domain,由启动标识决定初始化的url及domain
			1:初始地址是站点主页地址
			2:初始地址是站点的子页面地址
			3:初始地址是站点的各详情页地址
		"""
		startmark=self.getStartMark("spider001")		#启动类型标识
		self.startmark=startmark
		mark=self.getStartSiteMark("spider001")			#启动站点标识
		count=self.getUrlCount("spider001")				#启动加载url数量
		if startmark==1:
			self.initStartSiteUrl(mark)
		elif startmark==2:
			self.initStartSecondUrl(mark)
		elif startmark==3:
			self.initStarDetailsUrl(mark)
		else:
			pass
	
	def initStartSiteUrl(self,mark):
		"""初始化地址为站点主页"""
		for i in self.connectMongoDB().site.find({"mark":mark}):
			self.allowed_domains.append(re.split(r"\/",i['url'])[2])
			self.start_urls.append(i['url'])		
	
	def initStartSecondUrl(self,mark):
		"""初始化地址为子页面url"""
		for i in self.connectMongoDB().url_list.find({"name":mark,"mark":20}):
			self.allowed_domains.append(re.split(r"\/",i['url'])[2])
			self.start_urls.append(i['url'])

	def initStartDetailsUrl(self,mark):
		"""初始化地址为详情页url"""
		for i in self.connectMongoDB().url_list.find({"mark":startmark}).skip(count).limit(1000):
			try:
				self.allowed_domains.append(re.split(r"\/",str(i.get("url")))[2])
				self.start_urls.append(str(i.get("url")))
			except IndexError:
				pass

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

	def getStartMark(self,ID):
		'''获取启动标识,该标识决定启动的爬虫类型:类似"1","2","3"'''
		for i in self.connectMongoDB().url_list.find({"_id":ID}):
			mark=i['mark']
		return mark

	def getStartSiteMark(self,ID):
		'''获取启动站点标识,该标识决定启动的爬虫的站点:类似"somesite"'''
		for i in self.connectMongoDB().url_list.find({"_id":ID}):
			mark=i['name']
		return mark

	def getUrlSiteMark(self,url):
		"""获取url所在站点标识,该标识决定当前url所在站点:类似'somesite'"""
		sitemark=self.connectMongoDB().site.distinct("mark",{"url":url})
		urllistmark=self.connectMongoDB().url_list.distinct("name",{"url":url})
		if sitemark:
			return sitemark[0]
		else:
			return urllistmark[0]

	def getUrlCount(self,ID):
		"""获取url地址数量范围的值,该值决定了爬虫启动时获取的url数量:类似'1~1000'"""
		for i in self.connectMongoDB().url_list.find({"_id":ID}):
			count=i["count"]
		return count

	def getSiteRule(self,mark):
		"""根据当前url所属站点标识获取站点规则,该规则对应当前url所属的站点"""
		rule={}
		rule_path=os.path.abspath("../../rule/")+"/"
		for i in open(rule_path+mark+".rule"):
			rule[re.split(r":::",i)[0]]=re.split(r":::",i)[1]
		return rule

	def getSecondUrl(self,mark):
		"""获取子页面url方法"""
		try:
			url=eval(rule['url'])
			item=SspiderItem()
			item['url']=url
			item['mark']=2 
			item['name']=mark
			item['fingerprint']="0"
			items.append(item)
			return items
		except SyntaxError:	
			pass
		except IndexError:
			pass

	def getDetailsUrl(self,rule,mark):
		"""获取详情页url方法"""
		try:
			url=[]
			exec(rule['link'].replace("\\n","\n").replace("\\t","\t").replace("\\\'","\'"))
			for i in url:
				item=SspiderItem()
				item['url']=i
				item['mark']=3
				item['name']=mark
				item['fingerprint']="0"
				items.append(item)
			return items
		except IndexError:
			pass
	
	def getContent(self,rule,mark):
		"""3:标识为返回的详情页的内容"""
		try:
			ydqw=eval(rule['ydqw'])			#判断如果有阅读全文,则重新加载url页面源码"""
			if ydqw:
				browser.get(ydqw)
				browser.implicitly_wait(20)
				html=browser.page_source
			else:
				pass
		except IndexError:
			pass
		item=SspiderItem()
		for i in rule.keys():
			try:
				item[i]=eval(rule[i])
			except IndexError:
				pass
			except SyntaxError:
				locals()[i]=[]
				exec(rule[i].replace("\\n","\n").replace("\\t","\t").replace("\\\'","\'"))
				item[i]=i
		items.append(item)
		return items
			

	def parse(self, response):
		browser=self.browser()
		browser.get(response.url)		#调用浏览器加载url	
		browser.implicitly_wait(20)		#等待js加载时长
		html=browser.page_source		#获取url页面源码
		items=[]
		mark=self.getUrlSiteMark(unquote(response.url))
		rule=self.getSiteRule(mark)
		if self.startmark==1:
			self.getSecondUrl(mark)
		elif self.startmark==2:
			self.getDetailsUrl(rule,mark)
		elif self.startmark==3:
			self.getContent(rule,mark)
		else:
			pass
