# -*- coding:utf-8 -*-
import datetime
from .base import *

class Session(db.Document):

    user_id = db.IntField()
    # 是否登录
    is_login = db.IntField(default=1)
    # 登录次数
    serial_no = db.IntField(default=1)
    # 设备信息
    agent = db.StringField(max_value=100)
    ip = db.StringField(max_value=20)
    last_time = db.DateTimeField()

    created_at = db.DateTimeField()
    updated_at = db.DateTimeField(default=datetime.datetime.now)

    #meta = {'collection': 'session'}

    def save(self, *args, **kwargs):
        if not self.created_at:
            self.created_at = datetime.datetime.now()
        if not self.updated_at:
            self.updated_at = datetime.datetime.now()
        return super(Session, self).save(*args, **kwargs)

    def update(self, *args, **kwargs):
        kwargs['updated_at'] = datetime.datetime.now()
        self.updated_at = datetime.datetime.now()
        return super(Session, self).update(*args, **kwargs)

    def __unicode__(self):
        return self.name

