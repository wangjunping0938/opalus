# -*- coding: utf-8 -*-
import scrapy


class TbzcSpiderSpider(scrapy.Spider):
    name = "tbzc_spider"
    allowed_domains = ["https://izhongchou.taobao.com"]
    start_urls = ['http://https://izhongchou.taobao.com/']

    def parse(self, response):
        pass
