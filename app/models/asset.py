# -*- coding:utf-8 -*-
import datetime
import os
from . import db
from .base import Base
from flask import current_app

# 附件表- asset
class Asset(Base):

    meta = {
        'collection': 'asset',
        'ordering': ['-created_at'],
        'strict': True,
        'id_field': '_id'
    }

    _id = db.StringField()
    name = db.StringField(max_length=50) # 文件名称
    path = db.StringField(max_length=100) # 本地文件路径
    mime = db.StringField(max_length=10) # 文件类型
    ext = db.StringField(max_length=10) # 后缀名
    size = db.IntField(default=0)    # 大小
    width = db.IntField(default=0)    # 宽
    height = db.IntField(default=0)    # 高
    user_id = db.IntField(default=0)    # 用户ID
    domain = db.StringField(max_length=20) # 所属域
    asset_type = db.IntField(default=1)    # 图片类型: 1.后台上传；5.品牌logo；7.栏目封面；8.--；
    target_id = db.StringField(default='') # 关联ID
    kind = db.IntField(default=1)    # 类型:
    status = db.IntField(default=1)    # 状态: 0.禁用；1.启用
    remark = db.StringField(max_length=500, default='')  # 描述
    deleted = db.IntField(default=0)    # 是否软删除

    created_at = db.DateTimeField()
    updated_at = db.DateTimeField(default=datetime.datetime.now)

    # 获取七牛路径
    def get_thumb_path(self):
        asset_url = current_app.config['ASSET_URL']
        path = self.path
        if not path:
            return None

        row = {
            'sm': os.path.join(asset_url, path + '-sm'),
            'mi': os.path.join(asset_url, path + '-mi'),
            'bi': os.path.join(asset_url, path + '-bi'),
            'avs': os.path.join(asset_url, path + '-avs'),
            'avm': os.path.join(asset_url, path + '-avm'),
            'avb': os.path.join(asset_url, path + '-avb'),
        }
        return row

    # 标记删除
    def mark_delete(self):
        return super(Asset, self).update(deleted=1)

    # 彻底删除，同时删除源文件
    def delete(self):
        from app.helpers.asset import remove_qiniu
        super(Asset, self).delete()
        # 删除源文件
        remove_qiniu(self.path)

    def __unicode__(self):
        return self.name

