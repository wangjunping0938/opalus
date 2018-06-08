# -*- coding:utf-8 -*-
import datetime
from . import db
from .base import Base

# 配置表- block
class Block(Base):

    meta = {
        'collection': 'block',
        'ordering': ['-created_at'],
        'strict': True,
        'id_field': '_id'
    }

    _id = db.StringField()
    mark = db.StringField(max_length=30, required=True, unique=True)    # 唯一标识
    name = db.StringField(max_length=30, required=True) # 名称
    user_id = db.IntField(default=0)    # 用户ID
    kind = db.IntField(default=1)    # 类型:
    status = db.IntField(default=1)    # 状态: 0.禁用；1.启用
    code = db.StringField() # 代码块
    content = db.StringField()  # 内容
    remark = db.StringField(max_length=50, required=True)   # 备注
    role = db.IntField(default=0) # 权重：0.基本；1.编辑；5.超级管理员
    deleted = db.IntField(default=0)    # 是否软删除

    created_at = db.DateTimeField()
    updated_at = db.DateTimeField(default=datetime.datetime.now)


    def save(self, *args, **kwargs):
        return super(Block, self).save(*args, **kwargs)


    def update(self, *args, **kwargs):
        return super(Block, self).update(*args, **kwargs)

    def mark_delete(self):
        return super(Block, self).update(deleted=1)

    def __unicode__(self):
        return self.name

