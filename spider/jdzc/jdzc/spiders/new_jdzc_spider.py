# -*- coding: utf-8 -*-
import scrapy
import os
import re
from jdzc.items import JdzcItem
from selenium import webdriver
from scrapy.selector import Selector
import pymongo

class JdzcSpiderSpider(scrapy.Spider):
	name = "new_jdzc_spider"
	allowed_domains = ["z.jd.com"]
	#从数据库获取url地址
	client = pymongo.MongoClient('localhost',27017)
	db = client.opalus
	#新url地址
	coll = db.url_list
	url_list = coll.distinct("url",{"site_from":1})
	#旧url地址
	conn = db.product
	url = conn.distinct("url",{"site_from":1})	
	#判断是否已经爬去并添加起始地址
	start_urls = []
	for i in url_list:
		if i in url:
			pass
		else:
			start_urls.append(i)

	def parse(self, response):
		items = []
		item = JdzcItem()
		#引用浏览器
		js = re.sub(r'\n','',os.popen('which phantomjs').read())
		browser = webdriver.PhantomJS(executable_path = js)    
		browser.get(response.url)
		browser.implicitly_wait(10)
		html = browser.page_source
		#网址
		try:
			item['url'] = response.url 
		except IndexError as s:
			pass
		#关注人数
		try:
			favorite0 = re.sub(r'[\(\)]','',Selector(text=html).xpath('//p[@class="p-btns"]//a[1]/span/text()').extract()[1])
			favorite1 = re.compile(r'\d+').findall(favorite0)[0]
			if favorite0.endswith("千"):
				item['favorite_count'] = favorite1 + "000"
				item['favorite_count'] = int(item['favorite_count'])
			elif favorite0.endswith("万"):
				item['favorite_count'] = favorite1 + "0000"
				item['favorite_count'] = int(item['favorite_count'])
			else:
				item['favorite_count'] = int(favorite0)
		except IndexError as s:
			pass 
		#点赞人数
		try:
			love0 = re.sub(r'[\(\)]','',Selector(text=html).xpath('//p[@class="p-btns"]//a[2]/span/text()').extract()[1])
			love1 = re.compile(r'\d+').findall(love0)[0]
			if love0.endswith("千"):
				item['love_count'] = love1 + "000"
				item['love_count'] = int(item['love_count'])
			elif love0.endswith("万"):
				item['love_count'] = love1 + "0000"
				item['love_count'] = int(item['love_count'])
			else:
				item['love_count'] = int(love0)
		except IndexError as s:
			pass
		#众筹剩余天数
		try:
			item['info_last_time'] = re.sub(r'\s+','',Selector(text=html).xpath('//p[@class="p-target"]//span[3]/text()').extract()[0])
		except IndexError as s:
			pass
		#站点来源		
		item['site_from'] = 1
		#销售模式
		item['site_type'] = 2
		#项目名称
		try:
			item['title'] = Selector(text=html).xpath('//p[@class="p-title"]/text()').extract()[0]
		except IndexError as s:
			pass
		#简述
		try:
			item['resume'] = re.sub(r'[a-zA-Z0-9\.\/\?\=\&\:\_\%\-]','',Selector(text=html).xpath('//div[@class="tab-share-r"]//li/a/@href').extract()[-2])
		except IndexError as s:
			pass
		#项目发起人
		try:
			item['brand_name'] = Selector(text=html).xpath('//div[@class="promoters-name"]//a/@title').extract()[0]
		except IndexError as s:
			pass
		#分类
		try:
			item['category_tags'] = Selector(text=html).xpath('//div[@class="tab-share-l"]//a/text()').extract()[0]
		except IndexError as s:
			pass
		#产品编号
		try:
			item['out_number'] = re.compile(r'\d+').findall(os.path.basename(response.url))[0]
			#re.findall(r'\d+',os.path.basename(re.split("\&",re.split("\=",response.xpath('//div[@class="tab-share-r"]//li/a/@href').extract()[-2],maxsplit=2)[1],maxsplit=2)[0]))[0]
		except IndexError as s:
			pass
		#标签
		try:
			item['tags'] = Selector(text=html).xpath('//div[@class="tab-share-l"]//a/text()').extract()[0]
		except IndexError as s:
			pass
		#产品封面图
		try:
			item['cover_url'] = "http:" + re.sub(r'\s+','',Selector(text=html).xpath('//div[@class="project-img"]//img/@src').extract()[0])
		except IndexError as s:
			pass
		#原产品封面图地址
		try:
			item['o_cover_url'] = "/data/images/jd/" + re.findall(r'\d+',os.path.basename(re.split("\&",re.split("\=",Selector(text=html).xpath('//div[@class="tab-share-r"]//li/a/@href').extract()[-2],maxsplit=2)[1],maxsplit=2)[0]))[0] + '.' + re.split('\.',os.path.basename(re.sub(r'\s+','',Selector(text=html).xpath('//div[@class="main"]//div[@class="project-img"]//img/@src').extract()[0])))[-1]
		except IndexError as s:
			pass
		#销售总额
		try:
			item['total_price'] = Selector(text=html).xpath('//p[@class="p-num"]/text()').extract()[0]
		except IndexError as s:
			pass
		#支持人数
		try:
			item['support_count'] = re.findall(r'\d+',Selector(text=html).xpath('//span[@class="fr"]/text()').extract()[0])[0]
		except IndexError as s:
			pass
		#众筹发起人/公司
		try:
			item['info_name'] = Selector(text=html).xpath('//div[@class="promoters-name"]//a/@title').extract()[0]
		except IndexError as s:
			pass
		#众筹标准
		try:
			m1_s = re.sub(r'\n\s+','',Selector(text=html).xpath('//p[@class="p-target"]//text()').extract()[0])
			m_d = re.sub(r'\n\s+','',Selector(text=html).xpath('//p[@class="p-target"]//span/text()').extract()[0])
			m2_s = re.sub(r'\n\s+','',Selector(text=html).xpath('//p[@class="p-target"]//text()').extract()[2])
			m_m = re.sub(r'\n\s+','',Selector(text=html).xpath('//p[@class="p-target"]//text()').extract()[4]) 
			m3_s = re.sub(r'\n\s+','',Selector(text=html).xpath('//p[@class="p-target"]//text()').extract()[3])
			m4_s = re.split(r'！',re.sub(r'\n\s+','',Selector(text=html).xpath('//p[@class="p-target"]//text()').extract()[5]))[0]
			item['info_demand'] = m1_s + m_d + m2_s + m_m + m3_s + m4_s
		except IndexError as s:
			pass
		#众筹发起人/公司地址
		try:
			item['info_address'] = re.sub(r'\xa0','',Selector(text=html).xpath('//div[@class="val"]/text()').extract()[1])
		except IndexError as s:
			pass
		#众筹联系电话
		try:
			item['info_contact'] = re.sub(r'\xa0','',Selector(text=html).xpath('//div[@class="val"]/text()').extract()[2])
		except IndexError as s:
			pass
		#工作时间
		try:
			item['info_time'] = re.sub(r'\xa0','',Selector(text=html).xpath('//div[@class="val"]/text()').extract()[3])
		except IndexError as s:
			pass
		#众筹进度
		try:
			item['info_rate'] = int(re.findall(r'\d+',Selector(text=html).xpath('//span[@class="fl percent"]/text()').extract()[0])[0]) / 100
		except IndexError as s:
			pass
		items.append(item)
		return items
