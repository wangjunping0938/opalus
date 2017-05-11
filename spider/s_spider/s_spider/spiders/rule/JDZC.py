#!/bin/env python
# -*- coding: utf-8 -*-

from scrapy.selector import Selector
import os
import re
import sys
sys.path.append(os.path.abspath('../'))
import phantomJS
import connMongoDB

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#获取二级页面url方法
def urlList(html,url):
	#获取页面列表
	try:
		page_count = Selector(text=html).xpath('//div[@class="pagesbox"]//a/text()').extract()[-2]
		site_from = connMongoDB.connMongo().site.distinct('site_from',{'url':url})[0]
		if page_count:
			url_list = []
			for i in range(1,3):#int(page_count) + 1):
				sub_url = url + '?page=' + str(i)
				if url in connMongoDB.connMongo().url_list.distinct('url',{"site_from":site_from}):
					continue
				else:
					url_list.append(sub_url)
			return url_list
		else:
			pass
	except IndexError as s:
		pass
def urlTitle(url):
	#获取url站点来源名称
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




#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#获取详情页url方法
def urlDetailsList(html,url):
	try:
		UrlList = []
		url_list = Selector(text=html).xpath('//div[@class="i-tits"]//a/@href').extract()
		url_list = set(url_list)
		domain = os.path.split(os.path.split(url)[0])[0]
		for i in url_list:
			i = domain + i
			UrlList.append(i)
		return UrlList
	except IndexError as s:
		pass
	



#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#获取内容的方法
def favoriteCount(html):
	#获取关注人数
	try:
		favorite0 = re.sub(r'[\(\)]','',Selector(text=html).xpath('//p[@class="p-btns"]//a[1]/span/text()').extract()[1])
		favorite1 = re.compile(r'\d+').findall(favorite0)[0]
		if favorite0.endswith("千"):
			favorite_count = int(favorite1 + "000")
			return favorite_count
		elif favorite0.endswith("万"):
			favorite_count = int(favorite1 + "0000")
			return favorite_count
		else:
			favorite_count = int(favorite0)
			return favorite_count
	except IndexError as s:
		pass

#获取点赞人数
def loveCount(html):
	try:
		love0 = re.sub(r'[\(\)]','',Selector(text=html).xpath('//p[@class="p-btns"]//a[2]/span/text()').extract()[1])
		love1 = re.compile(r'\d+').findall(love0)[0]
		if love0.endswith("千"):
			love_count = int(love1 + "000")
			return love_count 	
		elif love0.endswith("万"):
			love_count = int(love1 + "0000")
			return love_count 	
		else:
			love_count = int(love0)
			return love_count 	
	except IndexError as s:
		pass
	
#获取众筹剩余天数
def infoLastTime(html):
	try:
		info_last_time = re.sub(r'\s+','',Selector(text=html).xpath('//p[@class="p-target"]//span[3]/text()').extract()[0])
		return info_last_time
	except IndexError as s:
		pass
	
#站点来源
def siteFrom(url):	
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
	
#销售模式
def siteType(url):
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

#项目名称
def title(html):
	try:
		title = Selector(text=html).xpath('//p[@class="p-title"]/text()').extract()[0]
		return title
	except IndexError as s:
		pass

#简述
def resume(html):
	try:
		resume = re.sub(r'[a-zA-Z0-9\.\/\?\=\&\:\_\%\-]','',Selector(text=html).xpath('//div[@class="tab-share-r"]//li/a/@href').extract()[-2])
		return resume
	except IndexError as s:
		pass

#项目发起人
def brandName(html):
	try:
		brand_name = Selector(text=html).xpath('//div[@class="promoters-name"]//a/@title').extract()[0]
		return brand_name
	except IndexError as s:
		pass

#分类
def categoryTags(html):
	try:
		category_tags = Selector(text=html).xpath('//div[@class="tab-share-l"]//a/text()').extract()[0]
		return category_tags
	except IndexError as s:
		pass

