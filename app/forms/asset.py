# coding: utf-8

from wtforms import TextAreaField, StringField, IntegerField
from wtforms.validators import DataRequired, Length, EqualTo, NumberRange
from flask_wtf import FlaskForm
from bson import ObjectId
from ..models.asset import Asset

class SaveForm(FlaskForm):
    id = StringField()

    name = StringField('名称', validators=[DataRequired(message="名称不能为空"), Length(min=2, max=30, message="长度大于2小于30个字符")])
    path = StringField()
    mime = StringField()
    domain = StringField()
    target_id = StringField()
    size = IntegerField()
    width = IntegerField()
    height = IntegerField()
    kind = IntegerField()
    remark = StringField()
    user_id = IntegerField()

    def update(self):
        id = self.data['id']
        item = Asset.objects(_id=ObjectId(id)).first()
        if not item:
            raise ValueError('内容不存在!')
        data = self.data
        data.pop('id')
        data.pop('user_id')
        #data.pop('csrf_token')
        ok = item.update(**data)
        return ok

    def save(self, **param):
        data = self.data;
        data['user_id'] = param['user_id']
        data.pop('id')
        item = Asset(**data)
        item.save()
        return item

class setStatus(FlaskForm):
    id = StringField()
    status = IntegerField()

    def set_status(self):
        id = self.data['id']
        item = Asset.objects(_id=ObjectId(id)).first()
        if not item:
            raise ValueError('内容不存在!')
        data = {}
        data['status'] = self.data['status']
        ok = item.update(**data)
        return ok
