# -*- coding:utf-8 -*-
import datetime
from . import db
from .base import Base

# 设计公司排行统计表- design_record
class DesignRecord(Base):

    meta = {
        'collection': 'design_record',
        'ordering': ['-created_at'],
        'strict': True,
        'id_field': '_id'
    }

    _id = db.StringField()
    number = db.StringField(max_length=20, default='') # 所属公司编号
    user_id = db.IntField(default=0)    # 用户ID
    mark = db.StringField(max_length=20, default='') # 所属配置标识
    no = db.IntField(default=0) # 统计期数
    type = db.IntField(default=1) # 类型：1.--;
    is_d3in = db.IntField(default=0) # 是否入驻铟果：0.否；1.是；

    ## 不同维度打分
    base_score = db.IntField(default=0)    # 基础分
    business_score = db.IntField(default=0)    # 商业力分
    innovate_score = db.IntField(default=0)    # 创新力分
    design_score = db.IntField(default=0)    # 设计力分
    effect_score = db.IntField(default=0)    # 影响力分
    credit_score = db.IntField(default=0)    # 信誉分

    ## 不同维度详细统计
    base_group = db.DictField() # 基础分组
    business_group = db.DictField() # 商业力组
    innovate_group = db.DictField() # 创新力组
    design_group = db.DictField() # 设计力组
    effect_group = db.DictField() # 影响力组
    credit_group = db.DictField() # 信誉分组

    ## 不同维度平均分（满分100，以最高分为基准）
    base_average = db.IntField(default=0)    # 基础分
    business_average = db.IntField(default=0)    # 商业力分
    innovate_average = db.IntField(default=0)    # 创新力分
    design_average = db.IntField(default=0)    # 设计力分
    effect_average = db.IntField(default=0)    # 影响力分
    credit_average = db.IntField(default=0)    # 信誉分

    ## 总分
    total_score = db.IntField(default=0)    # 总分
    # 总平均分(不用)
    total_ave_score = db.IntField(default=0)
    ## 平均分(百分制)
    ave_score = db.IntField(default=0)

    rank = db.IntField(default=0)   # 排名
    deleted = db.IntField(default=0)    # 软删除
    status = db.IntField(default=1)    # 状态: 0.禁用；1.启用

    created_at = db.DateTimeField()
    updated_at = db.DateTimeField()


    def save(self, *args, **kwargs):
        return super(DesignRecord, self).save(*args, **kwargs)


    def update(self, *args, **kwargs):
        return super(DesignRecord, self).update(*args, **kwargs)


    def mark_delete(self):
        return super(DesignRecord, self).update(deleted=1)

    def __unicode__(self):
        return self.name

