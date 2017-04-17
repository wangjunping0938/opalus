# -*- coding: utf-8 -*-
import scrapy
import os
import re
import time
import fileinput
from h5_yit.items import H5YitItem
from selenium import webdriver
from scrapy.selector import Selector

class YitSpiderSpider(scrapy.Spider):
	name = "yit_spider"
	allowed_domains = ["h5.yit.com"]
	url0="http://h5.yit.com/product.html?product_id="
	start_urls = []
	#for i in range(17672,30000):
	#	start_urls.append(url0 + '%s' % (i))
	start_urls = ["http://h5.yit.com/product.html?product_id=17630"]

	def parse(self, response):
        #pass
		items = []
		item = H5YitItem()
		browser = webdriver.PhantomJS()
		browser.get(response.url)
		browser.implicitly_wait(10)
		html = browser.page_source

		#网址
		try:
			item['url'] =  response.url
		except IndexError as s:
			pass
		#站点来源
		item['site_from'] = 4
		#销售模式
		item['site_type'] = 1
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

	#成本价
	#cost_price
	#子名称
	#sub_title = scrapy.Field()		#string
	#简述
	#resume = scrapy.Field()			#string  
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
	#品牌联系方式
	#brand_contact = scrapy.Field()	#string
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
	#标签
	#tags = scrapy.Field()			#string	多个用逗号分隔
		#产品封面图
		try:
			cover_url_tmp = Selector(text=html).xpath('//ul[@class="swiper-wrapper"]//li//img/@src').extract()[0]
			if "jpg" in cover_url_tmp:
				item['cover_url'] = cover_url_tmp
			else:
				item['cover_url'] = Selector(text=html).xpath('//div[@id="description"]//img/@src').extract()[0]
		except IndexError as s:
			pass
	#评分
	#rate = scrapy.Field()			#float
	#成本价
	#cost_price = scrapy.Field()		#float
		#销售价
		try:
			item['sale_price'] = float(re.compile(r'\d+').findall(Selector(text=html).xpath('//span[@class="price"]/text()').extract()[0])[0])
		except IndexError as s:
			pass
	#销售总额
	#total_price = scrapy.Field()	#float
	#喜欢/点赞数
	#love_count = scrapy.Field()		#integer
	#收藏/订阅数
	#favorite_count = scrapy.Field()	#integer
	#评论数
	#comment_count = scrapy.Field()	#integer
	#销售数量
	#sale_count = scrapy.Field()		#integer
	#浏览数
	#view_count = scrapy.Field()		#integer
		#原产品封面图地址
		try:
			item['o_cover_url'] = "/data/images/yit/" + re.compile(r'\d+').findall(re.split(r'\/',response.url)[-1])[0] + '.jpg'
			
	#re.split(r'\.',re.split(r'\-620',os.path.basename(Selector(text=html).xpath('//ul[@class="swiper-wrapper"]//li//img/@src').extract()[0]))[0])[-1]
	#re.split(r'\-',re.split(r'\.',os.path.basename(Selector(text=html).xpath('//ul[@class="swiper-wrapper"]//li//img/@src').extract()[0]))[1])[0]
		except IndexError as s:
			pass
		items.append(item)
		return items
