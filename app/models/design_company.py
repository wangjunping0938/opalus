# -*- coding:utf-8 -*-
import datetime
from . import db
from .base import Base

# 设计公司管理表- design_company
class DesignCompany(Base):

    meta = {
        'collection': 'design_company',
        'ordering': ['-created_at'],
        'strict': True,
        'id_field': '_id'
    }

    _id = db.StringField()
    number = db.IntField(required=True, unique=True)    # 唯一标识
    user_id = db.IntField(default=0)    # 用户ID
    d3ing_id = db.IntField(default=0)    # 铟果平台公司ID

    ## 基本信息
    name = db.StringField(max_length=50, required=True, unique=True) # 名称
    short_name = db.StringField(max_length=50, default='') # 短名称
    english_name = db.StringField(max_length=100, default='') # 英文名称
    url = db.StringField(max_length=200, default='') # 网址
    logo_url = db.StringField(max_length=200, default='') # LOGO地址
    scale = db.IntField(default=0)    # 公司规模
    scale_label = db.StringField(max_length=20, default='') # 公司规模_label
    nature = db.IntField(default=0)    # 公司性质
    nature_label = db.StringField(max_length=20, default='') # 公司性质_label
    company_status_label = db.StringField(max_length=50, default='') # 公司状态_label
    advantage = db.StringField(max_length=10000, default='') # 公司亮点、专业优势
    description = db.StringField(max_length=50000, default='') # 公司描述
    is_high_tech = db.IntField(default=0)    # 是否是高新企业: 0.否；1.是；
    is_design_center = db.IntField(default=0)    # 是否是设计中心: 0.否；1.省级；2.国家级；
    ty_score = db.IntField(default=0)    # 天眼查评分
    ty_view_count = db.IntField(default=0)    # 天眼查浏览量
    ty_last_time = db.StringField(max_length=50, default='') # 天眼查最后更新时间
    design_case_count = db.IntField(default=0)    # 抓取作品数量
    d3in_case_count = db.IntField(default=0)    # 铟果作品数量
    red_star_award_count = db.IntField(default=0)    # 红星奖数量
    innovative_design_award_count = db.IntField(default=0)    # 红棉奖数量
    china_design_award_count = db.IntField(default=0)    # 中国好设计奖数量
    dia_award_count = db.IntField(default=0) # 中国设计智造奖数量
    if_award_count = db.IntField(default=0)    # if奖数量
    red_dot_award_count = db.IntField(default=0)    # 红点奖数量
    idea_award_count = db.IntField(default=0) # 美国IDEA工业设计优秀奖数量
    gmark_award_count = db.IntField(default=0) # G-Mark设计奖数量


    ## 联系信息
    province_id = db.IntField(default=0)    # 省
    province = db.StringField(max_length=30, default='') # 省_label
    city_id = db.IntField(default=0)    # 市
    city = db.StringField(max_length=30, default='') # 市_label
    address = db.StringField(max_length=500, default='') # 详细地址
    zip_code = db.StringField(max_length=10, default='') # 邮编
    contact_name = db.StringField(max_length=30, default='') # 联系人姓名
    contact_phone = db.StringField(max_length=20, default='') # 联系人电话
    contact_email = db.StringField(max_length=200, default='') # 联系人邮箱
    tel = db.StringField(max_length=20, default='') # 公司电话

    ## 公司注册信息
    founder = db.StringField(max_length=30, default='') # 创始人
    founder_desc = db.StringField(max_length=1000, default='') # 创始人介绍 
    registered_capital = db.StringField(max_length=50, default='') # 注册资金
    registered_capital_format = db.IntField(default=0) # 注册资金格式化
    registered_time = db.StringField(max_length=30, default='') # 注册时间 
    company_count = db.StringField(max_length=30, default='') # 法人公司数量
    company_type = db.StringField(max_length=30, default='') # 公司类型
    registration_number = db.StringField(max_length=50, default='') # 工商注册号
    credit_code = db.StringField(max_length=30, default='') # 统一信用代码
    identification_number = db.StringField(max_length=30, default='') # 纳税人识别号
    industry = db.StringField(max_length=30, default='') # 行业
    business_term = db.StringField(max_length=50, default='') # 营业期限
    issue_date = db.StringField(max_length=20, default='') # 核准日期
    registration_authority = db.StringField(max_length=100, default='') # 登记机关
    registered_address = db.StringField(max_length=500, default='') # 注册地址
    scope_business = db.StringField(max_length=2000, default='') # 经营范围
    organization_code = db.StringField(max_length=50, default='') # 组织机构代码

    ## 公司背景(数量)
    key_personnel_count = db.IntField(default=0) # 主要人员
    shareholder_count = db.IntField(default=0) # 股东信息
    investment_abroad_count = db.IntField(default=0) # 对外投资
    annual_return_count = db.IntField(default=0) # 公司年报
    chage_record_count = db.IntField(default=0) # 变更记录
    affiliated_agency_count = db.IntField(default=0) # 分支机构

    ## 公司发展(数量)
    financing_count = db.IntField(default=0) # 融资
    core_team_count = db.IntField(default=0) # 核心团队
    enterprise_business_count = db.IntField(default=0) # 企业业务
    investment_events_count = db.IntField(default=0) # 投资事件
    competitor_count = db.IntField(default=0) # 竞品信息

    ## 司法风险(数量)
    action_at_law_count = db.IntField(default=0) # 法律诉讼
    court_announcement_count = db.IntField(default=0) # 法院公告
    dishonest_person_count = db.IntField(default=0) # 失信人
    person_subject_count = db.IntField(default=0) # 被执行人
    announcement_court_count = db.IntField(default=0) # 开庭公告

    ## 经营风险(数量)
    abnormal_operation_count = db.IntField(default=0) # 经营异常
    administrative_penalty_count = db.IntField(default=0) # 行政处罚
    break_law_count = db.IntField(default=0) # 严重违法
    equity_pledged_count = db.IntField(default=0) # 股权出质
    chattel_mortgage_count = db.IntField(default=0) # 动产抵押
    tax_notice_count = db.IntField(default=0) # 欠税公告
    judicial_sale_count = db.IntField(default=0) # 司法拍卖

    ## 经营状况(数量)
    bid_count = db.IntField(default=0) # 招投标
    tax_rating_count = db.IntField(default=0) # 税务评级
    product_count = db.IntField(default=0) # 产品信息
    import_and_export_credit_count = db.IntField(default=0) # 进出口信用
    certification_count = db.IntField(default=0) # 资质证书
    wx_public_count = db.IntField(default=0) # 公号

    ## 知识产权(数量)
    trademark_count = db.IntField(default=0) # 商标
    patent_count = db.IntField(default=0) # 专利
    software_copyright_count = db.IntField(default=0) # 软件著作权
    works_copyright_count = db.IntField(default=0) # 作品著作权
    icp_count = db.IntField(default=0) # 网站备案

    ## 附加
    tags = db.ListField()   # 标签
    branch = db.StringField(max_length=30, default='') # 分公司数量
    wx_public_no = db.StringField(max_length=200, default='') # 公众号ID
    wx_public = db.StringField(max_length=500, default='') # 公众号名称
    wx_public_qr = db.StringField(max_length=1000, default='') # 公众号二维码

    remark = db.StringField(max_length=1000, default='')   # 备注

    perfect_degree = db.IntField(default=0) # 信息完整度
    craw_count = db.IntField(default=0) # 抓取频次
    kind = db.IntField(default=0)    # 类型: 1.工业设计；2.平面设计；3.--；
    type = db.IntField(default=0)    # 类型: 预设
    craw_user_id = db.IntField(default=0)    # 抓取人ID;

    cida_credit_rating = db.IntField(default=0) # 工业设计协会认证等级: 0.NULL; 1.A; 2.AA; 3.AAA;


    last_on = db.DateTimeField()    # 最后一次抓取时间

    status = db.IntField(default=0)    # 状态: 0.禁用；1.启用
    deleted = db.IntField(default=0)    # 是否软删除

    created_at = db.DateTimeField()
    updated_at = db.DateTimeField()


    def save(self, *args, **kwargs):
        # 生成唯一编号
        self.number = self.gen_number()
        if self.tags and not isinstance(self.tags, list):
            self.tags = self.tags.split(',')
        else:
            self.tags = []

        return super(DesignCompany, self).save(*args, **kwargs)


    def update(self, *args, **kwargs):
        # 移除number
        if 'number' in kwargs.keys():
            kwargs.pop('number')
        if 'tags' in kwargs.keys() and not isinstance(kwargs['tags'], list):
            kwargs['tags'] = kwargs['tags'].split(',')

        return super(DesignCompany, self).update(*args, **kwargs)


    def mark_delete(self):
        return super(DesignCompany, self).update(deleted=1)

    def __unicode__(self):
        return self.name


    @staticmethod
    ## 生成唯一编号
    def gen_number():
        now = datetime.datetime.now().strftime("%y%m%d%H%M%S%f")
        return int(now)

