# -*- coding:utf-8 -*-
import datetime
from werkzeug import security
from app.models import db, current_app
from .base import Base


class DesignCase(Base):

    meta = {
        'collection': 'design_case',
        'ordering': ['-created_at'],
        'strict': True
    }

    _id = db.StringField()
    title = db.StringField(min_value=4, max_value=50, required=True)
    description = db.StringField(max_value=1000, default='')
    content = db.StringField(max_value=50000, default='')
    cover_id = db.StringField(max_value=20, default='')
    cover_url = db.StringField(max_value=100, default='')
    images = db.StringField(max_value=1000, default='')
    prize_label = db.StringField(max_value=30, default='')
    type = db.IntField(default=1) # 类型: 1.公司奖项案例
    target_id = db.StringField(default='')

    tags = db.ListField()   # 标签
    status = db.IntField(default=1)
    deleted = db.IntField(default=0) # 软删除

    created_at = db.DateTimeField()
    updated_at = db.DateTimeField(default=datetime.datetime.now)


    def save(self, *args, **kwargs):
        if self.tags and not isinstance(self.tags, list):
            self.tags = self.tags.split(',')
        else:
            self.tags = []

        return super(DesignCase, self).save(*args, **kwargs)


    def update(self, *args, **kwargs):
        if 'tags' in kwargs.keys() and not isinstance(kwargs['tags'], list):
            kwargs['tags'] = kwargs['tags'].split(',')

        return super(DesignCase, self).update(*args, **kwargs)


    def mark_delete(self):
        return super(DesignCase, self).update(deleted=1)
