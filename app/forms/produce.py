# coding: utf-8

from wtforms import TextAreaField, StringField, IntegerField, FloatField
from wtforms.validators import DataRequired, Length, EqualTo, NumberRange
from flask_wtf import FlaskForm
from bson import ObjectId
from ..models.produce import Produce


class SaveForm(FlaskForm):
    id = StringField()
    title = StringField('标题', validators=[Length(max=100, message="长度小于100个字符")])
    kind = IntegerField('类型')
    tags = StringField('标签', validators=[Length(max=500, message="长度小于500个字符")])  # 标签
    color_tags = StringField('颜色标签', validators=[Length(max=500, message="长度小于500个字符")])  # 颜色标签
    brand_tags = StringField('品牌标签', validators=[Length(max=500, message="长度小于500个字符")])  # 品牌标签
    material_tags = StringField('材质标签', validators=[Length(max=500, message="长度小于500个字符")])  # 材质
    style_tags = StringField('风格标签', validators=[Length(max=500, message="长度小于500个字符")])  # 风格
    technique_tags = StringField('工艺标签', validators=[Length(max=500, message="长度小于500个字符")])  # 工艺
    other_tags = StringField('其它标签', validators=[Length(max=500, message="长度小于500个字符")])  # 其它
    total_tags = StringField('所有标签')  # 所有标签
    url = StringField('原文地址', validators=[Length(max=500, message="长度小于500字符")])  # 原文地址
    price = StringField()  # 销售价
    currency_type = IntegerField()  # 币种: 1.RMB；2.美元；3.--；
    remark = StringField()
    designer = StringField()
    company = StringField()
    domain = IntegerField()
    # prize_id = IntegerField()  # 奖项ID
    # prize = StringField()
    # prize_level = StringField()  # 奖项级别
    # prize_time = StringField()  # 奖项时间
    info = StringField()
    channel = StringField('渠道', validators=[Length(max=30, message="长度小于30个字符")])  # 渠道
    brand_id = IntegerField()  # 品牌ID
    evt = IntegerField() # 来源
    category_id = IntegerField()  # 分类ID
    user_id = IntegerField()

    def update(self):
        id = self.data['id']
        item = Produce.objects(_id=ObjectId(id)).first()
        if not item:
            raise ValueError('产品不存在!')
        data = self.data
        if data['url']:
            if Produce.objects(_id__ne=ObjectId(id), img_url=data['url']).first():
                raise ValueError('产品已存在!!')
        data.pop('id')
        if 'total_tags' in data:
            data.pop('total_tags')
        data.pop('user_id')
        # data.pop('csrf_token')
        ok = item.update(**data)
        return ok

    def save(self, **param):
        data = self.data
        if data['img_url']:
            if Produce.objects(img_url=data['url']).first():
                raise ValueError('产品已存在!')
        data['user_id'] = param['user_id']
        data.pop('id')
        if 'total_tags' in data:
            data.pop('total_tags')
        item = Produce(**data)
        item.save()
        return item


## 保存 - API
class SaveApi(FlaskForm):
    id = StringField()
    title = StringField('标题', validators=[Length(max=100, message="长度小于100个字符")])
    kind = IntegerField('类型')
    channel = StringField('渠道', validators=[Length(max=30, message="长度小于30个字符")])  # 渠道
    url = StringField('原文地址', validators=[Length(max=500, message="长度小于500字符")])  # 原文地址
    tags = StringField('标签', validators=[Length(max=500, message="长度小于500个字符")])  # 标签
    color_tags = StringField('颜色标签', validators=[Length(max=500, message="长度小于500个字符")])  # 颜色标签
    brand_tags = StringField('品牌标签', validators=[Length(max=500, message="长度小于500个字符")])  # 品牌标签
    material_tags = StringField('材质标签', validators=[Length(max=500, message="长度小于500个字符")])  # 材质
    style_tags = StringField('风格标签', validators=[Length(max=500, message="长度小于500个字符")])  # 风格
    technique_tags = StringField('风格标签', validators=[Length(max=500, message="长度小于500个字符")])  # 风格
    other_tags = StringField('其它标签', validators=[Length(max=500, message="长度小于500个字符")])  # 其它
    remark = StringField()
    price = StringField()  # 销售价
    currency_type = IntegerField()  # 币种: 1.RMB；2.美元；3.--；
    brand_id = IntegerField()  # 品牌ID
    prize_id = IntegerField()  # 奖项ID
    designer = StringField()
    company = StringField()
    prize = StringField()
    prize_level = StringField()
    prize_time = StringField()
    info = StringField()
    evt = IntegerField()  # 来源

    def validate_img_url(self, field):
        if field.data:
            if Produce.objects(img_url=field.data).first():
                raise ValueError('产品已存在!')

    def save(self, **param):
        data = self.data
        item = Produce(**data)
        item.save()
        return item


class setStatus(FlaskForm):
    id = StringField()
    status = IntegerField()

    def set_status(self):
        id = self.data['id']
        item = Produce.objects(_id=ObjectId(id)).first()
        if not item:
            raise ValueError('产品不存在!')
        data = {}
        data['status'] = self.data['status']
        ok = item.update(**data)
        return ok
