# -*- coding: utf-8 -*-
import scrapy
import os
import re
import time
import fileinput
from jdzc.items import JdzcItem
from selenium import webdriver
from scrapy.selector import Selector


class JdzcSpiderSpider(scrapy.Spider):
	name = "jdzc_spider"
	allowed_domains = ["http://z.jd.com"]
	urls = time.strftime('%Y%m%d',time.localtime()) + ".txt"
	start_urls = []
	for i in fileinput.input(urls):
		i = i.strip('\n')
		start_urls.append(allowed_domains[0] + i)
	
	def parse(self, response):
        #pass
		items = []
		item = JdzcItem()
		#网址
		try:
#			item['url'] = re.split("\&",re.split("\=",response.xpath('//div[@class="tab-share-r"]//li/a/@href').extract()[-2],maxsplit=2)[1],maxsplit=2)[0]
			item['url'] = response.url
		except IndexError as s:
			pass
		#关注人数
		#引用浏览器
		browser = webdriver.PhantomJS()
		#使用浏览器请求url页面
		browser.get(response.url)
		browser.implicitly_wait(10)
		html = browser.page_source
		try:
			favorite_count0 = re.sub(r'[\(\)]','',Selector(text=html).xpath('//div[@class="project-introduce"]//p[@class="p-btns"]//a[1]/span[@class="num"]/text()').extract()[0])
			favorite_count1 = re.compile(r'\d+').findall(re.sub(r'[\(\)]','',Selector(text=html).xpath('//div[@class="project-introduce"]//p[@class="p-btns"]//a[1]/span[@class="num"]/text()').extract()[0]))[0]
			if favorite_count0.endswith("千"):
				item['favorite_count'] = favorite_count1 + "000"
				item['favorite_count'] = int(item['favorite_count'])
			elif favorite_count0.endswith("万"):
				item['favorite_count'] = favorite_count1 + "0000"
				item['favorite_count'] = int(item['favorite_count'])
			else:
				item['favorite_count'] = int(favorite_count0)
		except IndexError as s:
			pass 
		#点赞人数
		try:
			love_count0 = re.sub(r'[\(\)]','',Selector(text=html).xpath('//div[@class="project-introduce"]//p[@class="p-btns"]//a[2]/span[@class="num"]/text()').extract()[0])
			love_count1 = re.compile(r'\d+').findall(re.sub(r'[\(\)]','',Selector(text=html).xpath('//div[@class="project-introduce"]//p[@class="p-btns"]//a[2]/span[@class="num"]/text()').extract()[0]))[0]
			if love_count0.endswith("千"):
				item['love_count'] = love_count1 + "000"
				item['love_count'] = int(item['love_count'])
			elif love_count0.endswith("万"):
				item['love_count'] = love_count1 + "0000"
				item['love_count'] = int(item['love_count'])
			else:
				item['love_count'] = int(love_count0)
		except IndexError as s:
			pass
		#众筹剩余天数
		try:
			item['info_last_time'] = re.sub(r'\s+','',Selector(text=html).xpath('//div[@class="project-introduce"]//p[@class="p-target"]/span[@class="f_red"][3]/text()').extract()[0])
		except IndexError as s:
			pass
		#站点来源		
		item['site_from'] = 1
		#销售模式
		item['site_type'] = 2
		#名称
		try:
			item['title'] = response.xpath('//div[@class="wrap"]//div[@class="project-introduce"]//p[@class="p-title"]/text()').extract()[0]
		except IndexError as s:
			pass
		#简述
		try:
			item['resume'] = re.sub(r'[a-zA-Z0-9\.\/\?\=\&\:\_\%\-]','',response.xpath('//div[@class="tab-share-r"]//li/a/@href').extract()[-2])
		except IndexError as s:
			pass
		#品牌名
		try:
			item['brand_name'] = response.xpath('//div[@class="box-promoters"]//div[@class="promoters-name"]//a/@title').extract()[0]
		except IndexError as s:
			pass
		#分类
		try:
			item['category_tags'] = response.xpath('//div[@class="tab-share-l"]//a/text()').extract()[0]
		except IndexError as s:
			pass
		#产品编号
		try:
			item['out_number'] = re.findall(r'\d+',os.path.basename(re.split("\&",re.split("\=",response.xpath('//div[@class="tab-share-r"]//li/a/@href').extract()[-2],maxsplit=2)[1],maxsplit=2)[0]))[0]
		except IndexError as s:
			pass
		#标签
		try:
			item['tags'] = response.xpath('//div[@class="tab-share-l"]//a/text()').extract()[0]
		except IndexError as s:
			pass
		#产品封面图
		try:
			item['cover_url'] = "http:" + re.sub(r'\s+','',response.xpath('//div[@class="main"]//div[@class="project-img"]//img/@src').extract()[0])
		except IndexError as s:
			pass
		#re.sub(r'\s+','',response.xpath('//div[@class="project"]//div[@class="project-img"]/img//@src').extract()[0])
		#原产品封面图地址
		try:
			item['o_cover_url'] = "/data/images/jd/" + re.findall(r'\d+',os.path.basename(re.split("\&",re.split("\=",response.xpath('//div[@class="tab-share-r"]//li/a/@href').extract()[-2],maxsplit=2)[1],maxsplit=2)[0]))[0] + '.' + re.split('\.',os.path.basename(re.sub(r'\s+','',response.xpath('//div[@class="main"]//div[@class="project-img"]//img/@src').extract()[0])))[-1]
		except IndexError as s:
			pass
		#销售总额
		try:
			item['total_price'] = response.xpath('//div[@class="project-introduce"]//p[@class="p-num"]/text()').extract()[0]
		except IndexError as s:
			pass
		#喜欢/点赞数
	#收藏/订阅数
	#favorite_count = scrapy.Field()	#integer
	#评论数
	#comment_count = scrapy.Field()	#integer
	#销售数量
	#sale_count = scrapy.Field()		#integer
	#浏览数
	#view_count = scrapy.Field()		#integer
	#支持人数
		try:
			item['support_count'] = re.findall(r'\d+',response.xpath('//div[@class="project-introduce"]//p[@class="p-progress"]//span[@class="fr"]/text()').extract()[0])[0]
		except IndexError as s:
			pass
		#众筹发起人/公司
		try:
			item['info_name'] = response.xpath('//div[@class="box-promoters"]//div[@class="promoters-name"]//a/@title').extract()[0]
		except IndexError as s:
			pass
		#众筹标准
		try:
			mess1_str = re.sub(r'\s+',"",response.xpath('//div[@class="project-introduce"]//p[@id="projectMessage"]/text()').extract()[0])
			mess_date = re.sub(r'\s+',"",response.xpath('//div[@class="project-introduce"]//p[@id="projectMessage"]//span[1]/text()').extract()[0])
			mess2_str = re.sub(r'\s+',"",response.xpath('//div[@class="project-introduce"]//p[@id="projectMessage"]/text()').extract()[1])
			mess_money = response.xpath('//div[@class="project-introduce"]//p[@id="projectMessage"]//span[2]/text()').extract()[0]
			mess3_str = response.xpath('//div[@class="project-introduce"]//p[@id="projectMessage"]//span[2]/i/text()').extract()[0]
			mess4_str = re.sub(r'\s+',"",response.xpath('//div[@class="project-introduce"]//p[@id="projectMessage"]/text()').extract()[2])
			item['info_demand'] = mess1_str + mess_date + mess2_str + mess_money+mess3_str + mess4_str
		except IndexError as s:
			pass
		#众筹发起人/公司地址
		try:
			item['info_address'] = response.xpath('//div[@class="box-content"]//div[@class="val"]/text()').extract()[1]
		except IndexError as s:
			pass
		#众筹联系电话
		try:
			item['info_contact'] = response.xpath('//div[@class="box-content"]//div[@class="val"]/text()').extract()[2]
		except IndexError as s:
			pass
		#工作时间
		try:
			item['info_time'] = response.xpath('//div[@class="box-content"]//div[@class="val"]/text()').extract()[3]
		except IndexError as s:
			pass
		#众筹进度
		try:
			item['info_rate'] = int(re.findall(r'\d+',response.xpath('//div[@class="project-introduce"]//p[@class="p-progress"]//span[@class="fl percent"]/text()').extract()[0])[0]) / 100
		except IndexError as s:
			pass
	#众筹剩余时间
	#info_last_time = scrapy.Field()	#string
		items.append(item)
		return items
