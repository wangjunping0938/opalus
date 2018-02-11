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

    def __unicode__(self):
        return self.name

