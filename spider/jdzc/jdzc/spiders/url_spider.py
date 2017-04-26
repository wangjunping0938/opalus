# -*- coding: utf-8 -*-
import scrapy
import os
import re
import time
import fileinput
from jdzc.items import JdzcItem
from selenium import webdriver
from scrapy.selector import Selector
import pymongo

class JdzcSpiderSpider(scrapy.Spider):
	name = "url_spider"
	allowed_domains = ["z.jd.com/bigger/search.html"]
	start_urls = ["https://z.jd.com/bigger/search.html"]
	js = re.sub(r'\n','',os.popen('which phantomjs').read())
	browser = webdriver.PhantomJS(executable_path = js)
	browser.get(start_urls[0])
	browser.implicitly_wait(10)
	page = browser.page_source
	page_count = Selector(text=page).xpath('//div[@class="pagesbox"]//a/text()').extract()[-2]
	for i in range(1,int(page_count) + 1):
		start_urls.append(start_urls[0] + '?page=' + str(i))
		
		

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
			url_list = Selector(text=html).xpath('//div[@class="i-tits"]//a/@href').extract()
			for i in url_list:
				item['url'] = "https://z.jd.com" + i
				items.append(item)
		except IndexError as s:
			pass
		item['site_from'] = 1
		items.append(item)
		time.sleep(1)
		return items
