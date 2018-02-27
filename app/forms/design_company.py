# coding: utf-8
from wtforms import TextAreaField, StringField, IntegerField, DateTimeField
from wtforms.validators import DataRequired, Length, EqualTo, NumberRange
from flask_wtf import FlaskForm
import bson
from flask import current_app

#from .base import BaseForm
from ..models.design_company import DesignCompany
from ..helpers import *

class SaveForm(FlaskForm):
    id = StringField()
    ## 基本信息
    name = StringField('名称', validators=[DataRequired(message="名称不能为空"), Length(min=4, max=50, message="长度大于4小于50个字符")])
    short_name = StringField('短名称', validators=[Length(max=20, message="长度小于20个字符")])
    url = StringField('网址', validators=[Length(max=200, message="长度小于200个字符")])
    logo_url = StringField('logo', validators=[Length(max=200, message="长度小于200个字符")])
    scale = IntegerField()
    scale_label = StringField('公司规模', validators=[Length(max=20, message="长度小于20个字符")])
    nature = IntegerField()
    nature_label = StringField('公司性质', validators=[Length(max=20, message="长度小于20个字符")])
    advantage = StringField('公司亮点', validators=[Length(max=1000, message="长度小于1000个字符")])
    description = StringField('公司描述', validators=[Length(max=1000, message="长度小于1000个字符")])

    ## 联系信息
    province_id = IntegerField()
    province = StringField('省份', validators=[Length(max=30, message="长度小于30个字符")])
    city_id = IntegerField()
    city = StringField('城市', validators=[Length(max=30, message="长度小于30个字符")])
    address = StringField('详细地址', validators=[Length(max=500, message="长度小于30个字符")])
    zip_code = StringField('邮编', validators=[Length(max=10, message="长度小于10个字符")])
    contact_name = StringField('联系人姓名', validators=[Length(max=30, message="长度小于30个字符")])
    contact_phone = StringField('联系人电话', validators=[Length(max=20, message="长度小于20个字符")])
    contact_email = StringField('邮箱', validators=[Length(max=50, message="长度小于50个字符")])
    tel = StringField('公司电话', validators=[Length(max=20, message="长度小于20个字符")])

    ## 附加
    tags = StringField('标签', validators=[Length(max=100, message="长度小于100个字符")])   # 标签
    branch = StringField('分公司数', validators=[Length(max=20, message="长度小于20个字符")]) # 分公司数量
    wx_public_no = StringField('公众号ID', validators=[Length(max=20, message="长度小于20个字符")]) # 公众号ID
    wx_public = StringField('公众号名称', validators=[Length(max=30, message="长度小于30个字符")]) # 公众号名称
    remark = StringField('备注', validators=[Length(max=200, message="长度小于200个字符")])   # 备注
    perfect_degree = IntegerField() # 信息完整度
    craw_count = IntegerField() # 抓取频次
    kind = IntegerField()    # 类型: 预设
    type = IntegerField()    # 类型: 预设
    craw_user_id = IntegerField()    # 抓取人ID：1.军平；2.董永胜; 3.--;
    user_id = IntegerField()
    last_on = DateTimeField()    # 最后一次抓取时间

    def update(self):
        id = self.data['id']
        design_company = DesignCompany.objects(_id=bson.objectid.ObjectId(id)).first()
        if not design_company:
            raise ValueError('内容不存在!')

        '''
        data = {}
        data['name'] = self.data['name']
        data['short_name'] = self.data['short_name']
        data['url'] = self.data['url']
        data['logo_url'] = self.data['logo_url']
        data['scale'] = self.data['scale']
        data['scale_label'] = self.data['scale_label']
        data['nature'] = self.data['nature']
        data['nature_label'] = self.data['nature_label']
        data['advantage'] = self.data['advantage']
        data['description'] = self.data['description']
        data['remark'] = self.data['remark']
        data['tags'] = self.data['tags']
        data['branch'] = self.data['branch']
        data['wx_public_no'] = self.data['wx_public_no']
        data['wx_public'] = self.data['wx_public']
        '''

        data = self.data
        data.pop('id')

        current_app.logger.debug(data)
        for key in self.data:
            if self.data[key] == None:
                #current_app.logger.debug(key)
                data.pop(key)

        #current_app.logger.debug(data)
        ok = design_company.update(**data)
        return ok

    def save(self, **param):
        data = self.data;
        data['user_id'] = param['user_id']
        data.pop('id')
        design_company = DesignCompany(**data)
        design_company.save()
        return design_company


class setStatus(FlaskForm):
    id = StringField()
    status = IntegerField()

    def set_status(self):
        id = self.data['id']
        design_company = DesignCompany.objects(_id=bson.objectid.ObjectId(id)).first()
        if not design_company:
            raise ValueError('内容不存在!')
        data = {}
        data['status'] = self.data['status']
        ok = design_company.update(**data)
        return ok

