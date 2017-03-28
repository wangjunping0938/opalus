# coding: utf-8
from wtforms import TextAreaField, StringField, IntegerField
from wtforms.validators import DataRequired, Length, EqualTo, NumberRange
from flask_wtf import FlaskForm
import bson

#from .base import BaseForm
from ..models.order import Order
from ..helpers import *

class SaveForm(FlaskForm):
    id = StringField()
    mark = StringField('唯一标识', validators=[DataRequired(message="唯一标识不能为空"), Length(min=4, max=16, message="长度大于4小于16")])
    name = StringField('名称', validators=[DataRequired(message="名称不能为空")])
    code = StringField()
    content = StringField()
    remark = StringField()
    kind = IntegerField()
    status = IntegerField()
    user_id = IntegerField()

    def update_one(self):
        id = self.data['id']
        order = Order.objects(_id=bson.objectid.ObjectId(id)).first()
        if not order:
            raise ValueError('内容不存在!')
        data = {}

        data['mark'] = self.data['mark']
        data['name'] = self.data['name']
        data['code'] = self.data['code']
        data['content'] = self.data['content']
        data['remark'] = self.data['remark']
        data['kind'] = self.data['kind']
        data['status'] = self.data['status']

        ok = order.update(**data)
        return ok

    def save(self, **param):
        data = self.data;
        data['user_id'] = param['user_id']
        data.pop('id')
        order = Order(**data)
        order.save()
        return order
