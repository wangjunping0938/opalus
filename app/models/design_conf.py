# -*- coding:utf-8 -*-
import datetime
from . import db
from .base import Base

# 设计公司排行配置表- design_conf
class DesignConf(Base):

    meta = {
        'collection': 'design_conf',
        'ordering': ['-created_at'],
        'strict': True,
        'id_field': '_id'
    }

    _id = db.StringField()
    user_id = db.IntField(default=0)    # 用户ID
    mark = db.StringField(max_length=20, required=True, unique=True) # 标识
    name = db.StringField(max_length=30, required=True) # 名称
    type = db.IntField(default=1)    # # 类型：1.默认；2.--；

    ## 基本信息
    in_d3ing = db.IntField(default=0)    # 是否入驻铟果平台
    key_personnel_count = db.IntField(default=0)    # 主要人员
    shareholder_count = db.IntField(default=0) # 股东信息
    chage_record_count = db.IntField(default=0) # 变更记录
    affiliated_agency_count = db.IntField(default=0) # 分支机构
    financing_count = db.IntField(default=0) # 融资
    core_team_count = db.IntField(default=0) # 核心团队
    enterprise_business_count = db.IntField(default=0) # 企业业务
    competitor_count = db.IntField(default=0) # 竞品信息
    bid_count = db.IntField(default=0) # 招投标


    ## 商业力指数
    scale_a = db.IntField(default=0)    # 公司规模: 20人以下
    scale_b = db.IntField(default=0)    # 公司规模: 20-50人
    scale_c = db.IntField(default=0)    # 公司规模: 50-100
    scale_d = db.IntField(default=0)    # 公司规模: 100-300
    scale_e = db.IntField(default=0)    # 公司规模: 300以上
    registered_capital_format = db.IntField(default=0) # 注册资金
    registered_capital_format_a = db.IntField(default=0) # 注册资金(1~100万)
    registered_capital_format_b = db.IntField(default=0) # 注册资金(101~500万)
    registered_capital_format_c = db.IntField(default=0) # 注册资金(501~1000万)
    registered_capital_format_d = db.IntField(default=0) # 注册资金(1001~5000万)
    registered_capital_format_e = db.IntField(default=0) # 注册资金(5000万以上)
    investment_abroad_count = db.IntField(default=0) # 对外投资
    annual_return_count = db.IntField(default=0) # 公司年报
    branch = db.IntField(default=0) # 分公司数量


    ## 创新力指数
    trademark_count = db.IntField(default=0) # 商标
    trademark_count_a = db.IntField(default=0) # 商标(1-4)
    trademark_count_b = db.IntField(default=0) # 商标(5-9)
    trademark_count_c = db.IntField(default=0) # 商标(10-49)
    trademark_count_d = db.IntField(default=0) # 商标(50-99)
    trademark_count_e = db.IntField(default=0) # 商标(100-499)
    trademark_count_f = db.IntField(default=0) # 商标(500+)
    patent_count = db.IntField(default=0) # 专利
    patent_count_a = db.IntField(default=0) # 专利(1-4)
    patent_count_b = db.IntField(default=0) # 专利(5-9)
    patent_count_c = db.IntField(default=0) # 专利(10-49)
    patent_count_d = db.IntField(default=0) # 专利(50-99)
    patent_count_e = db.IntField(default=0) # 专利(100-499)
    patent_count_f = db.IntField(default=0) # 专利(500+)
    software_copyright_count = db.IntField(default=0) # 软件著作权
    software_copyright_count_a = db.IntField(default=0) # 软件著作权(1-4)
    software_copyright_count_b = db.IntField(default=0) # 软件著作权(5-9)
    software_copyright_count_c = db.IntField(default=0) # 软件著作权(10-49)
    software_copyright_count_d = db.IntField(default=0) # 软件著作权(50-99)
    software_copyright_count_e = db.IntField(default=0) # 软件著作权(100-499)
    software_copyright_count_f = db.IntField(default=0) # 软件著作权(500+)
    works_copyright_count = db.IntField(default=0) # 作品著作权
    works_copyright_count_a = db.IntField(default=0) # 作品著作权(1-4)
    works_copyright_count_b = db.IntField(default=0) # 作品著作权(5-9)
    works_copyright_count_c = db.IntField(default=0) # 作品著作权(10-49)
    works_copyright_count_d = db.IntField(default=0) # 作品著作权(50-99)
    works_copyright_count_e = db.IntField(default=0) # 作品著作权(100-499)
    works_copyright_count_f = db.IntField(default=0) # 作品著作权(500+)
    icp_count = db.IntField(default=0) # 网站备案


    ## 设计力指数
    design_case_count = db.IntField(default=0) # 抓取作品数量
    d3in_case_count = db.IntField(default=0) # 铟果作品数量
    design_center_province = db.IntField(default=0)    # 是否是设计中心: 省级；
    design_center_county = db.IntField(default=0)    # 是否是设计中心: 国家级；
    red_star_award_count = db.IntField(default=0)    # 红星奖数量
    innovative_design_award_count = db.IntField(default=0)    # 红棉奖数量
    china_design_award_count = db.IntField(default=0)    # 中国好设计奖数量
    dia_award_count = db.IntField(default=0)    # 中国设计智造奖数量
    if_award_count = db.IntField(default=0)    # IF奖数量
    red_dot_award_count = db.IntField(default=0)    # 红点奖数量
    idea_award_count = db.IntField(default=0) # 美国IDEA工业设计优秀奖数量
    gmark_award_count = db.IntField(default=0) # G-Mark设计奖数量


    ## 影响力指数
    is_high_tech = db.IntField(default=0)    # 高新企业
    ty_score = db.IntField(default=0)    # 天眼查评分
    #ty_view_count = db.IntField(default=0)    # 天眼查浏览量
    ty_view_count_a = db.IntField(default=0)    # 天眼查浏览量 < 100
    ty_view_count_b = db.IntField(default=0)    # 天眼查浏览量 >=100 & <500
    ty_view_count_c = db.IntField(default=0)    # 天眼查浏览量 >=500 & < 2000
    ty_view_count_d = db.IntField(default=0)    # 天眼查浏览量 >=2000 & < 5000
    ty_view_count_e = db.IntField(default=0)    # 天眼查浏览量 >=5000 & < 10000
    ty_view_count_f = db.IntField(default=0)    # 天眼查浏览量 >10000
    certification_count = db.IntField(default=0) # 资质证书
    cida_credit_rating_a = db.IntField(default=0) # 工会认证：A
    cida_credit_rating_b = db.IntField(default=0) # 工会认证：AA
    cida_credit_rating_c = db.IntField(default=0) # 工会认证：AAA
    wx_public_count = db.IntField(default=0) # 公号


    ## 社会信誉
    action_at_law_count = db.IntField(default=0) # 法律诉讼
    court_announcement_count = db.IntField(default=0) # 法院公告
    dishonest_person_count = db.IntField(default=0) # 失信人
    person_subject_count = db.IntField(default=0) # 被执行人
    announcement_court_count = db.IntField(default=0) # 开庭公告

    abnormal_operation_count = db.IntField(default=0) # 经营异常
    administrative_penalty_count = db.IntField(default=0) # 行政处罚
    break_law_count = db.IntField(default=0) # 严重违法
    equity_pledged_count = db.IntField(default=0) # 股权出质
    chattel_mortgage_count = db.IntField(default=0) # 动产抵押
    tax_notice_count = db.IntField(default=0) # 欠税公告
    judicial_sale_count = db.IntField(default=0) # 司法拍卖
    tax_rating_count = db.IntField(default=0) # 税务评级


    status = db.IntField(default=0)    # 状态: 0.禁用；1.启用
    deleted = db.IntField(default=0)    # 是否软删除

    created_at = db.DateTimeField()
    updated_at = db.DateTimeField()


    def save(self, *args, **kwargs):
        return super(DesignConf, self).save(*args, **kwargs)


    def update(self, *args, **kwargs):
        return super(DesignConf, self).update(*args, **kwargs)


    def mark_delete(self):
        return super(DesignConf, self).update(deleted=1)

    def __unicode__(self):
        return self.name


