#!/bin/env python
# -*- coding: utf-8 -*-
from scrapy.selector import Selector
import os
import re
import sys
sys.path.append(os.path.abspath('.'))
#引用浏览器
from . import phantomJS
#链接数据库
from . import connMongoDB

def urlList(html,url):
	#获取二级页面url方法
	try:
		site_from = siteFrom(url)
		title = urlTitle(url)	
		UrlList = []
		#获取京东二级页面方法
		if title =='JDZC' :
			page_count = Selector(text=html).xpath('//div[@class="pagesbox"]//a/text()').extract()[-2]
			for i in range(1,3):#int(page_count) + 1):
				i = url + '?page=' + str(i)
				if url in connMongoDB.connMongo().url_list.distinct('url',{"site_from":site_from}):
					continue
				else:
					UrlList.append(i)
		#获取一条二级页面方法
		elif title == 'YTSHG':
			url_list = Selector(text=html).xpath('//a/@href').extract()
			for i in url_list:
				if 'activity' in i:
					i = os.path.split(i)[0] + '/' + re.split('.htm',re.split('activity/',i)[-1])[0] + '.html'
					if not i.startswith('http'):
						pass
					else:
						UrlList.append(i)
				else:
					pass
		else:
			print ('获取二级页面失败')
		UrlList = set(UrlList)
		return UrlList
	except IndexError as s:
		pass



def urlTitle(url):
	#统一获取url站点标识
	if url in connMongoDB.connMongo().site.distinct('url'):
		try:
			title = connMongoDB.connMongo().site.distinct('mark',{'url':url})[0]
			return title
		except IndexError as s:
			pass
	elif url in connMongoDB.connMongo().url_list.distinct('url'):
		try:
			title = connMongoDB.connMongo().url_list.distinct('mark',{'url':url})[0]
			return title
		except IndexError as s:
			pass
	else:
		pass



def urlDetailsList(html,url):
	#获取详情页url方法
	try:
		url_list = Selector(text=html).xpath('//div[@class="i-tits"]//a/@href').extract()
		url_list = set(url_list)
		UrlList = []
		#获取京东详情页url方法
		if url_list:
			for i in url_list:
				domain = os.path.split(os.path.split(url)[0])[0]
				i = domain + i
				#i = os.path.split(url)[0] + '/' + re.split('.html',re.split('project/details/',i)[-1])[0] + '.html'
				UrlList.append(i)
			UrlList = set(UrlList)
			return UrlList	
		#获取一条详情页url方法
		elif not url_list:
			url_list = Selector(text=html).xpath('//a/@href').extract()
			for i in url_list:
				if 'product_id' in i:
					i = re.split('\&',i)[0]
					UrlList.append(i)
				else:
					pass
			UrlList = set(UrlList)
			return UrlList	
		else:
				pass			
	except IndexError as s:
		pass



def siteFrom(url):	
	#统一获取站点来源
	if url in connMongoDB.connMongo().site.distinct('url'):
		for i in connMongoDB.connMongo().site.find({'url':url}):
			site_from = i['site_from']
			return site_from
	elif url in connMongoDB.connMongo().url_list.distinct('url'):
		for i in connMongoDB.connMongo().url_list.find({'url':url}):
			site_from = i['site_from']
			return site_from
	else:
		site_from = ''
		return site_from

def siteType(url):
	#统一获取站点销售模式
	if url in connMongoDB.connMongo().site.distinct('url'):
		for i in connMongoDB.connMongo().site.find({'url':url}):
			site_type = i['site_type']
			return site_type
	elif url in connMongoDB.connMongo().url_list.distinct('url'):
		for i in connMongoDB.connMongo().url_list.find({'url':url}):
			site_type = i['site_type']
			return site_type
	else:
		site_type = ''
		return site_type
