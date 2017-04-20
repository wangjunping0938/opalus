# -*- coding: utf-8 -*-
import scrapy
from url_jdzc.items import UrlJdzcItem


class UrlSpiderSpider(scrapy.Spider):
	name = "url_spider"
	allowed_domains = ["http://z.jd.com"]
	start_url = "https://z.jd.com/bigger/search.html?page="
	start_urls = []
	for i in range(1,426):
		start_urls.append(start_url + '%s' % (i))
		
	def parse(self, response):
		#pass
		items = []
		url_list = response.xpath('//div[@class="l-info"]//div[@class="l-result"]//ul[@class="infos clearfix"]//div[@class="i-tits"]//a/@href').extract()
		for url in url_list:
			if "/project/details" in url:
				item = UrlJdzcItem()
				item['url_list'] = url
				items.append(item)
			else:
				pass
		return items
		#url_len = len(url_list)
		#for url in range(0,url_len):
		#	item = UrlJdzcItem()
		#	item['url_list'] = url_list[url]
		#	items.append(item)
		#return items
