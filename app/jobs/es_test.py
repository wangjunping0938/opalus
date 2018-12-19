from elasticsearch import Elasticsearch
import os
import sys

sys.path.append(os.path.abspath(os.path.dirname("__file__")))
from app.models.image import Image
from app.extensions import celery
from app.env import cf
from manage import create_app

app = create_app()


class ElasticObj:
    def __init__(self, ip="127.0.0.1"):
        self.index_name = 'opalus'
        self.index_type = 'image'
        # 无用户名密码状态
        self.es = Elasticsearch([ip])
        # 用户名密码状态
        # self.es = Elasticsearch([ip],http_auth=('elastic', 'password'),port=9200)

    # 创建索引
    def create_index(self):
        # 索引是否存在
        if self.es.indices.exists(index=self.index_name) is not True:
            res = self.es.indices.create(self.index_name)
            print(res)

    # 往es中插入数据
    def post_index_data(self, action):
        res = self.es.index(index=self.index_name, doc_type=self.index_type, body=action)
        print(res)


@celery.task()
def insert_data():
    query = {}
    page = 1
    per_page = 100
    is_end = False
    total = 1
    while not is_end:
        # 倒序
        data = Image.objects(**query).order_by('created_at').paginate(page=page, per_page=per_page)
        if not len(data.items):
            print("get data is empty! \n")
            break
        for i, image in enumerate(data.items):
            obj = ElasticObj()
            obj.create_index()
            print(type(image))
            # image['id'] = str(image['_id'])
            # image.pop('_id')
            # obj.post_index_data(image)
        total += 1
        print("current page %s: \n" % page)
        page += 1
        if len(data.items) < per_page:
            is_end = True
    print("is over execute count %s\n" % total)


insert_data()