#产品编号
def outNumber(url):
	if url in connMongoDB.connMongo().site.distinct('url'):
		pass
	else:
		try:
			out_number = re.compile(r'\d+').findall(os.path.basename(url))[0]
			return out_number
		except IndexError as s:
			pass

#标签
def tags(html):
	try:
		tags = Selector(text=html).xpath('//div[@class="tab-share-l"]//a/text()').extract()[0]
		return tags
	except IndexError as s:
		pass

#产品封面图
def coverUrl(html):
	try:
		cover_url = "http:" + re.sub(r'\s+','',Selector(text=html).xpath('//div[@class="project-img"]//img/@src').extract()[0])
		return cover_url
	except IndexError as s:
		pass

#产品原封面图
def oCoverUrl(html):
	try:
		o_cover_url = "/data/images/jd/" + re.findall(r'\d+',os.path.basename(re.split("\&",re.split("\=",Selector(text=html).xpath('//div[@class="tab-share-r"]//li/a/@href').extract()[-2],maxsplit=2)[1],maxsplit=2)[0]))[0] + '.' + re.split('\.',os.path.basename(re.sub(r'\s+','',Selector(text=html).xpath('//div[@class="main"]//div[@class="project-img"]//img/@src').extract()[0])))[-1]
		return o_cover_url
	except IndexError as s:
		pass

#售总额
def totalPrice(html):
	try:
		total_price = Selector(text=html).xpath('//p[@class="p-num"]/text()').extract()[0]
		return total_price
	except IndexError as s:
		pass

#支持人数
def supportCount(html):
	try:
		support_count = re.findall(r'\d+',Selector(text=html).xpath('//span[@class="fr"]/text()').extract()[0])[0]
		return support_count
	except IndexError as s:
		pass

#众筹发起人/公司
def infoName(html):
	try:
		info_name = Selector(text=html).xpath('//div[@class="promoters-name"]//a/@title').extract()[0]
		return info_name
	except IndexError as s:
		pass

#众筹标准
def infoDemand(html):
	try:
		m1_s = re.sub(r'\n\s+','',Selector(text=html).xpath('//p[@class="p-target"]//text()').extract()[0])
		m_d = re.sub(r'\n\s+','',Selector(text=html).xpath('//p[@class="p-target"]//span/text()').extract()[0])
		m2_s = re.sub(r'\n\s+','',Selector(text=html).xpath('//p[@class="p-target"]//text()').extract()[2])
		m_m = re.sub(r'\n\s+','',Selector(text=html).xpath('//p[@class="p-target"]//text()').extract()[4]) 
		m3_s = re.sub(r'\n\s+','',Selector(text=html).xpath('//p[@class="p-target"]//text()').extract()[3])
		m4_s = re.split(r'！',re.sub(r'\n\s+','',Selector(text=html).xpath('//p[@class="p-target"]//text()').extract()[5]))[0]
		info_demand = m1_s + m_d + m2_s + m_m + m3_s + m4_s
		return info_demand
	except IndexError as s:
		pass

#众筹发起人/公司地址
def infoAddress(html):
	try:
		info_address = re.sub(r'\xa0','',Selector(text=html).xpath('//div[@class="val"]/text()').extract()[1])
		return info_address
	except IndexError as s:
		pass

#众筹联系电话
def infoContact(html):
	try:
		info_contact = re.sub(r'\xa0','',Selector(text=html).xpath('//div[@class="val"]/text()').extract()[2])
		return info_contact
	except IndexError as s:
		pass

#工作时间
def infoTime(html):
	try:
		info_time = re.sub(r'\xa0','',Selector(text=html).xpath('//div[@class="val"]/text()').extract()[3])
		return info_time
	except IndexError as s:
		pass
	
#众筹进度
def infoRate(html):
	try:
		info_rate = int(re.findall(r'\d+',Selector(text=html).xpath('//span[@class="fl percent"]/text()').extract()[0])[0]) / 100
		return info_rate
	except IndexError as s:
		pass
