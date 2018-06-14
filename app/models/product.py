# -*- coding:utf-8 -*-
import datetime
from . import db
from .base import Base
from app.models.base import *

# 产品表- product
class Product(Base):

    meta = {
        'increase_key': True,
        'collection': 'product',
        'ordering': ['-created_at'],
        'strict': True 
    }

    _id = db.IntField(primary_key=True, required=True)
    out_number = db.StringField() # 站外编号(sku)
    title = db.StringField(max_length=30) # 名称
    sub_title = db.StringField(max_length=30) # 子名称
    resume = db.StringField(max_length=1000) # 简述
    content = db.StringField() # 内容
    #brand = db.EmbeddedDocumentField(Brand) # 品牌{name, address, contact}
    brand = db.DictField()
    url = db.StringField() # 原文链接
    tags = db.ListField() # 标签
    cover_url = db.StringField(max_length=200) # 封面
    o_cover_url = db.StringField(max_length=200) # 原封面地址
    kind = db.IntField(default=1)    # 类型:
    category_id = db.IntField(default=0)    # 分类ID
    category_tags = db.ListField() # 分类标签
    site_from = db.IntField(default=0)    # 来源: 
    site_type = db.IntField(default=1)    # 销售模式：1.正常销售；2.众筹；3.--
    rate = db.FloatField(default=0)    # 评分
    status = db.IntField(default=1)    # 状态: 0.禁用；1.启用
    remark = db.StringField()   # 备注
    deleted = db.IntField(default=0)    # 是否软删除
    last_grab_at = db.DateTimeField() # 最后一次抓取时间
    attrbute = db.DictField() # 产品参数信息
    info = db.DictField() # 记录关于众筹信息{name, demand, rate, address, contact, time, last_time}

    cost_price = db.FloatField(default=0)    # 成本价
    sale_price = db.FloatField()    # 销售单价
    total_price = db.FloatField()    # 销售总额

    ## 数量
    love_count = db.IntField(default=0)    # 喜欢/点赞数
    favorite_count = db.IntField(default=0)    # 收藏/订阅数
    comment_count = db.IntField(default=0)    # 评论数
    sale_count = db.IntField(default=0)    # 销售数
    view_count = db.IntField(default=0)    # 浏览数
    support_count = db.IntField(default=0)    # 支持人数
    grab_count = db.IntField(default=1)    # 抓取次数

    created_at = db.DateTimeField()
    updated_at = db.DateTimeField(default=datetime.datetime.now)


    def save(self, *args, **kwargs):
        if self.tags and not isinstance(self.tags, list):
            self.tags = self.tags.split(',')
        if self.category_tags and not isinstance(self.category_tags, list):
            self.category_tags = self.category_tags.split(',')
        return super(Product, self).save(*args, **kwargs)


    def update(self, *args, **kwargs):
        if 'tags' in kwargs.keys() and not isinstance(kwargs['tags'], list):
            kwargs['tags'] = kwargs['tags'].split(',')
        if 'category_tags' in kwargs.keys() and not isinstance(kwargs['category_tags'], list):
            kwargs['category_tags'] = kwargs['category_tags'].split(',')

        return super(Product, self).update(*args, **kwargs)

    def mark_delete(self):
        return super(Product, self).update(deleted=1)

    def __unicode__(self):
        return self.name

