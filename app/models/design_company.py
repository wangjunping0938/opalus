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
    name = db.StringField(max_length=50, required=True, unique=True) # 名称
    short_name = db.StringField(max_length=20, default='') # 短名称
    url = db.StringField(max_length=200, default='') # 网址
    logo_url = db.StringField(max_length=200, default='') # LOGO地址
    scale = db.IntField(default=0)    # 公司规模
    scale_label = db.StringField(max_length=20, default='') # 公司规模_label
    nature = db.IntField(default=0)    # 公司性质
    nature_label = db.StringField(max_length=20, default='') # 公司性质_label
    advantage = db.StringField(max_length=10000, default='') # 公司亮点、专业优势
    description = db.StringField(max_length=50000, default='') # 公司描述


    ## 联系信息
    province_id = db.IntField(default=0)    # 省
    province = db.StringField(max_length=20, default='') # 省_label
    city_id = db.IntField(default=0)    # 市
    city = db.StringField(max_length=20, default='') # 市_label
    address = db.StringField(max_length=500, default='') # 详细地址
    zip_code = db.StringField(max_length=10, default='') # 邮编
    contact_name = db.StringField(max_length=20, default='') # 联系人姓名
    contact_phone = db.StringField(max_length=20, default='') # 联系人电话
    contact_email = db.StringField(max_length=200, default='') # 联系人邮箱
    tel = db.StringField(max_length=20, default='') # 公司电话


    ## 附加
    tags = db.ListField()   # 标签
    branch = db.StringField(max_length=20, default='') # 分公司数量
    wx_public_no = db.StringField(max_length=20, default='') # 公众号ID
    wx_public = db.StringField(max_length=30, default='') # 公众号名称
    wx_public_qr = db.StringField(max_length=500, default='') # 公众号二维码

    remark = db.StringField(max_length=200, default='')   # 备注

    perfect_degree = db.IntField(default=0) # 信息完整度
    craw_count = db.IntField(default=0) # 抓取频次
    kind = db.IntField(default=0)    # 类型: 预设
    type = db.IntField(default=0)    # 类型: 预设
    craw_user_id = db.IntField(default=0)    # 抓取人ID：1.军平；2.小董; 3.--;


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

