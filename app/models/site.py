# -*- coding:utf-8 -*-
#import datetime
from . import db
from .base import Base

# 网站管理表- site
class Site(Base):

    meta = {
        'collection': 'site',
        'ordering': ['-created_at'],
        'strict': True,
        'id_field': '_id'
    }

    _id = db.StringField()
    mark = db.StringField(max_length=20, required=True, unique=True)    # 唯一标识
    name = db.StringField(max_length=20) # 名称
    url = db.StringField(max_length=200) # 网址
    user_id = db.IntField(default=0)    # 用户ID
    kind = db.IntField(default=1)    # 类型:
    category_id = db.IntField(default=0)    # 分类
    site_from = db.IntField(default=0)    # 站点来源
    site_type = db.IntField(default=0)    # 站点模式 1.销售；2.众筹；3.--
    code = db.StringField(default='') # 规则块
    remark = db.StringField(max_length=200,default='')   # 备注

    last_url = db.StringField(max_length=200,default='') # 最后一次抓取网址
    last_on = db.DateTimeField()    # 最后一次抓取时间

    status = db.IntField(default=1)    # 状态: 0.禁用；1.启用
    deleted = db.IntField(default=0)    # 是否软删除

    created_at = db.DateTimeField()
    updated_at = db.DateTimeField()


    def mark_delete(self):
        return super(Site, self).update(deleted=1)

    def __unicode__(self):
        return self.name

