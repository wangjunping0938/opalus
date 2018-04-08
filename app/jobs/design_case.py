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
    query['deleted'] = 0
    params = {}

    while not isEnd:
        data = DesignCompany.objects(**query).order_by('-created_at').paginate(page=page, per_page=perPage)
        if not data:
            print("get data is empty! \n")
            break

        # 过滤数据
        for i, d in enumerate(data.items):
            # 查看是否含有奖项
            if not d.d3ing_id:
                continue

            print("d3ing_id: %d" % d.d3ing_id)
            params['design_company_id'] = d.d3ing_id

            try:
                r = requests.get(url, params=params)
            except(Exception) as e:
                print(str(e))
                continue

            if not r:
                print('fetch design_case fail!!!')
                continue

            result = json.loads(r.text)
            if not 'meta' in result:
                print("data format error!")
                continue
                
            if not result['meta']['status_code'] == 200:
                print(result['meta']['message'])
                continue

            if not result['data']:
                print('案例作品为空')
                continue

            """
            caseCount = result['meta']['pagination']['total']

            """

            # 统计获奖数量
            caseCount = 0
            redDotAwardCount = 0
            ifAwardCount = 0
            ideaAwardCount = 0
            gmarkAwardCount = 0
            #print(result['data'])
            for m, n in enumerate(result['data']):
                caseCount += 1
                if not 'prizes' in n:
                    print("案例奖项不存在\n")
                    continue


                if n['prizes']:
                    if isinstance(n['prizes'], (list)):
                        awardType = n['prizes'][0]['type']
                    elif isinstance(n['prizes'], (dict)):
                        awardType = n['prizes']['type']
                    else:
                        awardType = 0
                    
                    if awardType == 1:
                        redDotAwardCount += 1
                    if awardType == 2:
                        ifAwardCount += 1
                    if awardType == 3:
                        ideaAwardCount += 1
                    if awardType == 8:
                        gmarkAwardCount += 1
                        

            if not caseCount:
                print("没有案例作品---%s.\n" % d.name)
                continue

            awardRow = {}
            awardRow['d3in_case_count'] = caseCount
            if redDotAwardCount:
                awardRow['red_dot_award_count'] = redDotAwardCount
            if ifAwardCount:
                awardRow['if_award_count'] = ifAwardCount
            if ideaAwardCount:
                awardRow['idea_award_count'] = ideaAwardCount
            if gmarkAwardCount:
                awardRow['gmark_award_count'] = gmarkAwardCount

            #company = DesignCompany.objects()
            ok = d.update(**awardRow)
            if not ok:
                print("更新失败！！！\n")
                continue

            print("更新成功---%s: %s.\n" % (d.name, awardRow))
            total += 1

        print("current page %s: \n" % page)
        page += 1
        if len(data.items) < perPage:
            isEnd = True

    print("is over execute count %s\n" % total)


