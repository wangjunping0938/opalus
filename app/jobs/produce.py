import time
import os
import sys

sys.path.append(os.path.abspath(os.path.dirname("__file__")))
from flask import current_app
from app.models.produce import Produce
from app.helpers.common import gen_mongo_id
from app.extensions import celery
from app.env import cf
import requests

# 批量修改
@celery.task()
def produce_update():

    page = 1
    perPage = 100
    isEnd = False
    successStatCount = 0
    failStatCount = 0
    query = {}
    #query['deleted'] = 0
    #query['kind'] = 1
    #query['status'] = 1
    #query['channel'] = 'g_mark'
    #query['total_tags'] = '女装'

    while not isEnd:
        data = Produce.objects(**query).order_by('-created_at').paginate(page=page, per_page=perPage)
        if not data:
            print("get data is empty! \n")
            continue

        # 过滤数据
        for i, d in enumerate(data.items):
            #img_url = d.img_url.strip()
            #if d.channel == 'g_mark':
            if True:
                ok = True
                #ok = d.update(random=r)
                if ok:
                    successStatCount += 1
                else:
                    failStatCount += 1

        print("current page %s: \n" % page)
        page += 1
        if len(data.items) < perPage:
            isEnd = True

    print("is over execute SuccessCount %d ---- failCount: %d\n" % (successStatCount, failStatCount))

