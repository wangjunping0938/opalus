# -*- coding:utf-8 -*-
import os
import datetime
import time
from flask import current_app
from bson import ObjectId
from . import db
from .base import Base
import re
import random
from app.models.image import Image

# 产品库表- produce
class Produce(Base):
    meta = {
        'collection': 'produce',
        'ordering': ['-created_at'],
        'strict': True,
        'id_field': '_id'
    }
    _id = db.StringField()
    title = db.StringField(max_length=100, default='')  # 标题
    channel = db.StringField(max_length=30, default='')  # 渠道
    url = db.StringField(max_length=500, default='')  # 原文地址
    tags = db.ListField()  # 标签
    color_tags = db.ListField()  # 颜色标签
    brand_tags = db.ListField()  # 品牌标签
    material_tags = db.ListField()  # 材质
    style_tags = db.ListField()  # 风格
    technique_tags = db.ListField()  # 工艺
    other_tags = db.ListField()  # 其它
    total_tags = db.ListField()  # 所有标签
    price = db.StringField(default='')  # 销售价
    currency_type = db.IntField(default=1)  # 币种: 1.RMB；2.美元；3.--；
    designer = db.StringField(max_length=200, default='')  # 设计师
    company = db.StringField(max_length=200, default='')  # 公司
    user_id = db.IntField(default=0)  # 用户ID
    kind = db.IntField(default=1)  # 类型: 1.设计类；5.服装类；
    brand_id = db.IntField(default=0)  # 品牌ID
    prize = db.ListField(default=[])  # 奖项
    category_id = db.IntField(default=0)  # 分类ID
    domain = db.IntField(default=0)  # 领域
    stick = db.IntField(default=0)  # 是否推荐：0.否；1.是；
    stick_on = db.IntField(default=0)  # 推荐时间；
    status = db.IntField(default=1)  # 状态: 0.禁用；1.启用
    remark = db.StringField(max_length=500, default='')  # 描述
    info = db.StringField(max_length=10000, default='')  # 其它json串
    evt = db.IntField(default=1)  # 来源：1.默认; 2.TIAN; 3.LZB; 5.WJP
    random = db.IntField(default=0)  # 生成随机数
    deleted = db.IntField(default=0)  # 是否软删除
    cover_id = db.StringField(default='')  # 封面ID
    editor = db.IntField(default=0)  # 编辑人用户id
    editor_level = db.IntField(default=0)  # 0 未编辑 1 2 编辑程度
    created_at = db.DateTimeField()
    updated_at = db.DateTimeField(default=datetime.datetime.now)

    def cover(self):
        if self.cover_id and len(self.cover_id) == 24:
            image = Image.objects(_id=ObjectId(self.cover_id)).first()
            if image and image.deleted==0:
                return image

        image = Image.objects(target_id=str(self._id), asset_type=2, deleted=0).first()
        if image and image.deleted==0:
            return image

        return None


    def save(self, *args, **kwargs):
        total_tags = []
        # current_app.logger.debug('test')
        if self.tags:
            if not isinstance(self.tags, list):
                self.tags = self.__trans_list(self.tags)
            total_tags += self.tags
        else:
            self.tags = []
        if self.color_tags:
            if not isinstance(self.color_tags, list):
                self.color_tags = self.__trans_list(self.color_tags)
            total_tags += self.color_tags
        else:
            self.color_tags = []

        if self.brand_tags:
            if not isinstance(self.brand_tags, list):
                self.brand_tags = self.__trans_list(self.brand_tags)
            total_tags += self.brand_tags
        else:
            self.brand_tags = []
        if self.material_tags :
            if not isinstance(self.material_tags, list):
                self.material_tags = self.__trans_list(self.material_tags)
            total_tags += self.material_tags
        else:
            self.material_tags = []
        if self.style_tags :
            if not isinstance(self.style_tags, list):
                self.style_tags = self.__trans_list(self.style_tags)
            total_tags += self.style_tags
        else:
            self.style_tags = []
        if self.technique_tags:
            if not isinstance(self.technique_tags, list):
                self.technique_tags = self.__trans_list(self.technique_tags)
            total_tags += self.technique_tags
        else:
            self.technique_tags = []
        if self.other_tags:
            if not isinstance(self.other_tags, list):
                self.other_tags = self.__trans_list(self.other_tags)
            total_tags += self.other_tags
        else:
            self.other_tags = []

        if not self.random:
            self.random = random.randint(1000000, 9999999)

        # 去重
        total_tags = list(set(total_tags))
        # 合并所有标签
        self.total_tags = total_tags
        return super(Produce, self).save(*args, **kwargs)

    def update(self, *args, **kwargs):
        total_tags = self.total_tags
        if 'tags' in kwargs.keys() and not isinstance(kwargs['tags'], list):
            kwargs['tags'] = self.__trans_list(kwargs['tags'])
            total_tags = self.__tags_merge(total_tags, self.tags, kwargs['tags'])
        if 'color_tags' in kwargs.keys() and not isinstance(kwargs['color_tags'], list):
            kwargs['color_tags'] = self.__trans_list(kwargs['color_tags'])
            total_tags = self.__tags_merge(total_tags, self.color_tags, kwargs['color_tags'])
        if 'brand_tags' in kwargs.keys() and not isinstance(kwargs['brand_tags'], list):
            kwargs['brand_tags'] = self.__trans_list(kwargs['brand_tags'])
            total_tags = self.__tags_merge(total_tags, self.brand_tags, kwargs['brand_tags'])
        if 'material_tags' in kwargs.keys() and not isinstance(kwargs['material_tags'], list):
            kwargs['material_tags'] = self.__trans_list(kwargs['material_tags'])
            total_tags = self.__tags_merge(total_tags, self.material_tags, kwargs['material_tags'])
        if 'style_tags' in kwargs.keys() and not isinstance(kwargs['style_tags'], list):
            kwargs['style_tags'] = self.__trans_list(kwargs['style_tags'])
            total_tags = self.__tags_merge(total_tags, self.style_tags, kwargs['style_tags'])
        if 'technique_tags' in kwargs.keys() and not isinstance(kwargs['technique_tags'], list):
            kwargs['technique_tags'] = self.__trans_list(kwargs['technique_tags'])
            total_tags = self.__tags_merge(total_tags, self.technique_tags, kwargs['technique_tags'])
        if 'other_tags' in kwargs.keys() and not isinstance(kwargs['other_tags'], list):
            kwargs['other_tags'] = self.__trans_list(kwargs['other_tags'])
            total_tags = self.__tags_merge(total_tags, self.other_tags, kwargs['other_tags'])

            # 去重
            total_tags = list(set(total_tags))
            # 合并所有标签
            kwargs['total_tags'] = total_tags
        return super(Produce, self).update(*args, **kwargs)

    # 标签整理
    def __tags_merge(self, all_tags, old_tags, new_tags):
        for d in old_tags:
            if d in all_tags:
                all_tags.remove(d)
        all_tags += new_tags
        return all_tags

    # 转列表并去除空
    def __trans_list(self, str):
        list = re.split('[,，]', str)
        if '' in list:
            list.remove('')
        return list

    # 推荐
    def mark_stick(self, evt=1):
        evt = int(evt)
        if evt == 1:
            return super(Produce, self).update(stick=1, stick_on=int(time.time()))
        else:
            return super(Produce, self).update(stick=0)

    # 标记删除
    def mark_delete(self):
        return super(Produce, self).update(deleted=1)

    # 标记恢复
    def mark_recovery(self):
        ok = super(Produce, self).update(deleted=0)
        return ok

    # 彻底删除，同时删除源文件
    def delete(self):
        super(Produce, self).delete()
        # 删除源文件

    def __unicode__(self):
        return self.title
