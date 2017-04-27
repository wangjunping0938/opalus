#!/bin/env python
import pymongo
import sys
client = pymongo.MongoClient('localhost',27017)
db = client.opalus
coll = db.url_list
url = coll.find({"site_from":1}).count()
if url != 0:
	coll.remove({"site_from":1})
	url = coll.find({"site_from":1}).count()
	if url != 0:
		sys.exit(1)
	else:
		sys.exit(0)
else:
	sys.exit(0)
