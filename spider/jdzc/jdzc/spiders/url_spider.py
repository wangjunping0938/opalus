# -*- coding: utf-8 -*-
import scrapy
import os
import re
from jdzc.items import JdzcItem
from selenium import webdriver
from scrapy.selector import Selector
import pymongo

class JdzcSpiderSpider(scrapy.Spider):
	name = "url_spider"
	allowed_domains = ["z.jd.com"]
	start_url = "https://z.jd.com/bigger/search.html"
	#浏览器执行文件路径
	js = re.sub(r'\n','',os.popen('which phantomjs').read())
	#引用浏览器
	browser = webdriver.PhantomJS(executable_path = js)
	browser.get(start_url)
	browser.implicitly_wait(10)
	page = browser.page_source
	#获取页面数量
	page_count = Selector(text=page).xpath('//div[@class="pagesbox"]//a/text()').extract()[-2]
	#起始页面列表
	start_urls = []
	for i in range(1,int(page_count) + 1):
		start_urls.append(start_url + '?page=' + str(i))
		
		

	def parse(self, response):
		items = []
		#浏览器执行文件路径
		js = re.sub(r'\n','',os.popen('which phantomjs').read())
		#引用浏览器
		browser = webdriver.PhantomJS(executable_path = js)
		browser.get(response.url)
		browser.implicitly_wait(10)
		html = browser.page_source
		#网址
		try:
			url_list = Selector(text=html).xpath('//div[@class="i-tits"]//a/@href').extract()
			if url_list:
				for i in url_list:
					item = JdzcItem()
					item['url'] = "https://z.jd.com" + i
					item['site_from'] = 1
					items.append(item)
			else:
				pass
		except IndexError as s:
			pass

		return items
