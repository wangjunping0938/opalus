# coding: utf-8

from wtforms import TextAreaField, StringField, IntegerField
from wtforms.validators import DataRequired, Length, EqualTo, NumberRange
from flask_wtf import FlaskForm

#from .base import BaseForm
from ..models.category import Category
from ..helpers import *

class SaveForm(FlaskForm):
    id = StringField()

    mark = StringField('标识', validators=[DataRequired(message="标识不能为空"), Length(min=4, max=16, message="长度大于4小于16")])
    name = StringField('名称', validators=[DataRequired(message="名称不能为空"), Length(min=4, max=16, message="长度大于4小于16")])
    kind = IntegerField('类型', validators=[NumberRange(min=1, max=8, message="类型设置不正确")])
    status = IntegerField('状态', validators=[NumberRange(min=0, max=5, message="状态设置不正确")])
    remark = StringField()
    user_id = IntegerField()
    pid = IntegerField()
    cid = IntegerField()

    def update(self):
        id = self.data['id']
        category = Category.objects(_id=id).first()
        if not category:
            raise ValueError('分类不存在!')
        data = self.data
        data.pop('id')
        data.pop('user_id')
        data.pop('csrf_token')
        ok = category.update(**data)
        return ok

    def save(self, **param):
        data = self.data;
        data['user_id'] = param['user_id']
        data.pop('csrf_token')
        data.pop('id')
        category = Category(**data)
        category.save()
        return category
