# -*- coding:utf-8 -*-
#import datetime
from . import db
from .base import Base

# 公司更新队列表- company_queue
class CompanyQueue(Base):

    meta = {
        'collection': 'company_queue',
        'ordering': ['-created_at'],
        'strict': True,
        'id_field': '_id'
    }

    _id = db.StringField()
    d3in_id = db.IntField(default=0)    # 铟果公司ID
    number = db.StringField()    # 唯一标识
    name = db.StringField(max_length=50, required=True) # 公司名称
    kind = db.IntField(default=0)    # 类型: 
    type = db.IntField(default=0)    # 类型: 预设
    remark = db.StringField(max_length=1000)   # 备注

    in_grap = db.IntField(default=0) # 站内抓取进度: 0.未抓取；1.抓取中；5.完成；
    out_grap = db.IntField(default=0) # 站外抓取进度: 0.未抓取；1.抓取中；5.完成；
    tyc_status = db.IntField(default=0) # 天眼查 抓取进度: 0.未抓取；1.抓取中；2.失败；5.完成；
    bd_status = db.IntField(default=0) # 百度 抓取进度: 0.未抓取；1.抓取中；2.失败；5.完成；

    grap_times = db.IntField(default=0) # 追加次数
    last_on = db.DateTimeField()    # 最后一次追加时间

    status = db.IntField(default=0)    # 状态: 0.禁用；1.启用
    deleted = db.IntField(default=0)    # 是否软删除

    created_at = db.DateTimeField()
    updated_at = db.DateTimeField()


    def mark_delete(self):
        return super(CompanyQueue, self).update(deleted=1)

    def __unicode__(self):
        return self.name

