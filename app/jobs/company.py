# coding: utf-8
from app.extensions import celery
from app.models.design_case import DesignCase
from app.models.design_company import DesignCompany
from flask import current_app, jsonify
import requests
import json

# 统计奖项数量
@celery.task()
def award_stat():
    
    page = 1
    perPage = 100
    isEnd = False
    total = 0
    query = {}

    while not isEnd:
        query['deleted'] = 0
        data = DesignCompany.objects(**query).order_by('-created_at').paginate(page=page, per_page=perPage)
        if not data:
            print("get data is empty! \n")
            break

        # 过滤数据
        for i, d in enumerate(data.items):
            # 查看是否含有奖项
            caseCount = DesignCase.objects(target_id=str(d.number)).count()
            if caseCount > 0:
                c = DesignCompany.objects(number=d.number).first()
                print("%s case_count: %d" % (d.name, caseCount))

                # 更新总数量
                if d.design_case_count < caseCount:
                    c.update(design_case_count=caseCount)

                # 更新不同奖项数
                awardArr = [['红星奖', 'red_star_award_count'], ['中国红棉奖', 'innovative_design_award_count'], ['中国好设计奖', 'china_design_award_count'], ['中国设计智造大奖', 'dia_award_count']]
                for aw in awardArr:
                    sCount = DesignCase.objects(target_id=str(d.number), prize_label=aw[0]).count()
                    if sCount > 0:
                        if c:
                            print("update %s: %d" % (aw[0], sCount))
                            c.update(**{aw[1]: sCount})

                print("------------------\n")
                total += 1

        print("current page %s: \n" % page)
        page += 1
        if len(data.items) < perPage:
            isEnd = True

    print("is over execute count %s\n" % total)


# 获取铟果设计公司数据并统计
@celery.task()
def d3in_company_stat():
    url = "%s/%s" % (current_app.config['D3INGO_URL'], 'opalus/company/list')

    page = 1
    perPage = 100
    isEnd = False
    total = 0
    params = {}
    params['type_status'] = 1
    params['type_verify_status'] = 1
    params['per_page'] = perPage

    while not isEnd:

        try:
            r = requests.get(url, params=params)
        except(Exception) as e:
            break
            print(str(e))

        if not r:
            break
            print('fetch info fail!!!')

        result = json.loads(r.text)
        if not 'meta' in result:
            break
            print("data format error!")
            
        if not result['meta']['status_code'] == 200:
            break
            print(result['meta']['message'])

        for i, d in enumerate(result['data']):
            print("公司名称: %s" % d['company_name'])
            total += 1

        print("current page %s: \n" % page)
        page += 1
        params['page'] = page
        if len(result['data']) < perPage:
            isEnd = True
                
    print("is over execute count %s\n" % total)


        


