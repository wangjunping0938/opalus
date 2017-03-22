# -*- coding:utf-8 -*-

from app.models import db

class Base(object):

    meta = {'allow_inheritance': True}


class Sequence(db.Document):
    name = db.StringField(max_length=10, required=True, unique=True)
    val = db.IntField()



