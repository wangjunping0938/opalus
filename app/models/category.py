import datetime
#from flask.ext.mongoengine.wtf import model_form
from app.models import db
from app.models.base import *

class Category(db.Document):

    meta = {
        'collection': 'category',
        'ordering': ['-created_at'],
        'strict': True,
        'id_field': '_id'
    }

    _id = db.IntField(primary_key=True, required=True, unique=True)
    mark = db.StringField(max_length=20)
    name = db.StringField(max_value=30, required=True, unique=True)
    user_id = db.IntField(required=True)
    kind = db.IntField(default=1) # 类型：1.平台；2.--；3.--
    pid = db.IntField(default=0)
    cid = db.IntField(default=0)
    status = db.IntField(default=1)
    deleted = db.IntField(default=0)
    remark = db.StringField()

    created_at = db.DateTimeField()
    updated_at = db.DateTimeField(default=datetime.datetime.now)


    def save(self, *args, **kwargs):
        if not self.created_at:
            self.created_at = datetime.datetime.now()
        if not self.updated_at:
            self.updated_at = datetime.datetime.now()

        # ID 自增
        sequence = Sequence._get_collection()
        sequence = sequence.find_one_and_update({'name':'category_id'}, {'$inc':{'val':1}}, upsert=True)
        self._id = sequence['val']
        return super(Category, self).save(*args, **kwargs)

    def update(self, *args, **kwargs):
        self.updated_at = datetime.datetime.now()
        kwargs['updated_at'] = datetime.datetime.now()
        return super(Category, self).update(*args, **kwargs)

    def mark_delete(self):
        return super(Category, self).update(deleted=1)

    def __unicode__(self):
        return self.name

    @classmethod
    def category_kind_options(self, kind=0):
        data = [
                {'id':1, 'name': '平台'},
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

    def list(self, kind=0, **kwargs):
        query = {}
        if kind != 0:
            query['kind'] = int(kind)
        catetories = Category.objects(query)
        return catetories



