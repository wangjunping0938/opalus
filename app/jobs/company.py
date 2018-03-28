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
            print(str(e))
            continue

        if not r:
            print('fetch info fail!!!')
            continue

        result = json.loads(r.text)
        if not 'meta' in result:
            print("data format error!")
            continue
            
        if not result['meta']['status_code'] == 200:
            print(result['meta']['message'])
            continue

        for i, d in enumerate(result['data']):
            if not d['company_name']:
                continue
            print("公司名称: %s" % d['company_name'])
            company = DesignCompany.objects(name=d['company_name']).first()
            if not company:
                continue
            query = {}
            query['d3ing_id'] = d['id']
            # 简称
            if d['company_abbreviation']:
                query['short_name'] = d['company_abbreviation']
            # 分公司数量
            if d['branch_office']:
                query['branch'] = str(d['branch_office'])
            # 英文名称
            if d['company_english']:
                query['english_name'] = d['company_english']
            # 规模
            if d['company_size']:
                query['scale'] = d['company_size']
                query['scale_label'] = d['company_size_val']
            # 网址
            if d['web']:
                query['url'] = d['web']
            # LOGO
            if d['logo_image']:
                query['logo_url'] = d['logo_image']['logo']
            ## 联系信息
            if d['province_value']:
                query['province'] = d['province_value']
            if d['city_value']:
                query['city'] = d['city_value']
            if d['address']:
                query['address'] = d['address']
            if d['contact_name'] and not company['contact_name']:
                query['contact_name'] = d['contact_name']
            if d['phone'] and not company['contact_phone']:
                query['contact_phone'] = d['phone']
            if d['email'] and not company['contact_email']:
                query['contact_email'] = d['email']


            print("更新字段: %s" % query)

            if not query:
                continue
            ok = company.update(**query)
            if not ok:
                continue
            print("公司存在: %d" % d['id'])
            print("-----------\n")
            total += 1

        print("current page %s: \n" % page)
        page += 1
        params['page'] = page
        if len(result['data']) < perPage:
            isEnd = True
                
    print("is over execute count %s\n" % total)


# 获取铟果设计公司数据并统计
@celery.task()
def export_design_center():
    provinceStr = """
    杭州奥格工业设计有限公司
    杭州跨界科技有限公司
    杭州飞神工业设计有限公司
    杭州领跑者工业设计有限公司
    温州中胤时尚鞋服设计有限公司
    浙江飞灵飞逊服饰有限公司
    浙江宝鼎服装设计有限公司
    绍兴光大芯业微电子有限公司
    浙江工业大学义乌科学技术研究院有限公司
    杭州汉度工业设计有限公司
    杭州上林电子科技有限公司
    杭州斯帕克造型艺术有限公司
    杭州热浪工业产品设计有限公司
    杭州源骏工业产品设计有限公司
    宁波大业产品造型艺术设计有限公司
    宁波科创制造技术开发有限公司
    宁波东方船舶设计院有限公司
    浙江思珀整合传播有限公司
    浙江力诺流体控制科技股份有限公司
    海宁市海涛时装创意设计有限公司
    浙江皇城工坊文化发展有限公司
    浙江斐络工业设计有限公司
    台州市黄岩博创工业设计有限公司
    台州市一锐工业设计有限公司
    浙江中科联创工业设计基地
    杭州瑞德设计有限公司
    杭州飞鱼工业设计有限公司
    杭州博乐工业产品设计有限公司
    杭州凸凹工业设计有限公司
    圣泓工业设计创意有限公司
    宁波市鄞州德来特技术有限公司
    温州市创力电子有限公司
    浙江欣海船舶设计研究院有限公司
    舟山万达船舶设计有限公司
    台州市韵点工业设计有限公司
    宁波和丰创意广场投资经营有限公司
    杭州经纬天地创意投资有限公司
    杭州和达文化创意产业园管理有限公司
    浙江乐富创意产业投资有限公司
    桐乡濮院针织产业园区开发建设有限公司
    马鞍山市必拓工业设计有限公司
    芜湖佳景科技有限公司
    安徽协同创新设计研究院有限公司
    安徽深装合大工业设计有限公司
    宜昌市微特电子设备有限公司
    武汉华夏星光工业产品设计有限公司
    湖北壹峰文化传媒有限公司
    武汉光谷楚创空间工业设计有限公司
    武汉光谷楚创空间工业设计有限公司
    湖北壹峰文化传媒有限公司
    宜昌市微特电子设备有限公司
    武汉光谷楚创空间工业设计有限公司
    湖北壹峰文化传媒有限公司
    宜昌市微特电子设备有限公司
    重庆优擎科技有限公司
    重庆蓝海时代产品设计有限公司
    重庆杜塞科技有限公司
    江苏鼎艺国际文化创意产业有限公司
    苏州奥杰汽车技术股份有限公司
    南通贝斯特船舶与海洋工程设计有限公司
    中国（长沙）创新设计产业园
    武汉光谷楚创空间工业设计有限公司
    湖北壹峰文化传媒有限公司
    宜昌市微特电子设备有限公司
    东风设计研究院有限公司
    武汉金玺广告有限公司
    武汉华夏星光工业产品设计有限公司
    郑州市浪尖产品设计有限公司
    郑州一诺工业产品设计有限公司
    广州市沅子工业产品设计有限公司
    深圳市中世纵横设计有限公司
    深圳洛可可工业设计有限公司
    深圳创新设计研究院有限公司
    江门市艾迪赞工业设计有限公司
    广东企盟工业设计有限公司
    佛山市青鸟工业设计有限公司
    广州市大业产品设计有限公司
    深圳市浪尖设计有限公司
    广东华南工业设计院
    中山市优力加工业设计有限公司
    """

    countryStr = """
    东道品牌创意集团有限公司
    阿尔特汽车技术股份有限公司
    杭州飞鱼工业设计有限公司
    德艺文化创意集团股份有限公司
    北京全路通信信号研究设计院集团有限公司
    秦皇岛玻璃工业研究设计院
    山西太钢工程技术有限公司
    上海龙创汽车设计股份有限公司
    江苏东方创意文化产业有限公司
    杭州瑞德设计股份有限公司
    厦门市拙雅科技有限公司
    东风设计研究院有限公司
    大连四达高技术发展有限公司
    深圳市浪尖设计有限公司
    北京洛可可科技有限公司
    沈阳创新设计服务有限公司
    上海指南工业设计有限公司
    泉州迪特工业产品设计有限公司
    """

    provinceCount = 0
    countryCount = 0

    # 省级统计
    provinceArr = provinceStr.split('\n')
    provinceArr = []

    print("totla province count: %d\n" % len(provinceArr))
    for d in provinceArr:
        name = d.strip()
        print(name)
        company = DesignCompany.objects(name=name).first()
        if not company:
            continue
        ok = company.update(is_design_center=1)
        if not ok:
            continue
        provinceCount += 1
        print("update success!\n")

    print("province success count: %d\n" % provinceCount)


    # 国家级统计
    countryArr = countryStr.split('\n')
    countryArr = []

    print("totla country count: %d\n" % len(countryArr))
    for d in countryArr:
        name = d.strip()
        print(name)
        company = DesignCompany.objects(name=name).first()
        if not company:
            continue
        ok = company.update(is_design_center=2)
        if not ok:
            continue
        countryCount += 1

    print("country success count: %d\n" % countryCount)



  


        


