# coding: utf-8
from app.extensions import celery
from app.models.design_case import DesignCase
from app.models.design_company import DesignCompany
from flask import current_app, jsonify
import requests
import json


# 获取铟果设计案例数据并统计
@celery.task()
def d3in_case_stat():

    page = 1
    perPage = 100
    isEnd = False
    total = 0
    url = "%s/%s" % (current_app.config['D3INGO_URL'], 'opalus/design_case/list')
    query = {}

    while not isEnd:
        query['deleted'] = 0
        data = DesignCompany.objects(deleted=0).order_by('-created_at').paginate(page=page, per_page=perPage)
        if not data:
            print("get data is empty! \n")
            break

        # 过滤数据
        for i, d in enumerate(data.items):
            # 查看是否含有奖项
            if not d.d3ing_id:
                continue

            query['design_company_id'] = d.d3ing_id

            try:
                r = requests.get(url, params=params)
            except(Exception) as e:
                continue
                print(str(e))

            if not r:
                continue
                print('fetch design_case fail!!!')

            result = json.loads(r.text)
            if not 'meta' in result:
                continue
                print("data format error!")
                
            if not result['meta']['status_code'] == 200:
                continue
                print(result['meta']['message'])

            caseCount = result['meta']['pagination']['total']
            if not caseCount:
                continue

            #company = DesignCompany.objects()
            ok = d.update(design_case_count=caseCount)
            if not ok:
                print("更新失败！！！\n")
                continue

            print("更新成功---%s: %d.\n" % (d.name, caseCount))
            total += 1

        print("current page %s: \n" % page)
        page += 1
        if len(data.items) < perPage:
            isEnd = True

    print("is over execute count %s\n" % total)


