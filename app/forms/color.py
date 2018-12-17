# coding: utf-8
from wtforms import TextAreaField, StringField, IntegerField
from wtforms.validators import DataRequired, Length, EqualTo, NumberRange
from flask_wtf import FlaskForm
from bson import ObjectId
from app.helpers.role import check_role

#from .base import BaseForm
from ..models.color import Color
#from ..helpers import *

class SaveForm(FlaskForm):
    id = StringField()
    rgb = StringField('rgb', validators=[Length(max=30, message="长度小于30")])
    hex = StringField('hex', validators=[Length(max=30, message="长度小于30")])
    cmyk = StringField()
    pantone = StringField()
    remark = StringField()
    user_id = IntegerField()

    def update(self):
        id = self.data['id']
        item = Color.objects(_id=ObjectId(id)).first()
        if not item:
            raise ValueError('内容不存在!')

        data = {}
        data = self.data
        data.pop('id')
        if 'user_id' in data:
            data.pop('user_id')
        ok = item.update(**data)
        return ok

    def save(self, **param):
        data = self.data;
        data['user_id'] = param['user_id']
        data.pop('id')
        item = Color(**data)
        item.save()
        return item

class setStatus(FlaskForm):
    id = StringField()
    status = IntegerField()

    def set_status(self):
        id = self.data['id']
        item = Color.objects(_id=ObjectId(id)).first()
        if not item:
            raise ValueError('内容不存在!')
        data = {}
        data['status'] = self.data['status']
        ok = item.update(**data)
        return ok

