from wtforms import TextAreaField, StringField, IntegerField
from wtforms.validators import DataRequired, Length, EqualTo, NumberRange
from flask_wtf import FlaskForm
from bson import ObjectId
from ..models.column_zone import ColumnZone


class SaveForm(FlaskForm):
    id = StringField()
    name = StringField('空间标识',validators=[Length(2,50,message='长度位于2~50之间')])
    title= StringField('空间名称',validators=[Length(2,50,message='长度位于2~50之间')])
    user_id = IntegerField() # 用户id
    width = IntegerField()  # 宽
    height = IntegerField()  # 高
    kind = IntegerField()  # 类型：1.PC；2.备选；3.--
    remark =  StringField() # 备注

    def update(self):
        id = self.data['id']
        item = ColumnZone.objects(_id=ObjectId(id)).first()
        if not item:
            raise ValueError('栏目空间位置不存在!')
        data = self.data
        if data['name']:
            if ColumnZone.objects(_id__ne=ObjectId(id), name=data['name']).first():
                raise ValueError('栏目空间位置已存在!!')
        data.pop('id')
        data.pop('user_id')
        #data.pop('csrf_token')
        ok = item.update(**data)
        return ok

    def save(self, **param):
        data = self.data
        if data['name']:
            if ColumnZone.objects(name=data['name']).first():
                raise ValueError('栏目空间位置已存在!')
        data['user_id'] = param['user_id']
        data.pop('id')
        item = ColumnZone(**data)
        item.save()
        return item



class setStatus(FlaskForm):
    id = StringField()
    status = IntegerField()

    def set_status(self):
        id = self.data['id']
        item = ColumnZone.objects(_id=ObjectId(id)).first()
        if not item:
            raise ValueError('栏目空间位置不存在!')
        data = {}
        data['status'] = self.data['status']
        ok = item.update(**data)
        return ok
