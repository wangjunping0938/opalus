# coding: utf-8
from wtforms import TextAreaField, StringField, IntegerField, DateTimeField
from wtforms.validators import DataRequired, Length, EqualTo, NumberRange
from flask_wtf import FlaskForm
import bson

#from .base import BaseForm
from ..models.site import Site
from ..helpers import *

class SaveForm(FlaskForm):
    id = StringField()
    mark = StringField('唯一标识', validators=[DataRequired(message="唯一标识不能为空"), Length(min=4, max=16, message="长度大于4小于16")])
    name = StringField('名称', validators=[DataRequired(message="名称不能为空")])
    url = StringField('网址', validators=[DataRequired(message="网址不能为空")])
    last_url = StringField()
    code = StringField()
    remark = StringField()
    kind = IntegerField()
    category_id = IntegerField()
    user_id = IntegerField()
    site_from = IntegerField()
    site_type = IntegerField()
    last_url = StringField() # 最后一次抓取网址
    last_on = DateTimeField()    # 最后一次抓取时间

    def update(self):
        id = self.data['id']
        site = Site.objects(_id=bson.objectid.ObjectId(id)).first()
        if not site:
            raise ValueError('内容不存在!')
        data = {}

        data['mark'] = self.data['mark']
        data['name'] = self.data['name']
        data['code'] = self.data['code']
        data['url'] = self.data['url']
        data['last_url'] = self.data['last_url']
        data['category_id'] = self.data['category_id']
        data['site_from'] = self.data['site_from']
        data['site_type'] = self.data['site_type']
        data['remark'] = self.data['remark']
        data['kind'] = self.data['kind']

        ok = site.update(**data)
        return ok

    def save(self, **param):
        data = self.data;
        data['user_id'] = param['user_id']
        data.pop('id')
        site = Site(**data)
        site.save()
        return site


class setStatus(FlaskForm):
    id = StringField()
    status = IntegerField()

    def set_status(self):
        id = self.data['id']
        site = Site.objects(_id=bson.objectid.ObjectId(id)).first()
        if not site:
            raise ValueError('内容不存在!')
        data = {}
        data['status'] = self.data['status']
        ok = site.update(**data)
        return ok

