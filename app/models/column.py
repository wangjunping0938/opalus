import datetime
#from flask.ext.mongoengine.wtf import model_form
from app.models import db
from app.models.asset import Asset
from .base import Base
from bson import ObjectId

# 栏目表 - column
class Column(Base):

    meta = {
        'increase_key': False,
        'collection': 'column',
        'ordering': ['-created_at'],
        'strict': True,
        'id_field': '_id'
    }

    _id = db.StringField()
    title = db.StringField(max_length=30)  # 标题
    sub_title = db.StringField(max_length=30)  # 副标题
    description = db.StringField()  # 简述
    target = db.StringField(max_length=1000)  # 标记，用于链接跳转或其它
    column_zone_id = db.StringField()  # 空间ID
    user_id = db.IntField(default=0)
    sort = db.IntField(default=0) # 排序
    kind = db.IntField(default=1) # 类型：1.--；2.--；3.--
    cover_id = db.StringField() # 封面ID
    status = db.IntField(default=1) # 是否发布：0.否；1.是；
    deleted = db.IntField(default=0)
    remark = db.StringField() # 备注

    created_at = db.DateTimeField()
    updated_at = db.DateTimeField(default=datetime.datetime.now)

    # 封面
    def cover(self):
        if self.cover_id and len(self.cover_id) == 12:
            asset = Asset.objects(_id=ObjectId(self.cover_id)).first()
            if asset and asset.deleted==0:
                return asset

        asset = Asset.objects(target_id=str(self._id), asset_type=7, deleted=0).first()
        if asset and asset.deleted==0:
            return asset
        return None

    # 标记删除
    def mark_delete(self):
        ok = super(Column, self).update(deleted=1)
        if ok:
            # 删除附件
            assets = Asset.objects(target_id=str(self._id), asset_type=7, deleted=0)
            for item in assets:
                item.mark_delete()


    # 标记恢复
    def mark_recovery(self):
        ok = super(Column, self).update(deleted=0)
        if ok:
            # 恢复附件
            assets = Asset.objects(target_id=str(self._id), asset_type=7, deleted=1)
            for item in assets:
                item.update(deleted=0)

    def __unicode__(self):
        return self.title


