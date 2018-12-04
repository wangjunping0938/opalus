import datetime
#from flask.ext.mongoengine.wtf import model_form
from app.models import db
from app.models.asset import Asset
from .base import Base
from bson import ObjectId

# 品牌表 - brand
class Brand(Base):

    meta = {
        'increase_key': True,
        'collection': 'brand',
        'ordering': ['-created_at'],
        'strict': True,
        'id_field': '_id'
    }

    _id = db.IntField(primary_key=True, required=True)
    name = db.StringField(min_value=2, max_value=30, required=True, unique=True)  # 品牌名称
    description = db.StringField()
    user_id = db.IntField(default=0)
    kind = db.IntField(default=1) # 类型：1.--；2.--；3.--
    cover_id = db.StringField(default='') # 封面ID
    status = db.IntField(default=1)
    deleted = db.IntField(default=0)
    remark = db.StringField()

    created_at = db.DateTimeField()
    updated_at = db.DateTimeField(default=datetime.datetime.now)

    # 封面
    def cover(self):
        if self.cover_id and len(self.cover_id) == 12:
            asset = Asset.objects(_id=ObjectId(self.cover_id)).first()
            if asset and asset.deleted==0:
                return asset

        asset = Asset.objects(target_id=str(self._id), asset_type=5, deleted=0).first()
        if asset and asset.deleted==0:
            return asset
        return None

    # 标记删除
    def mark_delete(self):
        ok = super(Brand, self).update(deleted=1)
        if ok:
            # 删除附件
            assets = Asset.objects(target_id=str(self._id), asset_type=5, deleted=0)
            for item in assets:
                item.mark_delete()


    # 标记恢复
    def mark_recovery(self):
        ok = super(Brand, self).update(deleted=0)
        if ok:
            # 恢复附件
            assets = Asset.objects(target_id=str(self._id), asset_type=5, deleted=1)
            for item in assets:
                item.update(deleted=0)

    def __unicode__(self):
        return self.name


