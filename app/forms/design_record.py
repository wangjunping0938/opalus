# coding: utf-8
from wtforms import TextAreaField, StringField, IntegerField, DateTimeField
from wtforms.validators import DataRequired, Length, NumberRange
from flask_wtf import FlaskForm
from bson import ObjectId
from flask import current_app

from ..models.design_record import DesignRecord

class SaveForm(FlaskForm):
    id = StringField()

    number = StringField('公司编号', validators=[DataRequired(message="编号不能为空"), Length(max=20, message="长度小于20个字符")]) # 所属公司编号
    mark = StringField('配置标识', validators=[DataRequired(message="标识不能为空"), Length(max=20, message="长度小于20个字符")]) # 所属配置标识
    no = IntegerField() # 统计期数
    user_id = IntegerField()
    deleted = IntegerField()  # 软删除
    type = IntegerField()

    ## 不同维度打分
    base_score = IntegerField()    # 基础分
    business_score = IntegerField()    # 商业力分
    innovate_score = IntegerField()    # 创新力分
    design_score = IntegerField()    # 设计力分
    effect_score = IntegerField()    # 影响力分
    credit_score = IntegerField()    # 信誉度分

    total_score = IntegerField()    # 总分


    def update(self, **param):
        id = self.data['id']
        if not id:
            id = param['id']
        if not id:
            raise ValueError('ID不存在!')

        item = DesignRecord.objects(_id=ObjectId(id)).first()
        if not item:
            raise ValueError('内容不存在!')

        data = self.data
        if 'deleted' in param:
            data['deleted'] = param['deleted']

        data.pop('id')

        current_app.logger.debug(data)
        for key in self.data:
            if self.data[key] == None:
                data.pop(key)

        ok = item.update(**data)
        return ok

    def save(self, **param):
        data = self.data;
        data.pop('id')
        item = DesignRecord(**data)
        item.save()
        return item


class setStatus(FlaskForm):
    id = StringField()
    status = IntegerField()

    def set_status(self):
        id = self.data['id']
        item = DesignRecord.objects(_id=ObjectId(id)).first()
        if not item:
            raise ValueError('内容不存在!')
        data = {}
        data['status'] = self.data['status']
        ok = item.update(**data)
        return ok

