# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class JdzcItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
	#pass
	#网址
	url = scrapy.Field()			#string	Not_Null
	#站点来源
	site_from = scrapy.Field()		#integer 	Not_Null
	#销售模式
	site_type = scrapy.Field()		#integer	Not_Null
	#产品编号		
	out_number = scrapy.Field()		#string
	#名称
	title = scrapy.Field()			#string	Not_Null
	#子名称
	sub_title = scrapy.Field()		#string
	#简述
	resume = scrapy.Field()			#string  
	#内容
	content = scrapy.Field()		#string
	#品牌名
	brand_name = scrapy.Field()		#string
	#品牌联系方式
	brand_contact = scrapy.Field()	#string
	#品牌地址
	brand_address = scrapy.Field()	#string
	#分类
	category_tags = scrapy.Field()	#string	多个用逗号做连接符号
	#标签
	tags = scrapy.Field()			#string	多个用逗号分隔
	#产品封面图
	cover_url = scrapy.Field()		#string
	#评分
	rate = scrapy.Field()			#float
	#成本价
	cost_price = scrapy.Field()		#float
	#销售价
	sale_price = scrapy.Field()		#float
	#销售总额
	total_price = scrapy.Field()	#float
	#喜欢/点赞数
	love_count = scrapy.Field()		#integer
	#收藏/订阅数
	favorite_count = scrapy.Field()	#integer
	#评论数
	comment_count = scrapy.Field()	#integer
	#销售数量
	sale_count = scrapy.Field()		#integer
	#浏览数
	view_count = scrapy.Field()		#integer
	#支持人数
	support_count = scrapy.Field()	#integer
	#众筹发起人/公司
	info_name = scrapy.Field()		#string
	#众筹标准
	info_demand = scrapy.Field()	#string
	#众筹发起人/公司地址
	info_address = scrapy.Field()	#string
	#众筹联系电话
	info_contact = scrapy.Field()	#string
	#工作时间
	info_time = scrapy.Field()		#string
	#众筹进度
	info_rate = scrapy.Field()		#float
	#众筹剩余时间
	info_last_time = scrapy.Field()	#string
	#原产品封面图地址
	o_cover_url = scrapy.Field()	#string
	URL = scrapy.Field()
