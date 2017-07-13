# -*- coding: utf-8 -*-
import pymongo
import scrapy
import re
import os
import sys
import inspect
from urllib.request import unquote
from scrapy.selector import Selector
from selenium import webdriver
from sSpider.items import SspiderItem



class XspiderSpider(scrapy.Spider):
	name="xspider"
	allowed_domains=[]
	start_urls=[]
	start_mark=""
	print("@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@")
	print(allowed_domains)
	print(start_urls)
	print(start_mark)
	print("@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@")

	#0.###
	def __init__(self):
		start_mark=self.getStartMark("spider001")
		self.start_mark=start_mark		#启动类型标识
		start_site_mark=self.getStartSiteMark("spider001")		#启动站点标识
		url_count=self.getUrlCount("spider001")		#url数量
		if start_mark==1:
			self.allowed_domains=self.addSiteUrls1(start_site_mark)[0]
			self.start_urls=self.addSiteUrls1(start_site_mark)[1]
		elif start_mark==2:
			self.allowed_domains=self.addSiteUrls2(start_site_mark)[0]
			self.start_urls=self.addSiteUrls2(start_site_mark)[1]
		elif start_mark==3:
			self.allowed_domains=self.addSiteUrls3(url_count,1000)[0]
			self.start_urls=self.addSiteUrls3(url_count,1000)[1]
		else:
			pass


	#1.###
	def	addSiteUrls1(self,mark):
		'''添加站点主页url'''
		domains=[]
		urls=[]
		data=self.connectMongoDB().site.find({"mark":mark})
		for i in data:
			dom=re.split(r"\/",i['url'])[2]
			url=i['url']
			urls.append(url)
			if dom in domains:
				pass
			else:
				domains.append(dom)
		return domains,urls


	#2.###
	def addSiteUrls2(self,mark):
		'''添加子页面url'''
		domains=[]
		urls=[]
		data=self.connectMongoDB().url_list.find({"site_mark":mark,"url_type_mark":10})
		for i in data:
			dom=re.split(r"\/",i['url'])[2]
			url=i['url']
			urls.append(url)
			if dom in domains:
				pass
			else:
				domains.append(dom)
		return domains,urls


	#3.###
	def addSiteUrls3(self,count,limit):
		'''添加详情页url'''
		domains=[]
		urls=[]
		data=self.connectMongoDB().url_list.find({"url_type_mark":20}).skip(count).limit(limit)
		for i in data:
			try:
				dom=re.split(r"\/",str(i.get("url")))[2]
				url=str(i.get("url"))
				urls.append(url)
				if dom in domains:
					pass
				else:
					domains.append(dom)
			except IndexError:
				pass
		return domains,urls


	#4.###
	def connectMongoDB(self):
		'''链接mongoDB opalus库'''
		client=pymongo.MongoClient("localhost",27017)
		db=client.opalus
		return db


	#5.###
	def browser(self):
		'''调用浏览器'''
		js=re.sub(r"\n","",os.popen("which phantomjs").read())
		log_path="/dev/null"
		browser=webdriver.PhantomJS(executable_path=js,service_log_path=log_path)
		return browser


	#6.###
	def getStartMark(self,ID):
		'''获取启动类型标识'''
		start_mark=self.connectMongoDB().url_list.distinct("start_mark",{"_id":ID})
		return int(start_mark[0])


	#7.###
	def getStartSiteMark(self,ID):
		'''获取启动站点标识'''
		start_site_mark=self.connectMongoDB().url_list.distinct("start_site_mark",{"_id":ID})
		return start_site_mark[0]


	#8.###
	def getUrlSiteMark(self,url):
		'''获取当前请求url所属站点标识'''
		if self.start_mark==1:
			try:
				for i in self.connectMongoDB().site.find({"url":url}):
					mark=i['mark']
				return mark
			except UnboundLocalError:
				pass
		elif self.start_mark==2: 
			try:
				for i in self.connectMongoDB().url_list.find({"url":url,"url_type_mark":10}):
					mark=i['site_mark']
				return mark
			except UnboundLocalError:
				pass
		elif self.start_mark==3:
			try:
				for i in self.connectMongoDB().url_list.find({"url":url,"url_type_mark":20}):
					mark=i['site_mark']
				return mark
			except UnboundLocalError:
				pass
		else:
			pass


	#9.###
	def getUrlCount(self,ID):
		'''获取url数量,该数量决定起始地址列表url数量'''
		try:
			for i in self.connectMongoDB().url_list.find({"_id":ID}):
				count=i['url_count']
			return int(count)
		except UnboundLocalError:
			pass


	#10.###
	def getUrlSiteRule(self,mark):
		'''根据当前请求url获取该url所在站点规则'''
		rule={}
		path='/'.join(re.split(r'\/',os.path.abspath(os.path.dirname(inspect.getfile(inspect.currentframe()))))[:-2])+'/rule/'
		for i in open(path+mark+".rule"):
			rule[re.split(r":::",i)[0]]=re.split(r":::",i)[1][:-1]
		return rule

	#11.###
	def getSubPageUrls(self,html,items,mark,rule):
		'''获取子页面url'''
		url=eval(rule['url'])
		item=SspiderItem()
		item['url']=url
		item['site_mark']=mark
		item['url_type_mark']=10
		item['fingerprint']=0
		items.append(item)
		return items
		
	#12.###
	def getDetailsUrlList(self,html,rule,response):
		'''获取详情页url列表'''
		try:
			exec(rule['link'].replace("\\n","\n").replace("\\t","\t").replace("\\\'","\'"))
			url=locals()['link']
			return url
		except IndexError:
			pass
		
	#13.###
	def getDetailsUrls(self,html,items,mark,rule,response):
		'''获取详情页url'''
		urls=self.getDetailsUrlList(html,rule,response)
		for i in urls:
			item=SspiderItem()
			item['url']=i
			item['url_type_mark']=20
			item['site_mark']=mark
			item['fingerprint']=0
			items.append(item)
		return items


	def getDetailsHtml(self,html,rule,browser):
		'''当详情页内容不全是重新加载页面'''
		try:
			read_full_text=eval(rule["read_full_text"])
			if read_full_text:
				browser.get(read_full_text)
				browser.implicitly_wait(20)
				html=browser.page_source
				return html
			else:
				pass
		except IndexError:
			pass


	def getDetailsContent(self,html,items,rule,browser,response):
		new_html=self.getDetailsHtml(html,rule,browser)
		if new_html:
			html=new_html
		else:
			pass
		item=SspiderItem()
		for i in rule.keys():
			try:
				item[i]=eval(rule[i])
			except IndexError:
				pass
			except SyntaxError:
				try:
					exec(rule[i].replace("\\n","\n").replace("\\t","\t").replace("\\\'","\'"))
					item[i]=locals()[i]
				except KeyError:
					pass
		item['url']=response.url
		items.append(item)
		return items
				
			
	def parse(self, response):
		browser=self.browser()
		browser.get(response.url)
		browser.implicitly_wait(20)
		html=browser.page_source
		items=[]
		mark=self.getUrlSiteMark(unquote(response.url))
		rule=self.getUrlSiteRule(mark)
		if self.start_mark==1:
			items=self.getSubPageUrls(html,items,mark,rule)
			return items
		elif self.start_mark==2:
			items=self.getDetailsUrls(html,items,mark,rule,response)
			return items
		elif self.start_mark==3:
			items=self.getDetailsContent(html,items,rule,browser,response)
			return items
		else:
			pass

