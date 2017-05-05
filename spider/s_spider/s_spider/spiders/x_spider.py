# -*- coding: utf-8 -*-
import scrapy
from s_spider.items import SSpiderItem
from selenium import webdriver
from scrapy.selector import Selector
import re
import os
import pymongo
import time


class XSpiderSpider(scrapy.Spider):
	client = pymongo.MongoClient('localhost',27017)
	db = client.opalus
	coll = db.site
	conn = db.url_list
	copt = db.product
	
	name = "x_spider"
#加载域名
	allowed_domains = []
	for i in coll.find({},{"url":1,"_id":0}):
		if i:
			allowed_domains.append(re.split(r'\/',i['url'])[2])		
		else:
			print (i + ":是空值不存在")
			pass
#加载启动url
	start_urls = []
#	site_count = []
#	for i in coll.find({},{"site_from":1,'_id':0}):
#		if i:
#			site_count.append(i['site_from'])
#		else:
#			print ('site_from的值为空')
#			pass
#	for i in site_count:
#		copt_count = copt.find({'site_from':i}).count()
#		conn_count = len(conn.distinct('url',{'site_from':i,}))
#		if conn_count > 

#	for i in coll.find({},{"url":1,"_id":0}):
#		if i:
#			start_urls.append(i['url'])	
#		else:
#			print (i + ":是空值不存在")
#			pass
	for i in conn.find({},{'url':1,"_id":0}):
		if i:
			start_urls.append(i['url'])
		else:
			print (i + ":是空值不存在")
			pass
	start_urls = set(start_urls)
	#start_urls = []
	#start_urls = ['https://z.jd.com/bigger/search.html','http://h5.yit.com']

	def parse(self, response):
		#pass
		client = pymongo.MongoClient('localhost',27017)
		db = client.opalus
		coll = db.site
		conn = db.url_list
		js = re.sub(r'\n','',os.popen('which phantomjs').read())
		browser = webdriver.PhantomJS(executable_path = js)
		#京东众筹起始url
		for i in coll.find({"mark":'JDZC'}):
			if i:
				jdzc = i['url']
				jdzc_site = i['site_from']
				jdzc_type = i['site_type']
				jdzc_domain = re.split(r'\/',jdzc)[2]
			else:
				print (i + ':京东众筹url为空')
				pass
		#一条生活馆起始url
		for i in coll.find({"mark":"YTSHG"}):
			if i:
				yit = i['url']
				yit_site = i['site_from']
				yit_type = i['site_type']
				yit_domain = re.split(r'\/',yit)[2]
			else:
				print (i + ':一条生活馆url为空')
				pass
			
		#如果请求的url地址是京东的起始页面地址,则爬取页面url
		if response.url == jdzc:
			#url地址池已有地址列表
			items = []
			browser.get(response.url)
			browser.implicitly_wait(10)
			html = browser.page_source
			try:
				page_count = Selector(text=html).xpath('//div[@class="pagesbox"]//a/text()').extract()[-2]
				if page_count:
					for i in range(1,3):#int(page_count) + 1):
						url = response.url + '?page=' + str(i)
						if url in conn.distinct('url',{"site_from":jdzc_site}):
							continue
						else:
							item = SSpiderItem()
							item['url'] = url
							item['title'] = jdzc_site
							item['site_from'] = jdzc_site
							items.append(item)
				else:
					pass
			except IndexError as s:
				pass
			return items
		#如果请求url是京东的列表页面则爬取详情页url
		elif jdzc_domain in response.url and '?page=' in response.url:
			#url地址池已有地址列表
			items = []
			browser.get(response.url)
			browser.implicitly_wait(10)
			html = browser.page_source
			#获取详情页url
			try:
				url_list = Selector(text=html).xpath('//div[@class="i-tits"]//a/@href').extract()
				url_list = set(url_list)
				if url_list:
					for i in url_list:
						if i in conn.distinct('url',{"site_from":jdzc_site}):
							pass
						else:
							item = SSpiderItem()
							item['url'] = 'https://' + jdzc_domain + i
							item['category_tags'] = jdzc_site
							item['site_from'] = jdzc_site
							items.append(item)
				else:
					pass
			except IndexError as s:
				pass
			return items
		elif jdzc_domain in response.url and '?page=' not in response.url:
			items = []
			browser.get(response.url)
			browser.implicitly_wait(10)
			html = browser.page_source
			item = SSpiderItem()
			#url
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
			item['site_from'] = jdzc_site
			#销售模式
			item['site_type'] = jdzc_type
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
			#销售总额
			except IndexError as s:
				pass
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
		
		#如果请求的url地址是一条生活馆的起始页面地址,则获取分类页面url
		elif response.url == yit:
			#url地址池已有地址列表
			items = []
			browser.get(response.url)
			browser.implicitly_wait(10)
			html = browser.page_source
			#获取
			try:
				url_list = []
				for i in Selector(text=html).xpath('//div[@class="module h5Navigate_1_32 "]//li//a/@href').extract():
					I = re.split(r'\?_spm',i)[0]
					url_list.append(I)
				url_title = Selector(text=html).xpath('//div[@class="module h5Navigate_1_32 "]//li//text()').extract()
				if url_list and url_title:
					for i in range(0,len(url_list)):
						new_url = url_list[i]
						if new_url in conn.distinct('url',{"site_from":yit_site}):
							pass
						else:
							item = SSpiderItem()
							item['url'] = url_list[i]
							item['title'] = yit_site
							item['tags'] = url_title[i]
							item['site_from'] = yit_site
							items.append(item)
				else:
					pass
			except IndexError as s:
				pass
			return items
