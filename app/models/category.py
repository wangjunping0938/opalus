import datetime
#from flask.ext.mongoengine.wtf import model_form
from app.models import db
from .base import Base

class Category(Base):

    meta = {
        'increase_key': True,
        'collection': 'category',
        'ordering': ['-created_at'],
        'strict': True,
        'id_field': '_id'
    }

    _id = db.IntField(primary_key=True, required=True, unique=True)
    mark = db.StringField(max_length=20)
    name = db.StringField(max_value=30, required=True, unique=True)
    user_id = db.IntField(required=True)
    kind = db.IntField(default=1) # 类型：1.文档；2.--；3.--
    pid = db.IntField(default=0)
    cid = db.IntField(default=0)
    sort = db.IntField(default=0) # 排序
    status = db.IntField(default=1)
    deleted = db.IntField(default=0)
    remark = db.StringField()

    created_at = db.DateTimeField()
    updated_at = db.DateTimeField(default=datetime.datetime.now)


    def mark_delete(self):
        return super(Category, self).update(deleted=1)

    def __unicode__(self):
        return self.name

    @classmethod
    def category_kind_options(self, kind=0):
        data = [
                {'id':1, 'name': '文档'},
                {'id':2, 'name': '未定义1'},
                {'id':3, 'name': '未定义2'}
            ]

        if kind==0:
            return data
        else:
            for d in data:
                if d['id']==kind:
                    return d
        return {'id': 0, 'name': ''}


    # 获取父级
    @classmethod
    def fetch_parent_options(self, kind=0):
        query = {}
        if kind != 0:
            query['kind'] = int(kind)
        query['pid'] = 0
        data = Category.objects(**query).order_by('-created_at').order_by('-sort').limit(50)

        # 过滤数据
        for i, d in enumerate(data):
            kind_label = '--'
            if d.kind == 1:
                kind_label = '文档'
            if d.kind == 2:
                kind_label = '备用'
                
            data[i].kind_label = kind_label
        return data
        

    def list(self, kind=0, **kwargs):
        query = {}
        if kind != 0:
            query['kind'] = int(kind)
        catetories = Category.objects(**query)
        return catetories



