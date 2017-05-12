#!/bin/env python
# -*- coding: utf-8 -*-

from scrapy.selector import Selector
import os
import re
import sys
sys.path.append(os.path.abspath('../'))
import connMongoDB
import phantomJS


html = ''
url = ''
def url(data):
	global url
	url = data
	return url
url('http://h5.yit.com/product.html?product_id=20700')
def html(url):
	global html
	browser = phantomJS.browser()
	browser.get(url)
	browser.implicitly_wait(10)
	html = browser.page_source
	return html
html(url)
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#获取内容方法
def outNumber(url):
	'''获取产品编号'''
	if url in connMongoDB.connMongo().site.distinct('url'):
		pass
	elif 'product' not in url:
		pass
	else:
		try:
			out_number = re.compile(r'\d+').findall(re.split(r'\?',url)[-1])[0]
			return out_number
		except IndexError as s:
			pass

def title(html):
	'''获取产品名称'''
	try:
		title_tmp = Selector(text=html).xpath('//div[@id="description"]//p//text()').extract()
		if title_tmp:
			if "品名：" in title_tmp:
				if "\xa0" in title_tmp[title_tmp.index("品名：") + 1]:
					title = re.sub(r'\xa0',' ',title_tmp[title_tmp.index("品名：") + 1])
					return title
				else:
					title = title_tmp[title_tmp.index("品名：") + 1]
					return title
			elif "器名：" in title_tmp:
				title = title_tmp[title_tmp.index("器名：") + 1]
				return title
			elif "器名" in title_tmp:
				title = re.split(r"：",title_tmp[title_tmp.index("器名") + 1])[-1]
				return title
			elif "名称" in title_tmp:
				title = re.split(r"：",title_tmp[title_tmp.index("名称") + 1])[-1]
				return title
			elif "名称：" in title_tmp:
				title = title_tmp[title_tmp.index("名称：") + 1]
				return title
			elif "名字：" in title_tmp:
				title = title_tmp[title_tmp.index("名字：") + 1]
				return title
			elif "书名：" in title_tmp:
				title = title_tmp[title_tmp.index("书名：") + 1]
				return title
			elif "品名：" in ','.join(title_tmp):
				for i in title_tmp:
					if "品名：" in i:
						title = re.split(r"品名：",title_tmp[title_tmp.index(i)])[-1]
						return title
						break
			else:
				title_tmp = Selector(text=html).xpath('//div[@class="page-title"]//span[@id="proTitle"]/text()').extract()[0]
				if "（" in title_tmp:
					title = re.split(r'（',Selector(text=html).xpath('//div[@class="page-title"]//span[@id="proTitle"]/text()').extract()[0])[0]
					return title
				else:
					reg = Selector(text=html).xpath('//li//strong/text()').extract()[0]
					title = re.split(reg,title_tmp)[0]
					return title
		else:
			pass
	except IndexError as s:
		pass
print (title(html))
def content(html):
	'''获取内容'''
	try:
		temp_content = Selector(text=html).xpath('//div[@id="product_description"]//p//text()').extract()
		if temp_content:
			content = ','.join(temp_content)
			return content
		else:
			pass
	except IndexError as s:
		pass

