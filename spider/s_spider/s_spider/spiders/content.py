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


class ContentSpider(scrapy.Spider):
	name = "content"
	#爬虫的域名范围列表
	allow_domains = rule.connMongoDB.domainList()
	#爬虫将爬取的页面url列表
	start_urls = rule.connMongoDB.detailsUrlList()
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
		details_url_list = rule.connMongoDB.detailsUrlList()
		func = rule.SECOND.urlTitle(url)
		FUNC = 'rule.' + func
		print (FUNC)
		#title = eval(FUNC).urlTitle(url)
		items = []
		#调用浏览器phantomjs获取url页面源代码
		browser = rule.phantomJS.browser()
		browser.get(url)
		browser.implicitly_wait(20)
		html = browser.page_source
		#获取详情页内容
		if url in details_url_list:
			item = SSpiderItem()
			#网址			String
			try:
				item['url'] = response.url
			except AttributeError:
				pass
			except KeyError:
				pass
			#站点来源		Integer
			try:
				item['site_from'] = site_from
			except AttributeError:
				pass
			except KeyError:
				pass
			#销售模式		Integer	,1=正常销售,2=众筹,3=抢购
			try:
				item['site_type'] = site_type
			except AttributeError:
				pass
			except KeyError:
				pass
			#产品编号		String
			try:
				item['out_number']  = eval(FUNC).outNumber(url)
			except AttributeError:
				pass
			except AttributeError:
				pass
			#名称			String
			try:
				item['title'] = eval(FUNC).title(html)
			except AttributeError:
				pass
			except AttributeError:
				pass
			#子名称			String
			try:
				item['sub_title'] = eval(FUNC).subTitle(html)
			except AttributeError:
				pass
			except KeyError:
				pass
			#简述			String
			try:
				item['resume'] =  eval(FUNC).resume(html)
			except AttributeError:
				pass
			except KeyError:
				pass
			#内容			String
			try:
				item['content'] = eval(FUNC).content(html)
			except AttributeError:
				pass
			except KeyError:
				pass
			#品牌名			String
			try:
				item['brand_name'] = eval(FUNC).brandName(html)
			except AttributeError:
				pass
			except KeyError:
				pass
			#品牌联系方式	String
			try:
				item['brand_contact'] = eval(FUNC).brandContact(html)
			except AttributeError:
				pass
			except KeyError:
				pass
			#品牌地址		String
			try:
				item['brand_address'] = eval(FUNC).brandAddress(html)
			except AttributeError:
				pass
			except KeyError:
				pass
			#分类			String	多个用","分割
			try:
				item['category_tags'] = eval(FUNC).categoryTags(html)
			except AttributeError:
				pass
			except KeyError:
				pass
			#标签			String	多个用","分割
			try:
				item['tags'] = eval(FUNC).tags(html)
			except AttributeError:
				pass
			except KeyError:
				pass
			#产品封面图		String
			try:
				item['cover_url'] = eval(FUNC).coverUrl(html)
			except AttributeError:
				pass
			except KeyError:
				pass
			#原产品封面图地址	String
			try:
				item['o_cover_url'] = eval(FUNC).oCoverUrl(url)
			except AttributeError:
				pass
			except KeyError:
				pass
			#评分			float
			try:
				item['rate'] = eval(FUNC).rate(html)
			except AttributeError:
				pass
			except KeyError:
				pass
			#成本价			float
			try:
				item['cost_price'] = eval(FUNC).costPrice(html)
			except AttributeError:
				pass
			except KeyError:
				pass
			#销售价			float
			try:
				item['sale_price'] = eval(FUNC).salePrice(html)
			except AttributeError:
				pass
			except KeyError:
				pass
			#销售总额		float
			try:
				item['total_price'] = eval(FUNC).totalPrice(html)
			except AttributeError:
				pass
			except KeyError:
				pass
			#喜欢/点赞数	Integer
			try:
				item['love_count'] = eval(FUNC).loveCount(html)
			except AttributeError:
				pass
			except KeyError:
				pass
			#收藏/订阅数	Integer
			try:
				item['favorite_count'] = eval(FUNC).favoriteCount(html)
			except AttributeError:
				pass
			except KeyError:
				pass
			#评论数			Integer
			try:
				item['comment_count'] = eval(FUNC).commentCount(html)
			except AttributeError:
				pass
			except KeyError:
				pass
			#销售数量		Integer
			try:
				item['sale_count'] = eval(FUNC).saleCount(html)
			except	AttributeError:
				pass
			except KeyError:
				pass
			#浏览数			Integer
			try:
				item['view_count'] = eval(FUNC).viewCount(html)
			except AttributeError:
				pass
			except KeyError:
				pass
			#支持人数		Integer
			try:
				item['support_count'] = eval(FUNC).supportCount(html)
			except AttributeError:
				pass
			except KeyError:
				pass
			#众筹发起人/公司	String
			try:
				item['info_name'] = eval(FUNC).infoName(html)
			except AttributeError:
				pass
			except KeyError:
				pass

			#众筹标准			String
			try:
				item['info_demand'] = eval(FUNC).infoDemand(html)
			except AttributeError:
				pass
			except KeyError:
				pass
			#众筹发起人/公司地址	String
			try:
				item['info_address'] = eval(FUNC).infoAddress(html)
			except AttributeError:
				pass
			except KeyError:
				pass
			#众筹联系电话		String
			try:
				item['info_contact'] = eval(FUNC).infoContact(html)
			except AttributeError:
				pass
			except KeyError:
				pass
			#工作时间			String
			try:
				item['info_time'] = eval(FUNC).infoTime(html)
			except AttributeError:
				pass
			except KeyError:
				pass
			#众筹进度			float	百分比/100
			try:
				item['info_rate'] = eval(FUNC).infoRate(html)
			except AttributeError:
				pass
			except KeyError:
				pass
			#众筹剩余时间		String
			try:
				item['info_last_time'] = eval(FUNC).infoLastTime(html)
			except AttributeError:
				pass
			except KeyError:
				pass
			items.append(item)	
			return items	
			
		else:
			pass
