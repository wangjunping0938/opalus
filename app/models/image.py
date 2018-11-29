# -*- coding:utf-8 -*-
import os
import datetime
import time
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
    title = db.StringField(max_length=100, default='') # 标题
    name = db.StringField(max_length=100, default='') # 文件名称
    channel = db.StringField(max_length=10, default='') # 渠道
    img_url = db.StringField(max_length=500, default='') # 图片地址
    url = db.StringField(max_length=500, default='') # 原文地址
    path = db.StringField(max_length=100, default='') # 七牛路径
    local_name = db.StringField(max_length=50, default='') # 本地文件名称
    local_path = db.StringField(max_length=100, default='') # 本地文件路径
    ext = db.StringField(max_length=10, default='') # 扩展名
    tags = db.ListField() # 标签
    color_tags = db.ListField() # 颜色标签
    brand_tags = db.ListField() # 品牌标签
    material_tags = db.ListField() # 材质
    style_tags = db.ListField() # 风格
    technique_tags = db.ListField() # 工艺
    other_tags = db.ListField() # 其它
    designer = db.StringField(max_length=200, default='') # 设计师
    company = db.StringField(max_length=100, default='') # 公司
    user_id = db.IntField(default=0)    # 用户ID
    kind = db.IntField(default=1)    # 类型:
    brand_id = db.IntField(default=0)    # 品牌ID
    prize_id = db.IntField(default=0)   # 奖项ID
    prize = db.StringField(max_length=50, default='')  # 奖项名称
    prize_level = db.StringField(max_length=50, default='')  # 奖项级别
    prize_time = db.StringField(max_length=50, default='')  # 奖项时间
    category_id = db.IntField(default=0)    # 分类ID
    stick = db.IntField(default=0)  # 是否推荐：0.否；1.是；
    stick_on = db.IntField(default=0)  # 推荐时间；
    status = db.IntField(default=1)    # 状态: 0.禁用；1.启用
    remark = db.StringField(max_length=500, default='')  # 描述
    info = db.StringField(max_length=10000, default='')  # 其它json串
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
        if self.color_tags and not isinstance(self.color_tags, list):
            self.color_tags = self.color_tags.split(',')
        if self.brand_tags and not isinstance(self.brand_tags, list):
            self.brand_tags = self.brand_tags.split(',')
        if self.material_tags and not isinstance(self.material_tags, list):
            self.material_tags = self.material_tags.split(',')
        if self.style_tags and not isinstance(self.style_tags, list):
            self.style_tags = self.style_tags.split(',')
        if self.technique_tags and not isinstance(self.technique_tags, list):
            self.technique_tags = self.technique_tags.split(',')
        if self.other_tags and not isinstance(self.other_tags, list):
            self.other_tags = self.other_tags.split(',')
        return super(Image, self).save(*args, **kwargs)


    def update(self, *args, **kwargs):
        if 'tags' in kwargs.keys() and not isinstance(kwargs['tags'], list):
            kwargs['tags'] = kwargs['tags'].split(',')
        if 'color_tags' in kwargs.keys() and not isinstance(kwargs['color_tags'], list):
            kwargs['color_tags'] = kwargs['color_tags'].split(',')
        if 'brand_tags' in kwargs.keys() and not isinstance(kwargs['brand_tags'], list):
            kwargs['brand_tags'] = kwargs['brand_tags'].split(',')
        if 'material_tags' in kwargs.keys() and not isinstance(kwargs['material_tags'], list):
            kwargs['material_tags'] = kwargs['material_tags'].split(',')
        if 'style_tags' in kwargs.keys() and not isinstance(kwargs['style_tags'], list):
            kwargs['style_tags'] = kwargs['style_tags'].split(',')
        if 'technique_tags' in kwargs.keys() and not isinstance(kwargs['technique_tags'], list):
            kwargs['technique_tags'] = kwargs['technique_tags'].split(',')
        if 'other_tags' in kwargs.keys() and not isinstance(kwargs['other_tags'], list):
            kwargs['other_tags'] = kwargs['other_tags'].split(',')
        return super(Image, self).update(*args, **kwargs)

    # 推荐
    def mark_stick(self, evt=1):
        evt = int(evt)
        if evt == 1:
            return super(Image, self).update(stick=1, stick_on=int(time.time()))
        else:
            return super(Image, self).update(stick=0)

    # 标记删除
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

