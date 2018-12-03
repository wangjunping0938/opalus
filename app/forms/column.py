from wtforms import TextAreaField, StringField, IntegerField
from wtforms.validators import DataRequired, Length, EqualTo, NumberRange
from flask_wtf import FlaskForm
from bson import ObjectId

from app.models.asset import Asset
from ..models.column import Column


class SaveForm(FlaskForm):
    id = StringField()
    title = StringField('标题', validators=[Length(max=30, message='长度最大为30')])
    sub_title = StringField('副标题', validators=[Length(max=30, message='长度最大为30')])
    description = StringField()  # 描述
    target = StringField('标记',validators=[Length(max=1000, message='长度最大为1000')])
    column_zone_id = StringField()  # 栏目空间id
    user_id = IntegerField()  # 用户id
    sort = IntegerField()  # 排序
    cover_id = StringField()  # 封面id
    kind = IntegerField()  # 类型：1.PC；2.备选；3.--
    remark = StringField()  # 备注
    asset_ids = StringField()
    asset_type = IntegerField()

    def update(self):
        id = self.data['id']
        item = Column.objects(_id=ObjectId(id)).first()
        if not item:
            raise ValueError('栏目信息不存在!')
        data = self.data
        if data['title']:
            if Column.objects(_id__ne=ObjectId(id), name=data['title']).first():
                raise ValueError('栏目信息已存在!!')
        data.pop('id')
        data.pop('user_id')
        data.pop('asset_type')
        data.pop('asset_ids')
        # data.pop('csrf_token')
        ok = item.update(**data)
        return ok

    def save(self, **param):
        data = self.data
        asset_ids = data['asset_ids']
        if data['title']:
            if Column.objects(title=data['title']).first():
                raise ValueError('栏目信息已存在!')
        data['user_id'] = param['user_id']
        data.pop('id')
        data.pop('asset_ids')
        data.pop('asset_type')
        item = Column(**data)
        ok = item.save()
        if not ok:
            raise ValueError('保存失败!')
        # 更新附件
        if asset_ids:
            asset_arr = asset_ids.strip().split(',')
            for asset_id in asset_arr:
                try:
                    asset = Asset.objects(_id=ObjectId(asset_id)).first()
                    if asset:
                        asset.update(target_id=str(item._id))
                except(Exception) as e:
                    continue
        return item


class setStatus(FlaskForm):
    id = StringField()
    status = IntegerField()

    def set_status(self):
        id = self.data['id']
        item = Column.objects(_id=ObjectId(id)).first()
        if not item:
            raise ValueError('栏目信息不存在!')
        data = {}
        data['status'] = self.data['status']
        ok = item.update(**data)
        return ok