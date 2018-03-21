# coding: utf-8
from wtforms import TextAreaField, StringField, IntegerField, DateTimeField
from wtforms.validators import DataRequired, Length, EqualTo, NumberRange
from flask_wtf import FlaskForm
from bson import ObjectId
from flask import current_app

from ..models.design_case import DesignCase
#from ..helpers import *

class SaveForm(FlaskForm):
    id = StringField()
    title = StringField('标题', validators=[DataRequired(message="名称不能为空"), Length(max=100, message="长度小于100个字符")])
    description = StringField('简述', validators=[Length(max=1000, message="长度小于1000个字符")])
    content = StringField('内容', validators=[Length(max=50000, message="长度小于50000个字符")])
    category = StringField('分类', validators=[Length(max=50, message="长度小于50个字符")])

    cover_url = StringField('封面', validators=[Length(max=200, message="长度小于200个字符")])
    images = StringField('图集', validators=[Length(max=1000, message="长度小于1000个字符")])
    prize_label = StringField('奖项名称', validators=[Length(max=100, message="长度小于100个字符")])
    prize_level = StringField('奖项级别', validators=[Length(max=100, message="长度小于100个字符")])
    target_id = StringField('关联ID', validators=[Length(max=20, message="长度小于20个字符")])
    type = IntegerField()    # 类型: 1.公司奖项案例
    user_id = IntegerField()
    tags = StringField('标签', validators=[Length(max=500, message="长度小于100个字符")])   # 标签
    designer_name = StringField('设计师姓名', validators=[Length(max=30, message="长度小于30个字符")])
    company_name = StringField('公司名称', validators=[Length(max=100, message="长度小于100个字符")])
    en_company_name = StringField('公司英文名称', validators=[Length(max=200, message="长度小于200个字符")])
    award_time = StringField('获奖时间', validators=[Length(max=20, message="长度小于20个字符")])
    is_listed = StringField('是否上市', validators=[Length(max=20, message="长度小于20个字符")])

    def update(self):
        id = self.data['id']
        item = DesignCase.objects(_id=ObjectId(id)).first()
        if not item:
            raise ValueError('内容不存在!')

        data = self.data
        data.pop('id')

        for key in self.data:
            if self.data[key] == None:
                data.pop(key)

        current_app.logger.debug(data)
        ok = item.update(**data)
        return ok

    def save(self, **param):
        data = self.data;
        data['user_id'] = param['user_id']
        data.pop('id')
        item = DesignCase(**data)
        item.save()
        return item


class setStatus(FlaskForm):
    id = StringField()
    status = IntegerField()

    def set_status(self):
        id = self.data['id']
        item = DesignCase.objects(_id=bson.objectid.ObjectId(id)).first()
        if not item:
            raise ValueError('内容不存在!')
        data = {}
        data['status'] = self.data['status']
        ok = item.update(**data)
        return ok

