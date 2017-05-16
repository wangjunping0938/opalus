# -*- coding: utf-8 -*-
import scrapy
from s_spider.items import SSpiderItem
from selenium import webdriver
from scrapy.selector import Selector
import re
import os
import sys
sys.path.append(os.path.abspath('.'))
import rule
import time



class DetailsUrlSpider(scrapy.Spider):
	name = "details_url"
	#爬虫的域名范围列表
	allow_domains = rule.connMongoDB.domainList()
	#爬虫将爬取的页面url列表
	start_urls = rule.connMongoDB.secondUrlList()
	print ('test############################')
	print (allow_domains)
	print ('test############################')
	print (start_urls)
	print ('test############################')

	def parse(self, response):
		#当前请求的url
		url = response.url
		#当前请求的url的站点来源
		site_from = rule.SECOND.siteFrom(url)
		site_type = rule.SECOND.siteType(url)
		second_url_list = rule.connMongoDB.secondUrlList()
		title = rule.SECOND.urlTitle(url)
		items = []
		#调用浏览器phantomjs获取url页面源代码
		browser = rule.phantomJS.browser()
		browser.get(url)
		browser.implicitly_wait(20)
		html = browser.page_source
		if url in second_url_list:
			url_list = rule.SECOND.urlDetailsList(html,url)
			details_url_list = rule.connMongoDB.detailsUrlList()
			print ('test################################')
			print (url_list)
			print ('test################################')
			if url_list:
				for i in url_list:
					if i in details_url_list:
						pass
					else:
						item = SSpiderItem()
						#详情页url
						item['url'] = i
						#详情页url站点来源
						item['site_from'] = site_from
						#详情页url标识
						item['tags'] = 'details'
						#站点销售类型
						item['site_type'] = site_type
						#u二级页面站点来源标识
						item['mark'] = title
						items.append(item)
				return items
			else:
				pass
		else:
			print ("url不属于二级页面url,无法爬去详情页url")
			pass
