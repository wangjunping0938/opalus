# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class SspiderItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    #pass
	url=scrapy.Field()		#url地址(string)
	site_from=scrapy.Field()		#url来源(integer)
	site_type=scrapy.Field()		#销售模式(string)
	out_number=scrapy.Field()		#产品编号(interge)
	title=scrapy.Field()		#标题
	ub_title = scrapy.Field()		#子名称
