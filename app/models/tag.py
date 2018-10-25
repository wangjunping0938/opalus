# -*- coding:utf-8 -*-
import datetime
from . import db
from .base import Base

# 标签表- tag
class Tag(Base):

    meta = {
        'collection': 'tag',
        'ordering': ['-created_at'],
        'strict': True,
        'id_field': '_id'
    }

    _id = db.StringField()
    name = db.StringField(max_length=30, required=True, unique=True) # 名称
    user_id = db.IntField(default=0)    # 用户ID
    kind = db.IntField(default=1)    # 类型:
    pid = db.IntField(default=0)    # 父分类:
    cid = db.IntField(default=0)    # 子分类:
    status = db.IntField(default=1)    # 状态: 0.禁用；1.启用
    total_count = db.IntField(default=0) # 总数量
    remark = db.StringField(max_length=50, default='')   # 备注
    deleted = db.IntField(default=0)    # 是否软删除

    created_at = db.DateTimeField()
    updated_at = db.DateTimeField(default=datetime.datetime.now)


    def save(self, *args, **kwargs):
        return super(Tag, self).save(*args, **kwargs)


    def update(self, *args, **kwargs):
        return super(Tag, self).update(*args, **kwargs)

    def mark_delete(self):
        return super(Tag, self).update(deleted=1)

    def __unicode__(self):
        return self.name

