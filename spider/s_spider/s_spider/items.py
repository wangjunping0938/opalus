# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class SSpiderItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    #pass
	#网址			String
	url = scrapy.Field()
	#站点来源		Integer
	site_from = scrapy.Field()
	#销售模式		Integer	,1=正常销售,2=众筹,3=抢购
	site_type = scrapy.Field()
	#产品编号		String
	out_number = scrapy.Field()
	#名称			String
	title = scrapy.Field()
	#子名称			String
	sub_title = scrapy.Field()
	#简述			String
	resume = scrapy.Field()
	#内容			String
	content = scrapy.Field()
	#品牌名			String
	brand_name = scrapy.Field()
	#品牌联系方式	String
	brand_contact = scrapy.Field()
	#品牌地址		String
	brand_address = scrapy.Field()
	#分类			String	多个用","分割
	category_tags = scrapy.Field()
	#标签			String	多个用","分割
	tags = scrapy.Field()
	#产品封面图		String
	cover_url = scrapy.Field()
	#原产品封面图地址	String
	o_cover_url = scrapy.Field()
	#评分			float
	rate = scrapy.Field()
	#成本价			float
	cost_price = scrapy.Field()
	#销售价			float
	sale_price = scrapy.Field()
	#销售总额		float
	total_price = scrapy.Field()
	#喜欢/点赞数	Integer
	love_count = scrapy.Field()
	#收藏/订阅数	Integer
	favorite_count = scrapy.Field()
	#评论数			Integer
	comment_count = scrapy.Field()
	#销售数量		Integer
	sale_count = scrapy.Field()
	#浏览数			Integer
	view_count = scrapy.Field()
	#支持人数		Integer
	support_count = scrapy.Field()
	#众筹发起人/公司	String
	info_name = scrapy.Field()
	#众筹标准			String
	info_demand = scrapy.Field()
	#众筹发起人/公司地址	String
	info_address = scrapy.Field()
	#众筹联系电话		String
	info_contact = scrapy.Field()
	#工作时间			String
	info_time = scrapy.Field()
	#众筹进度			float	百分比/100
	info_rate = scrapy.Field()
	#众筹剩余时间		String
	info_last_time = scrapy.Field()
