# coding: utf-8
from wtforms import TextAreaField, StringField, IntegerField
from wtforms.validators import DataRequired, Length, EqualTo, NumberRange
from flask_wtf import FlaskForm
from bson import ObjectId

#from .base import BaseForm
from ..models.tag import Tag
#from ..helpers import *

class SaveForm(FlaskForm):
    id = StringField()
    name = StringField('名称', validators=[DataRequired(message="不能为空"), Length(max=30, message="长度小于30")])
    total_count = IntegerField()
    remark = StringField()
    kind = IntegerField()
    pid = IntegerField()
    cid = IntegerField()
    user_id = IntegerField()


    def update(self):
        id = self.data['id']
        item = Tag.objects(_id=ObjectId(id)).first()
        if not item:
            raise ValueError('内容不存在!')

        data = {}

        data['mark'] = self.data['mark']
        data['name'] = self.data['name']
        data['code'] = self.data['code']
        data['content'] = self.data['content']
        data['remark'] = self.data['remark']
        data['kind'] = self.data['kind']
        data['role'] = self.data['role']

        ok = item.update(**data)
        return ok

    def save(self, **param):
        data = self.data;

        data['user_id'] = param['user_id']
        data.pop('id')
        item = Tag(**data)
        item.save()
        return item

class setStatus(FlaskForm):
    id = StringField()
    status = IntegerField()

    def set_status(self):
        id = self.data['id']
        item = Tag.objects(_id=ObjectId(id)).first()
        if not item:
            raise ValueError('内容不存在!')
        data = {}
        data['status'] = self.data['status']
        ok = item.update(**data)
        return ok

