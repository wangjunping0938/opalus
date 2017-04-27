#!/bin/env python
import pymongo
import sys

client = pymongo.MongoClient('localhost',27017)
db = client.opalus
coll = db.url_list
conn = db.product

old_url = len(conn.distinct('url',{"site_from":1}))
new_url = len(coll.distinct('url',{"site_from":1}))

#内容表,地址表都没有数据
if old_url == 0:
	sys.exit(1)
#内容表,地址表数据一致
elif old_url != 0 and new_url <= old_url:
	sys.exit(2)
#内容表有内容且地址有更新
elif old_url != 0 and new_url > old_url:
	sys.exit(3)
else:
	sys.exit(0)
