# coding: utf-8
from wtforms import TextAreaField, StringField, IntegerField, DateTimeField
from wtforms.validators import DataRequired, Length, EqualTo, NumberRange
from flask_wtf import FlaskForm
from bson import ObjectId
from flask import current_app

#from .base import BaseForm
from ..models.design_company import DesignCompany
#from ..helpers import *

class SaveForm(FlaskForm):
    id = StringField()
    ## 基本信息
    name = StringField('名称', validators=[Length(max=50, message="长度小于50个字符")])
    short_name = StringField('短名称', validators=[Length(max=20, message="长度小于20个字符")])
    url = StringField('网址', validators=[Length(max=200, message="长度小于200个字符")])
    logo_url = StringField('logo', validators=[Length(max=200, message="长度小于200个字符")])
    scale = IntegerField()
    scale_label = StringField('公司规模', validators=[Length(max=20, message="长度小于20个字符")])
    nature = IntegerField()
    nature_label = StringField('公司性质', validators=[Length(max=20, message="长度小于20个字符")])
    advantage = StringField('公司亮点', validators=[Length(max=10000, message="长度小于10000个字符")])
    description = StringField('公司描述', validators=[Length(max=50000, message="长度小于50000个字符")])

    ## 联系信息
    province_id = IntegerField()
    province = StringField('省份', validators=[Length(max=30, message="长度小于30个字符")])
    city_id = IntegerField()
    city = StringField('城市', validators=[Length(max=30, message="长度小于30个字符")])
    address = StringField('详细地址', validators=[Length(max=500, message="长度小于500个字符")])
    zip_code = StringField('邮编', validators=[Length(max=10, message="长度小于10个字符")])
    contact_name = StringField('联系人姓名', validators=[Length(max=30, message="长度小于30个字符")])
    contact_phone = StringField('联系人电话', validators=[Length(max=20, message="长度小于20个字符")])
    contact_email = StringField('邮箱', validators=[Length(max=50, message="长度小于50个字符")])
    tel = StringField('公司电话', validators=[Length(max=20, message="长度小于20个字符")])

    ## 公司注册信息
    founder = StringField('创始人', validators=[Length(max=30, message="长度小于30个字符")])
    founder_desc = StringField('创始人介绍', validators=[Length(max=500, message="长度小于500个字符")])
    registered_capital = StringField('注册资金', validators=[Length(max=30, message="长度小于30个字符")])
    registered_time = StringField('注册时间', validators=[Length(max=30, message="长度小于30个字符")])
    company_count = StringField('公司数量', validators=[Length(max=20, message="长度小于20个字符")])
    company_type = StringField('公司类型', validators=[Length(max=30, message="长度小于30个字符")])
    registration_number = StringField('纳税人识别号', validators=[Length(max=50, message="长度小于50个字符")])
    credit_code = StringField('统一信用代码', validators=[Length(max=30, message="长度小于30个字符")])
    identification_number = StringField('纳税人识别号', validators=[Length(max=30, message="长度小于30个字符")])
    industry = StringField('行业', validators=[Length(max=30, message="长度小于30个字符")])
    business_term = StringField('营业期限', validators=[Length(max=30, message="长度小于30个字符")])
    issue_date = StringField('核准日期', validators=[Length(max=20, message="长度小于20个字符")])
    registration_authority = StringField('登记机关', validators=[Length(max=50, message="长度小于50个字符")])
    registered_address = StringField('注册地址', validators=[Length(max=500, message="长度小于500个字符")])
    scope_business = StringField('经营范围', validators=[Length(max=2000, message="长度小于2000个字符")])
    organization_code = StringField('组织机构代码', validators=[Length(max=30, message="长度小于30个字符")])

    ## 公司背景(数量)
    key_personnel_count = IntegerField() # 主要人员
    shareholder_count = IntegerField() # 股东信息
    investment_abroad_count = IntegerField() # 对外投资
    annual_return_count = IntegerField() # 公司年报
    chage_record_count = IntegerField() # 变更记录
    affiliated_agency_count = IntegerField() # 分支机构


    ## 公司发展(数量)
    financing_count = IntegerField() # 融资
    core_team_count = IntegerField() # 核心团队
    enterprise_business_count = IntegerField() # 企业业务
    investment_events_count = IntegerField() # 投资事件
    competitor_count = IntegerField() # 竞品信息

    ## 司法风险(数量)
    action_at_law_count = IntegerField() # 法律诉讼
    court_announcement_count = IntegerField() # 法院公告
    dishonest_person_count = IntegerField() # 失信人
    person_subject_count = IntegerField() # 被执行人
    announcement_court_count = IntegerField() # 开庭公告

    ## 经营风险(数量)
    abnormal_operation_count = IntegerField() # 经营异常
    administrative_penalty_count = IntegerField() # 行政处罚
    break_law_count = IntegerField() # 严重违法
    equity_pledged_count = IntegerField() # 股权出质
    chattel_mortgage_count = IntegerField() # 动产抵押
    tax_notice_count = IntegerField() # 欠税公告
    judicial_sale_count = IntegerField() # 司法拍卖

    ## 经营状况(数量)
    bid_count = IntegerField() # 招投标
    tax_rating_count = IntegerField() # 税务评级
    product_count = IntegerField() # 产品信息
    import_and_export_credit_count = IntegerField() # 进出口信用
    certification_count = IntegerField() # 资质证书
    wx_public_count = IntegerField() # 公号

    ## 知识产权(数量)
    trademark_count = IntegerField() # 商标
    patent_count = IntegerField() # 专利
    software_copyright_count = IntegerField() # 软件著作权
    works_copyright_count = IntegerField() # 作品著作权
    icp_count = IntegerField() # 网站备案


    ## 附加
    tags = StringField('标签', validators=[Length(max=100, message="长度小于100个字符")])   # 标签
    branch = StringField('分公司数', validators=[Length(max=30, message="长度小于30个字符")]) # 分公司数量
    wx_public_no = StringField('公众号ID', validators=[Length(max=200, message="长度小于200个字符")]) # 公众号ID
    wx_public = StringField('公众号名称', validators=[Length(max=300, message="长度小于300个字符")]) # 公众号名称
    wx_public_qr = StringField('公众号二维码', validators=[Length(max=500, message="长度小于500个字符")]) # 公众号二维码
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
        design_company = DesignCompany.objects(_id=ObjectId(id)).first()
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
        design_company = DesignCompany.objects(_id=ObjectId(id)).first()
        if not design_company:
            raise ValueError('内容不存在!')
        data = {}
        data['status'] = self.data['status']
        ok = design_company.update(**data)
        return ok

