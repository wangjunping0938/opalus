import datetime
#from flask.ext.mongoengine.wtf import model_form
from app.models import db
from .base import Base
from bson import ObjectId

# 栏目空间表 - column_zone
class ColumnZone(Base):

    meta = {
        'increase_key': False,
        'collection': 'column_zone',
        'ordering': ['-created_at'],
        'strict': True,
        'id_field': '_id'
    }

    _id = db.StringField()
    name = db.StringField(min_value=2, max_value=50, required=True, unique=True)  # 空间标识
    title = db.StringField(min_value=2, max_value=50)  # 空间名称
    user_id = db.IntField(default=0)
    width = db.IntField(default=0)  # 图片宽
    height = db.IntField(default=0) # 图片高
    kind = db.IntField(default=1) # 类型：1.PC；2.备选；3.--
    status = db.IntField(default=1)
    deleted = db.IntField(default=0)
    remark = db.StringField() # 备注

    created_at = db.DateTimeField()
    updated_at = db.DateTimeField(default=datetime.datetime.now)


    # 标记删除
    def mark_delete(self):
        ok = super(ColumnZone, self).update(deleted=1)
        return ok

    # 标记恢复
    def mark_recovery(self):
        ok = super(ColumnZone, self).update(deleted=0)
        return ok

    def __unicode__(self):
        return self.name


