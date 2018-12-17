# -*- coding:utf-8 -*-
import datetime
import re

from . import db, current_app
from .base import Base


class Color(Base):
    meta = {
        'collection': 'color',
        'ordering': ['-created_at'],
        'id_field': '_id',
        'strict': True
    }

    _id = db.StringField()
    rgb = db.StringField(max_value=30, default='')  # rgb值
    hex = db.StringField(max_value=30, default='')  # 十六进制值
    pantone = db.StringField(max_value=30, default='')  # 潘通色卡号
    cmyk = db.StringField(max_value=30, default='')  # CMYK印刷色值
    user_id = db.IntField(default=0)
    status = db.IntField(default=1)  # 是否禁用：0.是；1.否；
    deleted = db.IntField(default=0)  # 软删除
    remark = db.StringField(max_value=5000, default='') # 备注
    created_at = db.DateTimeField()
    updated_at = db.DateTimeField()

    def mark_delete(self):
        return super(Color, self).update(deleted=1)

    def __unicode__(self):
        return str(self._id)
