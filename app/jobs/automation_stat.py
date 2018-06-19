# coding: utf-8
from app.extensions import celery
from app.models.company_queu import CompanyQueue
from flask import current_app, jsonify
from app.helpers.common import force_int, force_float_2
from app.jobs.company import create_company
import requests
import json
import time

# 时实更新公司统计
@celery.task()
def auto_company_stat_update():

    page = 1
    perPage = 100
    isEnd = False
    total = 0
    query = {}
    query['status'] = 1
    query['deleted'] = 0

    while not isEnd:
        query['deleted'] = 0
        data = CompanyQueue.objects(**query).order_by('-created_at').paginate(page=page, per_page=perPage)
        if not data:
            print("get data is empty! \n")
            break

        # 过滤数据
        for i, d in enumerate(data.items):
            # 内部统计
            if d.in_grap == 0:
                d.update(in_grap=1)
                # 创建公司
                isCreate = create_company(d.name, {d3in_id: d.d3in_id})
                if not isCreate:
                    d.update(in_grap=2)
                    continue

                isUpdate = d3in_company_one(d3in_id)
                if not isUpdate['success']:
                    d.update(in_grap=2)
                    continue

            # 外部爬取
            elif d.out_grap == 0:
                pass

            print("------------------\n")
            total += 1

        print("current page %s: \n" % page)
        page += 1
        if len(data.items) < perPage:
            isEnd = True
