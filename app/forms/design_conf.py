# coding: utf-8
from wtforms import TextAreaField, StringField, IntegerField, DateTimeField
from wtforms.validators import DataRequired, Length, EqualTo, NumberRange
from flask_wtf import FlaskForm
from bson import ObjectId
from flask import current_app

#from .base import BaseForm
from ..models.design_conf import DesignConf
#from ..helpers import *

class SaveForm(FlaskForm):
    id = StringField()
    user_id = IntegerField()    # 用户ID
    name = StringField('名称', validators=[Length(max=30, message="长度小于30个字符")])
    mark = StringField('标识', validators=[Length(max=20, message="长度小于20个字符")])
    type = IntegerField()    # 类型：1.默认；2.--；


    ## 基本信息
    in_d3ing = IntegerField()    # 是否入驻铟果平台
    key_personnel_count = IntegerField()    # 主要人员
    shareholder_count = IntegerField() # 股东信息
    chage_record_count = IntegerField() # 变更记录
    affiliated_agency_count = IntegerField() # 分支机构
    financing_count = IntegerField() # 融资
    core_team_count = IntegerField() # 核心团队
    enterprise_business_count = IntegerField() # 企业业务
    competitor_count = IntegerField() # 竞品信息
    bid_count = IntegerField() # 招投标


    ## 商业力指数
    scale_a = IntegerField()    # 公司规模: 20人以下
    scale_b = IntegerField()    # 公司规模: 20-50人
    scale_c = IntegerField()    # 公司规模: 50-100
    scale_d = IntegerField()    # 公司规模: 100-300
    scale_e = IntegerField()    # 公司规模: 300以上
    registered_capital_format = IntegerField() # 注册资金
    registered_capital_format_a = IntegerField() # 注册资金(1~100万)
    registered_capital_format_b = IntegerField() # 注册资金(101~500万)
    registered_capital_format_c = IntegerField() # 注册资金(501~1000万)
    registered_capital_format_d = IntegerField() # 注册资金(1001~5000万)
    registered_capital_format_e = IntegerField() # 注册资金(5000万以上)
    investment_abroad_count = IntegerField() # 对外投资
    annual_return_count = IntegerField() # 公司年报
    branch = IntegerField() # 分公司数量
    company_count = IntegerField() # 法人公司数量


    ## 创新力指数
    trademark_count = IntegerField() # 商标
    trademark_count_a = IntegerField() # 商标(1-4)
    trademark_count_b = IntegerField() # 商标(5-9)
    trademark_count_c = IntegerField() # 商标(10-49)
    trademark_count_d = IntegerField() # 商标(50-99)
    trademark_count_e = IntegerField() # 商标(100-499)
    trademark_count_f = IntegerField() # 商标(500+)
    patent_count = IntegerField() # 专利
    patent_count_a = IntegerField() # 专利(1-4)
    patent_count_b = IntegerField() # 专利(5-9)
    patent_count_c = IntegerField() # 专利(10-49)
    patent_count_d = IntegerField() # 专利(50-99)
    patent_count_e = IntegerField() # 专利(100-499)
    patent_count_f = IntegerField() # 专利(500+)
    software_copyright_count = IntegerField() # 软件著作权
    software_copyright_count_a = IntegerField() # 软件著作权(1-4)
    software_copyright_count_b = IntegerField() # 软件著作权(5-9)
    software_copyright_count_c = IntegerField() # 软件著作权(10-49)
    software_copyright_count_d = IntegerField() # 软件著作权(50-99)
    software_copyright_count_e = IntegerField() # 软件著作权(100-499)
    software_copyright_count_f = IntegerField() # 软件著作权(500+)

    works_copyright_count = IntegerField() # 作品著作权
    works_copyright_count_a = IntegerField() # 作品著作权(1-4)
    works_copyright_count_b = IntegerField() # 作品著作权(5-9)
    works_copyright_count_c = IntegerField() # 作品著作权(10-49)
    works_copyright_count_d = IntegerField() # 作品著作权(50-99)
    works_copyright_count_e = IntegerField() # 作品著作权(100-499)
    works_copyright_count_f = IntegerField() # 作品著作权(500+)
    icp_count = IntegerField() # 网站备案


    ## 设计力指数
    design_case_count = IntegerField() # 抓取作品数量
    d3in_case_count = IntegerField() # 铟果作品数量
    d3in_case_count_a = IntegerField() # 铟果作品数量(1-5)
    d3in_case_count_b = IntegerField() # 铟果作品数量(6-20)
    d3in_case_count_c = IntegerField() # 铟果作品数量(21-50)
    d3in_case_count_d = IntegerField() # 铟果作品数量(51-100)
    d3in_case_count_e = IntegerField() # 铟果作品数量(101-500)
    d3in_case_count_f = IntegerField() # 铟果作品数量(500+)
    design_center_province = IntegerField()    # 是否是设计中心: 省级；
    design_center_county = IntegerField()    # 是否是设计中心: 国家级；
    red_star_award_count = IntegerField()    # 红星奖数量
    innovative_design_award_count = IntegerField()    # 红棉奖数量
    china_design_award_count = IntegerField()    # 中国好设计奖数量
    dia_award_count = IntegerField() # 中国设计智造奖数量
    if_award_count = IntegerField()    # IF奖数量
    red_dot_award_count = IntegerField()    # 红点奖数量
    idea_award_count = IntegerField() # 美国IDEA工业设计优秀奖数量
    gmark_award_count = IntegerField() # G-Mark设计奖数量


    ## 影响力指数
    is_high_tech = IntegerField()    # 高新企业
    ty_score = IntegerField()    # 天眼查评分
    #ty_view_count = IntegerField()    # 天眼查浏览量
    ty_view_count_a = IntegerField()    # 天眼查浏览量 <100
    ty_view_count_b = IntegerField()    # 天眼查浏览量 >=100 & <500
    ty_view_count_c = IntegerField()    # 天眼查浏览量 >=500 & < 2000
    ty_view_count_d = IntegerField()    # 天眼查浏览量 >=2000 & < 5000
    ty_view_count_e = IntegerField()    # 天眼查浏览量 >=5000 & < 10000
    ty_view_count_f = IntegerField()    # 天眼查浏览量 >10000
    certification_count = IntegerField() # 资质证书
    cida_credit_rating_a = IntegerField() # 工会认证：A
    cida_credit_rating_b = IntegerField() # 工会认证：AA
    cida_credit_rating_c = IntegerField() # 工会认证：AAA
    wx_public_count = IntegerField() # 公号


    ## 社会信誉
    action_at_law_count = IntegerField() # 法律诉讼
    court_announcement_count = IntegerField() # 法院公告
    dishonest_person_count = IntegerField() # 失信人
    person_subject_count = IntegerField() # 被执行人
    announcement_court_count = IntegerField() # 开庭公告

    abnormal_operation_count = IntegerField() # 经营异常
    administrative_penalty_count = IntegerField() # 行政处罚
    break_law_count = IntegerField() # 严重违法
    equity_pledged_count = IntegerField() # 股权出质
    chattel_mortgage_count = IntegerField() # 动产抵押
    tax_notice_count = IntegerField() # 欠税公告
    judicial_sale_count = IntegerField() # 司法拍卖
    tax_rating_count = IntegerField() # 税务评级
    credit_enter_extra = IntegerField() # 入驻额外加分

    def update(self):
        id = self.data['id']
        design_conf = DesignConf.objects(_id=ObjectId(id)).first()
        if not design_conf:
            raise ValueError('内容不存在!')

        data = self.data
        data.pop('id')

        current_app.logger.debug(data)
        for key in self.data:
            if self.data[key] == None:
                #current_app.logger.debug(key)
                data.pop(key)

        #current_app.logger.debug(data)
        ok = design_conf.update(**data)
        return ok

    def save(self, **param):
        data = self.data;
        data['user_id'] = param['user_id']
        data.pop('id')
        design_conf = DesignConf(**data)
        design_conf.save()
        return design_conf


class setStatus(FlaskForm):
    id = StringField()
    status = IntegerField()

    def set_status(self):
        id = self.data['id']
        design_conf = DesignConf.objects(_id=ObjectId(id)).first()
        if not design_conf:
            raise ValueError('内容不存在!')
        data = {}
        data['status'] = self.data['status']
        ok = design_conf.update(**data)
        return ok

