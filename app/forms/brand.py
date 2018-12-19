# coding: utf-8

from wtforms import TextAreaField, StringField, IntegerField
from wtforms.validators import DataRequired, Length, EqualTo, NumberRange
from flask_wtf import FlaskForm

from ..models.brand import Brand
from ..models.asset import Asset
from bson import ObjectId

class SaveForm(FlaskForm):
    id = StringField()

    name = StringField('名称', validators=[DataRequired(message="名称不能为空"), Length(min=2, max=30, message="长度大于2小于30个字符")])
    en_name = StringField()
    asset_type = IntegerField()
    kind = IntegerField()
    category_id = IntegerField()
    country = StringField()
    found_time = StringField()
    url = StringField()
    remark = StringField()
    cover_id = StringField()
    description = StringField()
    user_id = IntegerField()
    asset_ids = StringField()

    def update(self):
        id = self.data['id']
        item = Brand.objects(_id=id).first()
        if not item:
            raise ValueError('内容不存在!')
        data = self.data
        data.pop('id')
        data.pop('user_id')
        data.pop('asset_type')
        data.pop('asset_ids')
        #data.pop('csrf_token')
        ok = item.update(**data)
        return ok

    def save(self, **param):
        data = self.data;
        asset_ids = data['asset_ids']
        data['user_id'] = param['user_id']
        data.pop('id')
        data.pop('asset_ids')
        data.pop('asset_type')
        item = Brand(**data)
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
        item = Brand.objects(_id=id).first()
        if not item:
            raise ValueError('内容不存在!')
        data = {}
        data['status'] = self.data['status']
        ok = item.update(**data)
        return ok
