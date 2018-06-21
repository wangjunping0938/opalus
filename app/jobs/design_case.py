# coding: utf-8
from app.extensions import celery
from app.models.design_case import DesignCase
from app.models.design_company import DesignCompany
from flask import current_app, jsonify
import requests
import json


# 获取铟果设计案例数据并统计 -- 全部
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
            result = d3in_case_core(d)
            if not result['success']:
                continue

            print("更新成功---%s: %s.\n" % (d.name, result['data']))
            total += 1

        print("current page %s: \n" % page)
        page += 1
        if len(data.items) < perPage:
            isEnd = True

    print("is over execute count %s\n" % total)


# 获取铟果设计案例数据并统计 -- 单个
@celery.task()
def d3in_case_one_stat(d):
    result = d3in_case_core(d)
    return result


# 获取铟果设计案例数据并统计--core
@celery.task()
def d3in_case_core(d):
    result = {'success': False, 'message': ''}
    # 查看是否含有奖项
    if not d.d3ing_id:
        result['message'] = 'd3in_id 不存在!'
        return result

    print("d3ing_id: %d" % d.d3ing_id)
    params = {}
    params['design_company_id'] = d.d3ing_id

    try:
        r = requests.get(url, params=params)
    except(Exception) as e:
        print(str(e))
        result['message'] = str(e)
        return result

    if not r:
        print('fetch design_case fail!!!')
        result['message'] = 'fetch design_case fail!!!'
        return result

    res = json.loads(r.text)
    if not 'meta' in res:
        print("data format error!")
        res['message'] = 'data format error!'
        return result
        
    if not res['meta']['status_code'] == 200:
        print(res['meta']['message'])
        result['message'] = res['meta']['message']
        return result

    if not res['data']:
        print('案例作品为空')
        result['message'] = '案例作品为空'
        return result

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
    for m, n in enumerate(res['data']):
        caseCount += 1
        if not 'prizes' in n:
            print("案例奖项不存在\n")
            result['message'] = '案例奖项不存在'
            return result

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
        result['message'] = '没有案例作品'
        return result

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

    ok = d.update(**awardRow)
    if not ok:
        print("更新失败！！！\n")
        result['message'] = '更新失败！！！'
        return result

    result['success'] = True
    result['data'] = awardRow
    return result
