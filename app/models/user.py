# -*- coding:utf-8 -*-
import datetime
from werkzeug import security
from . import db, current_app
from .base import Base
from app.helpers.common import gen_sha1


class User(Base):

    meta = {
        'increase_key': True,
        'collection': 'user',
        'ordering': ['-created_at'],
        'strict': True
    }

    _id = db.IntField(primary_key=True, required=True)
    account = db.StringField(min_value=4, max_value=20, required=True, unique=True)
    phone = db.StringField(max_value=20, default='')
    email = db.StringField(max_value=50, default='')
    password = db.StringField(max_value=20)
    type = db.IntField(default=1)
    role_id = db.IntField(default=1) # 权限: 1.用户；2.编辑；5.管理员；8.系统管理员；
    status = db.IntField(default=1) # 状态：0.禁用；1.待审核；5.激活；
    deleted = db.IntField(default=0) # 软删除
    token = db.StringField(max_value=20, required=True, unique=True)
    profile = db.DictField() # 记录个人信息{realname, sex, address, position}

    created_at = db.DateTimeField()
    updated_at = db.DateTimeField(default=datetime.datetime.now)


    def save(self, *args, **kwargs):
        self.password = self.create_password(self.password, self.account)
        self.account = self.account.lower()
        self.token = self.create_token(16)
        return super(User, self).save(*args, **kwargs)

    def __unicode__(self):
        return self.name

    @staticmethod
    def create_password(raw, account):
        passwd = '%s:%s:%s' % (raw, current_app.config['PASSWORD_SECRET'], account)
        return gen_sha1(passwd)

    @staticmethod
    def create_token(length=16):
        return security.gen_salt(length)

    def check_password(self, raw, account):
        passwd = '%s:%s:%s' % (raw, current_app.config['PASSWORD_SECRET'], account)
        return self.password == gen_sha1(passwd)

    def change_password(self, raw):
        self.password = self.create_password(raw)
        self.token = self.create_token()
        return self

