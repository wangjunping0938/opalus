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

    ## 基本信息
    name = db.StringField(max_length=50) # 名称
    short_name = db.StringField(max_length=20) # 短名称
    url = db.StringField(max_length=200) # 网址
    logo_url = db.StringField(max_length=200) # LOGO地址
    size = db.IntField(default=0)    # 公司规模
    size_label = db.StringField(max_length=20) # 公司规模_label
    nature = db.IntField(default=0)    # 公司性质
    nature_label = db.StringField(max_length=20) # 公司性质_label
    advantage = db.StringField(max_length=1000) # 公司亮点、专业优势
    description = db.StringField(max_length=1000) # 公司描述


    ## 联系信息
    province_id = db.IntField(default=0)    # 省
    province = db.StringField(max_length=20) # 省_label
    city_id = db.IntField(default=0)    # 市
    city = db.StringField(max_length=20) # 市_label
    address = db.StringField(max_length=500) # 详细地址
    zip_code = db.StringField(max_length=10) # 邮编
    contact_name = db.StringField(max_length=20) # 联系人姓名
    contact_phone = db.StringField(max_length=20) # 联系人电话
    contact_email = db.StringField(max_length=200) # 联系人邮箱
    tel = db.StringField(max_length=20) # 公司电话


    ## 附加
    tags = db.ListField()   # 标签
    branch = db.IntField(default=0) # 分公司数量
    wx_public_no = db.StringField(max_length=50) # 公众号ID

    remark = db.StringField(max_length=200)   # 备注

    perfect_degree = db.IntField(default=0) # 信息完整度
    craw_count = db.IntField(default=0) # 抓取频次
    kind = db.IntField(default=0)    # 类型: 预设
    type = db.IntField(default=0)    # 类型: 预设
    craw_user_id = db.IntField(default=0)    # 抓取人ID：1.军平；2.董永胜; 3.--;


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
        if 'tags' in kwargs.keys() and not isinstance(kwargs['tags'], list):
            kwargs['tags'] = kwargs['tags'].split(',')
        else:
            kwargs['tags'] = []

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

