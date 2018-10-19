# -*- coding:utf-8 -*-
import datetime
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
    title = db.StringField(max_length=50) # 标题
    name = db.StringField(max_length=50) # 文件名称
    url = db.StringField(max_length=500) # 抓取地址
    img_url = db.StringField(max_length=500) # 图片地址
    local_name = db.StringField(max_length=50) # 本地文件名称
    local_path = db.StringField(max_length=100) # 本地文件路径
    ext = db.StringField(max_length=10) # 扩展名
    user_id = db.IntField(default=0)    # 用户ID
    kind = db.IntField(default=1)    # 类型:
    brand_id = db.IntField(default=0)    # 品牌ID
    category_id = db.IntField(default=0)    # 分类ID
    status = db.IntField(default=1)    # 状态: 0.禁用；1.启用
    remark = db.StringField(max_length=500)  # 描述
    deleted = db.IntField(default=0)    # 是否软删除

    created_at = db.DateTimeField()
    updated_at = db.DateTimeField(default=datetime.datetime.now)

    def mark_delete(self):
        return super(Image, self).update(deleted=1)

    def __unicode__(self):
        return self.name

