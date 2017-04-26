#!/bin/env python
import pymongo
import sys

client = pymongo.MongoClient('localhost',27017)
db = client.opalus
coll = db.url_list
conn = db.product

old_url = len(conn.distinct('url',{"site_from":1}))
new_url = len(coll.distinct('url',{"site_from":1}))

if old_url == new_url and old_url != 0:
	sys.exit(0)
elif old_url == 0:
	sys.exit(2)
else:
	sys.exit(1)