def brandName(html):
	'''获取品牌名'''
	try:
		brand_name_tmp = Selector(text=html).xpath('//div[@id="description"]//p//text()').extract()
		brand_name_temp = Selector(text=html).xpath('//div[@id="product_description"]//span//text()').extract()
		if brand_name_tmp or brand_name_temp:
			if "作者" in brand_name_tmp:
				brand_name = re.split("：",brand_name_tmp[brand_name_tmp.index("作者") + 1])[-1]
				return brand_name
			elif "作者：" in brand_name_tmp:
				brand_name = brand_name_tmp[brand_name_tmp.index("作者：") + 1]
				return brand_name
			elif "品牌：" in brand_name_tmp:
				brand_name = brand_name_tmp[brand_name_tmp.index("品牌：") + 1]
				return brand_name
			elif "出品" in ','.join(brand_name_temp):
				brand_name = re.split(r"：",re.split(r"出品",','.join(brand_name_temp))[-1])[-1]
				return brand_name
			elif "品牌" in brand_name_tmp:
				brand_name = re.split("：",brand_name_tmp[brand_name_tmp.index("品牌") + 1])[-1]
				return brand_name
			elif "著者：" in brand_name_temp:
				brand_name = brand_name_temp[brand_name_temp.index("著者：") + 1]
				return brand_name
			elif "作者" in brand_name_temp:
				brand_name = re.split(r"：",brand_name_temp[brand_name_temp.index("作者") + 1])[-1]
				return brand_name
			elif "品牌：" in brand_name_temp:
				brand_name = brand_name_temp[brand_name_temp.index("品牌：") + 1]
				return brand_name
			else:
				brand_name = Selector(text=html).xpath('//li//strong/text()').extract()[0]
				return brand_name
		else:
			pass
	except IndexError as s:
		pass

def brandAddress(html):
	'''获取品牌地址'''
	try:
		brand_address = Selector(text=html).xpath('//div[@id="product_description"]//span//text()').extract()
		if "产地：" in brand_address:
			brandaddress = brand_address[brand_address.index("产地：") + 1]
			return brandaddress
		elif "产地" in brand_address:
			brandaddress = brand_address[brand_address.index("产地") + 2]
			return brandaddress
		elif "上课地点：" in brand_address:
			brandaddress = brand_address[brand_address.index("上课地点：") + 1]
			return brandaddress
		elif "出版" in brand_address:
			brand_address = re.split(r"：",brand_address[brand_address.index("出版") + 1])[-1]
			return brandaddress
		elif "出版：" in brand_address:
			temp = brand_address[brand_address.index("出版：") + 1]
			if "/" in temp:
				brandaddress = temp + brand_address[brand_address.index("出版：") + 2]
				return brandaddress
			else:
				brandaddress = temp
				return brandaddress
		elif "出版社：" in brand_address:
			brandaddress = brand_address[brand_address.index("出版社：") + 1]
			return brandaddress
		elif "种植地：" in brand_address:
			brandaddress = brand_address[brand_address.index("种植地：") + 1]
			return brandaddress
		elif "原产地：" in brand_address:
			brandaddress = brand_address[brand_address.index("原产地：") + 1]
			return brandaddress
		elif "产地：" in ','.join(brand_address):
			for i in brand_address:
				if "产地：" in i:
					brandaddress = re.split(r"产地：",brand_address[brand_address.index(i)])[-1]
					return brandaddress
				else:
					brand_address = Selector(text=html).xpath('//div[@id="product_description"]//span//text()').extract()
					return brandaddress
					for i in brand_address:
						if "原产地" in i:
							N = brand_address[brand_address.index(i)]
							brandaddress = re.split(r'：',N)[-1]
							return brandaddress
							break
		else:
			pass
	except IndexError as s:
		pass
	
def coverUrl(html):
	'''获取封面图'''
	try:
		cover_url_tmp = Selector(text=html).xpath('//ul[@class="swiper-wrapper"]//li//img/@src').extract()[0]
		if "jpg" in cover_url_tmp:
			cover_url = cover_url_tmp
			return cover_url
		else:
			cover_url = Selector(text=html).xpath('//div[@id="description"]//img/@src').extract()[0]
			return cover_url
	except IndexError as s:
		pass

def salePrice(html):
	'''获取销售价格'''
	try:
		sale_price = float(re.compile(r'\d+').findall(Selector(text=html).xpath('//span[@class="price"]/text()').extract()[0])[0])
		return sale_price	
	except IndexError as s:
		pass

def oCoverUrl(url):
	'''获取原封面图'''
	try:
		o_cover_url = "/data/images/yit/" + re.compile(r'\d+').findall(re.split(r'\/',url)[-1])[0] + '.jpg'
		return o_cover_url
	except IndexError as s:
		pass
print (oCoverUrl(url))
