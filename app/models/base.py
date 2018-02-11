# -*- coding:utf-8 -*-
import datetime
from flask import current_app

from app.models import db

class Base(db.Document):

    meta = {
        'allow_inheritance': False,
        'abstract': True
    }

    def save(self, *args, **kwargs):
        meta = self._meta
        if not self.created_at:
            self.created_at = datetime.datetime.now()
        if not self.updated_at:
            self.updated_at = datetime.datetime.now()

        if 'increase_key' in meta and meta['increase_key'] == True:
            inc_key = '%s_%s' % (meta['collection'], 'id')
            #current_app.logger.debug(inc_key)
            # ID 自增
            sequence = Sequence._get_collection()
            sequence = sequence.find_one_and_update({'name':inc_key}, {'$inc':{'val':1}}, upsert=True)
            self._id = sequence['val']

        return super(Base, self).save(*args, **kwargs)

    def update(self, *args, **kwargs):
        kwargs['updated_at'] = datetime.datetime.now()
        self.updated_at = datetime.datetime.now()
        #current_app.logger.debug('aa')
        return super(Base, self).update(*args, **kwargs)


# 主键自增表
class Sequence(db.Document):
    name = db.StringField(max_length=10, required=True, unique=True)
    val = db.IntField()



