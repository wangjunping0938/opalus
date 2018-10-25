# -*- coding:utf-8 -*-
import os
import datetime
from flask import current_app
from . import db
from .base import Base

# 图片素材表- image
class Image(Base):

    meta = {
        'collection': 'image',
        'ordering': ['-created_at'],
        'strict': True,
        'id_field': '_id'
    }

    _id = db.StringField()
    title = db.StringField(max_length=50, default='') # 标题
    name = db.StringField(max_length=50, default='') # 文件名称
    channel = db.StringField(max_length=10, default='') # 渠道
    img_url = db.StringField(max_length=500, default='') # 图片地址
    path = db.StringField(max_length=100, default='') # 七牛路径
    local_name = db.StringField(max_length=50, default='') # 本地文件名称
    local_path = db.StringField(max_length=100, default='') # 本地文件路径
    ext = db.StringField(max_length=10, default='') # 扩展名
    tags = db.ListField() # 标签
    user_id = db.IntField(default=0)    # 用户ID
    kind = db.IntField(default=1)    # 类型:
    brand_id = db.IntField(default=0)    # 品牌ID
    category_id = db.IntField(default=0)    # 分类ID
    status = db.IntField(default=1)    # 状态: 0.禁用；1.启用
    remark = db.StringField(max_length=500, default='')  # 描述
    evt = db.IntField(default=1)    # 来源：1.默认
    deleted = db.IntField(default=0)    # 是否软删除

    created_at = db.DateTimeField()
    updated_at = db.DateTimeField(default=datetime.datetime.now)

    # 获取七牛路径
    def get_thumb_path(self):
        asset_url = current_app.config['ASSET_URL']
        path = self.path
        if not path:
            return None

        row = {
            'sm': os.path.join(asset_url, path + '-sm'),
            'mi': os.path.join(asset_url, path + '-mi'),
            'bi': os.path.join(asset_url, path + '-bi'),
            'avs': os.path.join(asset_url, path + '-avs'),
            'avm': os.path.join(asset_url, path + '-avm'),
            'avb': os.path.join(asset_url, path + '-avb'),
        }
        return row

    def save(self, *args, **kwargs):
        if self.tags and not isinstance(self.tags, list):
            self.tags = self.tags.split(',')
        return super(Image, self).save(*args, **kwargs)


    def update(self, *args, **kwargs):
        if 'tags' in kwargs.keys() and not isinstance(kwargs['tags'], list):
            kwargs['tags'] = kwargs['tags'].split(',')
        return super(Image, self).update(*args, **kwargs)

    def mark_delete(self):
        return super(Image, self).update(deleted=1)

    # 标记恢复
    def mark_recovery(self):
        ok = super(Image, self).update(deleted=0)
        return ok

    # 彻底删除，同时删除源文件
    def delete(self):
        super(Image, self).delete()
        # 删除源文件

    def __unicode__(self):
        return self.name

