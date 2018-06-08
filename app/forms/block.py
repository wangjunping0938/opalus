# coding: utf-8
from wtforms import TextAreaField, StringField, IntegerField
from wtforms.validators import DataRequired, Length, EqualTo, NumberRange
from flask_wtf import FlaskForm
from bson import ObjectId
from app.helpers.role import check_role

#from .base import BaseForm
from ..models.block import Block
#from ..helpers import *

class SaveForm(FlaskForm):
    id = StringField()
    mark = StringField('唯一标识', validators=[DataRequired(message="唯一标识不能为空"), Length(min=4, max=30, message="长度大于4小于30")])
    name = StringField('名称', validators=[DataRequired(message="名称不能为空")])
    code = StringField()
    content = StringField()
    remark = StringField()
    kind = IntegerField()
    role = IntegerField() # 权重：0.基本；1.编辑；5.超级管理员
    user_id = IntegerField()

    def update(self):
        id = self.data['id']
        block = Block.objects(_id=ObjectId(id)).first()
        if not block:
            raise ValueError('内容不存在!')

        is_pass = check_role(block.role)
        if not is_pass:
            raise ValueError('无权限操作!')
        data = {}

        data['mark'] = self.data['mark']
        data['name'] = self.data['name']
        data['code'] = self.data['code']
        data['content'] = self.data['content']
        data['remark'] = self.data['remark']
        data['kind'] = self.data['kind']
        data['role'] = self.data['role']

        ok = block.update(**data)
        return ok

    def save(self, **param):
        data = self.data;

        is_pass = check_role(data['role'])
        if not is_pass:
            raise ValueError('无权限操作!')

        data['user_id'] = param['user_id']
        data.pop('id')
        block = Block(**data)
        block.save()
        return block

class setStatus(FlaskForm):
    id = StringField()
    status = IntegerField()

    def set_status(self):
        id = self.data['id']
        block = Block.objects(_id=ObjectId(id)).first()
        if not block:
            raise ValueError('内容不存在!')
        data = {}
        data['status'] = self.data['status']
        ok = block.update(**data)
        return ok

