# coding: utf-8
from wtforms import TextAreaField, StringField, IntegerField
from wtforms.validators import DataRequired, Length, EqualTo, NumberRange
from flask_wtf import FlaskForm
from bson import ObjectId
from ..models.color import Color


class SaveForm(FlaskForm):
    id = StringField()
    rgb = StringField('rgb色值', validators=[DataRequired(message="RGB不能为空")])
    hex = StringField()
    cmyk = StringField()
    pantong = StringField()
    user_id = IntegerField()

    def update(self):
        id = self.data['id']
        color = Color.objects(_id=ObjectId(id)).first()
        if not color:
            raise ValueError('内容不存在!')

        data = {}

        data['rgb'] = self.data['rgb']
        data['hex'] = self.data['hex']
        data['cmyk'] = self.data['cmyk']
        data['pantong'] = self.data['pantong']
        ok = color.update(**data)
        return ok

    def save(self, **param):
        data = self.data
        data.pop('id')
        color = Color(**data)
        color.save()
        return color


class setStatus(FlaskForm):
    id = StringField()
    status = IntegerField()

    def set_status(self):
        id = self.data['id']
        block = Color.objects(_id=ObjectId(id)).first()
        if not block:
            raise ValueError('内容不存在!')
        data = {}
        data['status'] = self.data['status']
        ok = block.update(**data)
        return ok
