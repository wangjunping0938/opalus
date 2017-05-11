# -*- coding: utf-8 -*-
import scrapy
from s_spider.items import SSpiderItem
from selenium import webdriver
from scrapy.selector import Selector
import re
import os
import sys
#sys.path.append(os.path.dirname(os.path.abspath('.')))
#sys.path.append(os.path.abspath(os.path.dirname(os.path.abspath('./rule')))
sys.path.append(os.path.abspath('.'))
sys.path.append(os.path.abspath('./rule'))
import connMongoDB
import phantomJS
import JDZC
import YTSHG
import time

	
class XSpiderSpider(scrapy.Spider):
	#爬虫名称
	name = "x_spider"
	#爬虫的域名范围列表
	allow_domains = connMongoDB.domainList()
	#爬虫将爬取的页面url列表
	start_urls = connMongoDB.startUrlList()
	
	print ('test############################')
	print (allow_domains)
	print ('test############################')
	print (start_urls)
	print ('test############################')

	def parse(self, response):
		#当前请求的url
		url = response.url
		#当前请求的url的站点来源
		site_from = YTSHG.siteFrom(url)
		start_url_list = connMongoDB.StartUrlList()
		second_url_list = connMongoDB.secondUrlList()
		details_url_list = connMongoDB.detailsUrlList()
		title = YTSHG.urlTitle(url)
		items = []
		#调用浏览器phantomjs获取url页面源代码
		browser = phantomJS.browser()
		browser.get(url)
		browser.implicitly_wait(20)
		html = browser.page_source
		#获取二级页面url
		if url in start_url_list:
			url_list = YTSHG.urlList(html,url)
			print ('test########################')
			print (url_list)
			print ('test########################')
			if url_list:
				for i in url_list:
					if i in second_url_list:
						pass
					else:
						item = SSpiderItem()
						#二级页面url
						item['url'] = i
						#二级页面url站点来源
						item['site_from'] = site_from
						#二级页面url类型
						item['site_type'] = YTSHG.siteType(url)
						#二级页面站点来源名称
						item['title'] = 'second'
						items.append(item)
				return items
			else:
				print ('url已经全部添加')
				pass
		#获取详情页url
		elif url in second_url_list:
			url_list = YTSHG.urlDetailsList(html,url)
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
						#详情页url类型
						item['site_type'] = YTSHG.siteType(url)
						#详情页url标识
						item['tags'] = 'details'
						items.append(item)
				return items
			else:
				pass
		#获取详情页内容
		elif url in details_url_list:
			item = SSpiderItem()
			#网址			String
			try:
				item['url'] = response.url
			except KeyError:
				pass
			#站点来源		Integer
			try:
				item['site_from'] = site_from
			except KeyError:
				pass
			#销售模式		Integer	,1=正常销售,2=众筹,3=抢购
			try:
				item['site_type'] = YTSHG.siteType(url)
			except KeyError:
				pass
			#产品编号		String
			try:
				item['out_number']  = YTSHG.outNumber(url)
			except KeyError:
				pass
			#名称			String
			try:
				item['title'] = YTSHG.title(html)
			except KeyError:
				pass
			#子名称			String
			try:
				item['sub_title']
			except KeyError:
				pass
			#简述			String
			try:
				item['resume'] #= JDZC.resume(html)
			except KeyError:
				pass
			#内容			String
			try:
				item['content'] = YTSHG.content(html)
			except KeyError:
				pass
			#品牌名			String
			try:
				item['brand_name'] = YTSHG.brandName(html)
			except KeyError:
				pass
			#品牌联系方式	String
			try:
				item['brand_contact'] 
			except KeyError:
				pass
			#品牌地址		String
			try:
				item['brand_address'] = YTSHG.brandAddress(html)
			except KeyError:
				pass
			#分类			String	多个用","分割
			try:
				item['category_tags']# = JDZC.categoryTags(html)
			except KeyError:
				pass
			#标签			String	多个用","分割
			try:
				item['tags'] #= JDZC.tags(html)
			except KeyError:
				pass
			#产品封面图		String
			try:
				item['cover_url'] = YTSHG.coverUrl(html)
			except KeyError:
				pass
			#原产品封面图地址	String
			try:
				item['o_cover_url'] = YTSHG.oCoverUrl(url)
			except KeyError:
				pass
			#评分			float
			try:
				item['rate'] 
			except KeyError:
				pass
			#成本价			float
			try:
				item['cost_price']
			except KeyError:
				pass
			#销售价			float
			try:
				item['sale_price'] = YTSHG.salePrice(html)
			except KeyError:
				pass
			#销售总额		float
			try:
				item['total_price'] #= JDZC.totalPrice(html)
			except KeyError:
				pass
			#喜欢/点赞数	Integer
			try:
				item['love_count'] #= JDZC.loveCount(html)
			except KeyError:
				pass
			#收藏/订阅数	Integer
			try:
				item['favorite_count']# = JDZC.favoriteCount(html)
			except KeyError:
				pass
			#评论数			Integer
			try:
				item['comment_count'] 
			except KeyError:
				pass
			#销售数量		Integer
			try:
				item['sale_count']
			except KeyError:
				pass
			#浏览数			Integer
			try:
				item['view_count']
			except KeyError:
				pass
			#支持人数		Integer
			try:
				item['support_count'] #= JDZC.supportCount(html)
			except KeyError:
				pass
			#众筹发起人/公司	String
			try:
				item['info_name'] #= JDZC.infoName(html)
			except KeyError:
				pass
			#众筹标准			String
			try:
				item['info_demand'] #= JDZC.infoDemand(html)
			except KeyError:
				pass
			#众筹发起人/公司地址	String
			try:
				item['info_address']# = JDZC.infoAddress(html)
			except KeyError:
				pass
			#众筹联系电话		String
			try:
				item['info_contact'] #= JDZC.infoContact(html)
			except KeyError:
				pass
			#工作时间			String
			try:
				item['info_time']# = JDZC.infoTime(html)
			except KeyError:
				pass
			#众筹进度			float	百分比/100
			try:
				item['info_rate'] #= JDZC.infoRate(html)
			except KeyError:
				pass
			#众筹剩余时间		String
			try:
				item['info_last_time'] #= JDZC.infoLastTime(html)
			except KeyError:
				pass
			items.append(item)	
			return items	
			
		else:
			pass

