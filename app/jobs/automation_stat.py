# coding: utf-8
from app.extensions import celery
from app.models.company_queue import CompanyQueue
from flask import current_app, jsonify
from app.helpers.common import force_int, force_float_2
from app.jobs.company import create_company, d3in_company_one, award_stat_one
from app.jobs.design_case import d3in_case_one_stat
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
        data = CompanyQueue.objects(**query).order_by('-created_at').paginate(page=page, per_page=perPage)
        if not data:
            print("get data is empty! \n")
            break

        # 过滤数据
        for i, d in enumerate(data.items):
            # 内部统计
            if d.in_grap == 0 or d.in_grap == 2:
                # 创建公司
                param = {}
                param['d3ing_id'] = d.d3in_id
                companyResult = create_company(d.name, **param)
                if not companyResult['success']:
                    d.update(in_grap=2)
                    continue
                print("完成创建公司。..")
                company = companyResult['data']
                # 同步铟果官网数据
                isUpdate = d3in_company_one(d.d3in_id)
                if not isUpdate['success']:
                    d.update(in_grap=2)
                    continue

                print("同步铟果官网数据....")

                # 统计站外奖项信息
                isSyncAward = award_stat_one(company.number)
                print('统计站外奖项...')

                # 统计铟果作品数
                isD3inCase = d3in_case_one_stat(company)
                print("统计铟果作品奖项...")

                d.update(in_grap=5)
                print("更新完成...")

            # 外部爬取
            elif d.out_grap == 0:
                pass

            print("------------------\n")
            total += 1

        print("current page %s: \n" % page)
        page += 1
        if len(data.items) < perPage:
            isEnd = True
