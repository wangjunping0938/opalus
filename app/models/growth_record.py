# -*- coding:utf-8 -*-
import datetime
from . import db
from .base import Base

# 增长量记录表- growth_record
class GrowthRecord(Base):

    meta = {
        'collection': 'growth_record',
        'ordering': ['-created_at'],
        'strict': True,
        'id_field': '_id'
    }

    _id = db.StringField()
    target_id = db.IntField(required=True)    # 产品ID
    day = db.IntField(required=True)    # 天;格式: 20170501
    url = db.StringField(max_length=50) # 网址
    kind = db.IntField(default=1)    # 类型: 1.产品；2.--

    site_from = db.IntField(default=0)    # 站点来源
    site_type = db.IntField(default=0)    # 站点模式 1.销售；2.众筹；3.--

    status = db.IntField(default=1)    # 状态: 0.禁用；1.启用
    deleted = db.IntField(default=0)    # 是否软删除

    total_price = db.FloatField(default=0)    # 销售总额

    ## 数量
    love_count = db.IntField(default=0)    # 喜欢/点赞数
    favorite_count = db.IntField(default=0)    # 收藏/订阅数
    comment_count = db.IntField(default=0)    # 评论数
    sale_count = db.IntField(default=0)    # 销售数
    view_count = db.IntField(default=0)    # 浏览数
    support_count = db.IntField(default=0)    # 支持人数
    rate = db.FloatField(default=0)    # 评分
    grab_count = db.IntField(default=1)    # 抓取次数

    cost_price = db.FloatField(default=0)    # 成本价
    sale_price = db.FloatField(default=0)    # 销售单价

    created_at = db.DateTimeField()
    updated_at = db.DateTimeField(default=datetime.datetime.now)

    def mark_delete(self):
        return super(GrowthRecord, self).update(deleted=1)

    def __unicode__(self):
        return self.name

