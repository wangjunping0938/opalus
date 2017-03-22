# -*- coding:utf-8 -*-
import datetime
from . import db

# 订单表- order
class Order(db.Document):

    meta = {
        'collection': 'order',
        'ordering': ['-created_at'],
        'strict': True,
        'id_field': '_id'
    }

    _id = db.StringField()
    mark = db.StringField(max_length=20, required=True, unique=True)    # 唯一标识
    name = db.StringField(max_length=30, required=True) # 名称
    user_id = db.IntField(default=0)    # 用户ID
    kind = db.IntField(default=1)    # 类型:
    status = db.IntField(default=1)    # 状态: 0.禁用；1.启用
    code = db.StringField() # 代码块
    content = db.StringField()  # 内容
    remark = db.StringField(max_length=50, required=True)   # 备注
    deleted = db.IntField(default=0)    # 是否软删除

    created_at = db.DateTimeField()
    updated_at = db.DateTimeField(default=datetime.datetime.now)


    def save(self, *args, **kwargs):
        if not self.created_at:
            self.created_at = datetime.datetime.now()
        if not self.updated_at:
            self.updated_at = datetime.datetime.now()
        return super(Order, self).save(*args, **kwargs)


    def update(self, *args, **kwargs):
        kwargs['updated_at'] = datetime.datetime.now()
        self.updated_at = datetime.datetime.now()
        return super(Order, self).update(*args, **kwargs)

    def mark_delete(self):
        return super(Order, self).update(deleted=1)

    def __unicode__(self):
        return self.name