#################################################################################
		elif '?product_id=' not in response.url and yit_domain in response.url:
			#url地址池已有地址列表
			items = []
			browser.get(response.url)
			browser.implicitly_wait(10)
			html = browser.page_source
			for i in conn.find({'url':response.url}):
				if i:
					data_from = i
				else:
					print (i + ":是空值不存在")
					pass
			try:
				url_list = []
				for i in Selector(text=html).xpath('//li[@class="cms-src-item"]//a/@href').extract():
					I = re.split("&_spm",i)[0]
					url_list.append(I)
				url_list = set(url_list)
				if url_list:
					for i in url_list:
						if i in conn.distinct('url',{"site_from":yit_site}):
							continue
						else:
							item = SSpiderItem()
							item['url'] = i
							item['category_tags'] = yit_site
							item['tags'] = data_from['tags']
							item['site_from'] = yit_site
							items.append(item)
				else:
					pass
			except IndexError as s:
				pass
			return items
###################################################################################
		elif '?product_id=' in response.url and yit_domain in response.url:
			items = []
			item = SSpiderItem()
			browser.get(response.url)
			browser.implicitly_wait(10)
			html = browser.page_source
			for i in conn.find({'url':response.url}):
				if i:
					data_from = i
				else:
					print (i + ":是空值不存在")
					pass
			#网址
			try:
				item['url'] =  response.url
			except IndexError as s:
				pass
			#站点来源
			item['site_from'] = yit_site
			#销售模式
			item['site_type'] = yit_type
			#产品编号
			item['out_number'] = re.compile(r'\d+').findall(re.split(r'\?',response.url)[-1])[0]
			#名称
			try:
				title_tmp = Selector(text=html).xpath('//div[@id="description"]//p//text()').extract()
				if title_tmp:
					if "品名：" in title_tmp:
						if "\xa0" in title_tmp[title_tmp.index("品名：") + 1]:
							item['title'] = re.sub(r'\xa0',' ',title_tmp[title_tmp.index("品名：") + 1])
						else:
							item['title'] = title_tmp[title_tmp.index("品名：") + 1]
					elif "器名：" in title_tmp:
						item['title'] = title_tmp[title_tmp.index("器名：") + 1]
					elif "器名" in title_tmp:
						item['title'] = re.split(r"：",title_tmp[title_tmp.index("器名") + 1])[-1]
					elif "名称" in title_tmp:
						item['title'] = re.split(r"：",title_tmp[title_tmp.index("名称") + 1])[-1]
					elif "名称：" in title_tmp:
						item['title'] = title_tmp[title_tmp.index("名称：") + 1]
					elif "名字：" in title_tmp:
						item['title'] = title_tmp[title_tmp.index("名字：") + 1]
					elif "书名：" in title_tmp:
						item['title'] = title_tmp[title_tmp.index("书名：") + 1]
					elif "品名：" in ','.join(title_tmp):
						for i in title_tmp:
							if "品名：" in i:
								item['title'] = re.split(r"品名：",title_tmp[title_tmp.index(i)])[-1]
								break
					else:
						title_tmp = Selector(text=html).xpath('//div[@class="page-title"]//span[@id="proTitle"]/text()').extract()[0]
						if "（" in title_tmp:
							item['title'] = re.split(r'（',Selector(text=html).xpath('//div[@class="page-title"]//span[@id="proTitle"]/text()').extract()[0])[0]
						else:
							reg = Selector(text=html).xpath('//li//strong/text()').extract()[0]
							item['title'] = re.split(reg,title_tmp)[0]
			except IndexError as s:
				pass
			#内容
			try:
				content_tmp = Selector(text=html).xpath('//div[@id="product_description"]//p//text()').extract()
				if content_tmp:
					item['content'] = ','.join(content_tmp)
			except IndexError as s:
				pass
			#品牌名
			try:
				brand_name_tmp = Selector(text=html).xpath('//div[@id="description"]//p//text()').extract()
				brand_name_temp = Selector(text=html).xpath('//div[@id="product_description"]//span//text()').extract()
				if brand_name_tmp:
					if "作者" in brand_name_tmp:
						item['brand_name'] = re.split("：",brand_name_tmp[brand_name_tmp.index("作者") + 1])[-1]
					elif "作者：" in brand_name_tmp:
						item['brand_name'] = brand_name_tmp[brand_name_tmp.index("作者：") + 1]
					elif "品牌：" in brand_name_tmp:
						item['brand_name'] = brand_name_tmp[brand_name_tmp.index("品牌：") + 1]
					elif "出品" in ','.join(brand_name_temp):
						item['brand_name'] = re.split(r"：",re.split(r"出品",','.join(brand_name_temp))[-1])[-1]
					elif "品牌" in brand_name_tmp:
						item['brand_name'] = re.split("：",brand_name_tmp[brand_name_tmp.index("品牌") + 1])[-1]
					elif "著者：" in brand_name_temp:
						item['brand_name'] = brand_name_temp[brand_name_temp.index("著者：") + 1]
					elif "作者" in brand_name_temp:
						item['brand_name'] = re.split(r"：",brand_name_temp[brand_name_temp.index("作者") + 1])[-1]
					elif "品牌：" in brand_name_temp:
						item['brand_name'] = brand_name_temp[brand_name_temp.index("品牌：") + 1]
					else:
						item['brand_name'] = Selector(text=html).xpath('//li//strong/text()').extract()[0]
			except IndexError as s:
				pass
			#品牌地址
			try:
				brand_address = Selector(text=html).xpath('//div[@id="product_description"]//span//text()').extract()
				if "产地：" in brand_address:
					item['brand_address'] = brand_address[brand_address.index("产地：") + 1]
				elif "产地" in brand_address:
					item['brand_address'] = brand_address[brand_address.index("产地") + 2]
				elif "上课地点：" in brand_address:
					item['brand_address'] = brand_address[brand_address.index("上课地点：") + 1]
				elif "出版" in brand_address:
					item['brand_address'] = re.split(r"：",brand_address[brand_address.index("出版") + 1])[-1]
				elif "出版：" in brand_address:
					temp = brand_address[brand_address.index("出版：") + 1]
					if "/" in temp:
						item['brand_address'] = temp + brand_address[brand_address.index("出版：") + 2]
					else:
						item['brand_address'] = temp
				elif "出版社：" in brand_address:
					item['brand_address'] = brand_address[brand_address.index("出版社：") + 1]
				elif "种植地：" in brand_address:
					item['brand_address'] = brand_address[brand_address.index("种植地：") + 1]
				elif "原产地：" in brand_address:
					item['brand_address'] = brand_address[brand_address.index("原产地：") + 1]
				elif "产地：" in ','.join(brand_address):
					for i in brand_address:
						if "产地：" in i:
							item['brand_address'] = re.split(r"产地：",brand_address[brand_address.index(i)])[-1]
				else:
					brand_address = Selector(text=html).xpath('//div[@id="product_description"]//span//text()').extract()
					for i in brand_address:
						if "原产地" in i:
							N = brand_address[brand_address.index(i)]
							item['brand_address'] = re.split(r'：',N)[-1]
							break
			except IndexError as s:
				pass
			#产品编号		
			try:
				item['out_number'] = re.compile(r'\d+').findall(re.split(r'\/',response.url)[-1])[0]
			except IndexError as s:
				pass
	
			#分类
			#category_tags = scrapy.Field()	#string	多个用逗号做连接符号
			item['category_tags'] = data_from['tags']
			#标签
			item['tags'] = data_from['tags']
			#产品封面图
			try:
				cover_url_tmp = Selector(text=html).xpath('//ul[@class="swiper-wrapper"]//li//img/@src').extract()[0]
				if "jpg" in cover_url_tmp:
					item['cover_url'] = cover_url_tmp
				else:
					item['cover_url'] = Selector(text=html).xpath('//div[@id="description"]//img/@src').extract()[0]
			except IndexError as s:
				pass
			#销售价
			try:
				item['sale_price'] = float(re.compile(r'\d+').findall(Selector(text=html).xpath('//span[@class="price"]/text()').extract()[0])[0])
			except IndexError as s:
				pass
			#原产品封面图地址
			try:
				item['o_cover_url'] = "/data/images/yit/" + re.compile(r'\d+').findall(re.split(r'\/',response.url)[-1])[0] + '.jpg'
			except IndexError as s:
				pass
			items.append(item)
			return items
		else:
			print ("执行完毕")
			pass
		
