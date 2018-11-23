from elasticsearch import Elasticsearch
from pymongo import MongoClient

class MogoCl:
    def __init__(self,ip,data_base,collection):
        self.moncl = MongoClient(ip,27017)
        self.db = self.moncl[data_base]
        self.collection = self.db[collection]
    # 从mongodb 中查询数据
    def query_all(self):
        return self.collection.find()


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
    def post_index_data(self,action):
        res = self.es.index(index="index_test", doc_type="doc_type_test", body=action)
        print(res)


obj = ElasticObj()
obj.create_index()
moncl = MogoCl('127.0.0.1','opalus','image')
for i in moncl.query_all():
    i.pop('_id')
    obj.post_index_data(i)


