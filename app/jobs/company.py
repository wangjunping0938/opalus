# coding: utf-8
from app.extensions import celery
from app.models.design_case import DesignCase
from app.models.design_company import DesignCompany
from flask import current_app, jsonify
from app.helpers.common import force_int, force_float_2
import requests
import json
import time

# 创建/更新公司信息
@celery.task()
def create_company(name, **options):
    query = {}
    if not name:
        return False
    query['name'] = name
    item = DesignCompany.objects(name=name).first()
    if not item:
        options['name'] = name
        item = DesignCompany(**options)
        ok = item.save()
        if not ok:
            return False
    return True

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
            continue

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
            # 简介
            if d['company_profile']:
                query['description'] = d['company_profile']
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


# 初始化字段
@celery.task()
def init_company():
    
    page = 1
    perPage = 100
    isEnd = False
    total = 0
    query = {}
    query['deleted'] = 0
    query['status'] = 0
    query['craw_user_id'] = 0

    while not isEnd:
        data = DesignCompany.objects(**query).order_by('-created_at').paginate(page=page, per_page=perPage)
        if not data:
            print("get data is empty! \n")
            continue

        row = {
            'short_name': '',
            'english_name': '',
            'url': '',
            'logo_url': '',
            'scale': 0,
            'scale_label': '',
            'nature': 0,
            'nature_label': '',
            'company_status_label': '',
            'advantage': '',
            'description': '',
            'is_high_tech': 0,
            'ty_score': 0,
            'ty_view_count': 0,
            'design_case_count': 0,
            'd3in_case_count': 0,
            'red_star_award_count': 0,
            'innovative_design_award_count': 0,
            'china_design_award_count': 0,
            'dia_award_count': 0,
            'if_award_count': 0,
            'red_dot_award_count': 0,
            'idea_award_count': 0,
            'gmark_award_count': 0,
            'province_id': 0,
            'province': '',
            'city_id': 0,
            'city': '',
            'address': '',
            'zip_code': '',
            'contact_name': '',
            'contact_phone': '',
            'contact_email': '',
            'tel': '',
            'founder': '',
            'founder_desc': '',
            'registered_capital': '',
            'registered_capital_format': 0,
            'registered_time': '',
            'company_count': '',
            'company_type': '',
            'registration_number': '',
            'credit_code': '',
            'identification_number': '',
            'industry': '',
            'business_term': '',
            'issue_date': '',
            'registration_authority': '',
            'registered_address': '',
            'scope_business': '',
            'organization_code': '',
            'key_personnel_count': 0,
            'shareholder_count': 0,
            'investment_abroad_count': 0,
            'annual_return_count': 0,
            'chage_record_count': 0,
            'affiliated_agency_count': 0,
            'financing_count': 0,
            'core_team_count': 0,
            'enterprise_business_count': 0,
            'investment_events_count': 0,
            'competitor_count': 0,
            'action_at_law_count': 0,
            'court_announcement_count': 0,
            'dishonest_person_count': 0,
            'person_subject_count': 0,
            'announcement_court_count': 0,
            'abnormal_operation_count': 0,
            'administrative_penalty_count': 0,
            'break_law_count': 0,
            'equity_pledged_count': 0,
            'chattel_mortgage_count': 0,
            'tax_notice_count': 0,
            'judicial_sale_count': 0,
            'bid_count': 0,
            'tax_rating_count': 0,
            'product_count': 0,
            'import_and_export_credit_count': 0,
            'certification_count': 0,
            'wx_public_count': 0,
            'trademark_count': 0,
            'patent_count': 0,
            'software_copyright_count': 0,
            'works_copyright_count': 0,
            'icp_count': 0,
            'tags': [],
            'branch': '',
            'wx_public_no': '',
            'wx_public': '',
            'wx_public_qr': '',
            'remark': '',
            'perfect_degree': 0,
            'craw_count': 0,
        }

        # 过滤数据
        for i, d in enumerate(data.items):
            company = DesignCompany.objects(_id=d._id).first()
            try:
                #ok = company.update(**row)
                ok = True
                if not ok:
                    print("更新失败: %s\n" % company.name)
                    continue

                #time.sleep(0.05)
                print("更新成功: %s\n" % company.name)
                total += 1
            except(Exception) as e:
                print(str(e))
                continue

        print("current page %s: \n" % page)
        page += 1
        if len(data.items) < perPage:
            isEnd = True

    print("is over execute count %s\n" % total)

  
# 根据提供的公司名称创建公司
@celery.task()
def generate_company():
    data = []
    str = """
    品物（上海）工业产品设计顾问有限公司
    北京上品极致产品设计有限公司
    北京华新意创工业设计有限公司
    北京品物堂产品设计有限公司
    杭州领跑者工业设计有限公司
    上海木马工业产品设计有限公司
    杭州飞鱼工业设计有限公司
    杭州凸凹工业设计有限公司
    杭州博乐工业设计股份有限公司
    北京木马工业设计有限公司
    广州市大业产品设计有限公司
    上海威曼工业产品设计有限公司
    青岛图灵设计顾问有限公司
    北京智加问道科技有限公司
    杭州热浪工业产品设计有限公司
    杭州源骏工业产品设计有限公司
    杭州汉度工业设计有限公司
    同点设计策划（深圳）有限公司
    深圳市佳简几何工业设计有限公司
    深圳宝嘉能源有限公司
    佛山市柏飞特工业设计有限公司
    佛山市顺德区宏翼工业设计有限公司
    杭州奥格工业设计有限公司
    杭州斯帕克工业设计有限公司
    深圳旗鱼工业设计有限公司
    宁波大业产品造型艺术设计有限公司
    广东顺德东方麦田工业设计有限公司
    深圳市鼎典工业产品设计有限公司
    深圳市上善工业设计有限公司
    深圳云一创新科技有限公司
    深圳市矩阵工业产品设计有限公司
    上海柏菲工业产品设计有限公司
    上海指南工业设计有限公司
    深圳市雷骏科技有限公司
    深圳比例文化发展有限公司
    杭州亿智智能科技有限公司
    厦门伊亚创新科技有限公司
    慈溪瑞普工业产品设计有限公司
    天盯科技（深圳）有限公司有限公司
    深圳市凯旋创新品牌产品设计有限公司
    柯怡工业设计
    合肥市方块工业设计有限公司
    上海艺凯设计有限公司
    佛山市顺德区鼎纳设计有限公司
    东莞市尚同工业设计有限公司
    深圳白色产品设计有限公司
    上海天狐创意设计股份有限公司
    广东顺德潜龙工业设计有限公司
    北京米帮科技有限公司
    深圳市设际邹工业设计有限公司
    易迪思工业设计顾问（上海）有限公司
    宁波艺加意工业设计有限公司
    上海创骋工业设计有限公司
    广州市沅子工业产品设计有限公司
    宁波卓一工业设计有限公司
    佛山市青鸟工业设计有限公司
    台州市梦工厂工业设计有限公司
    永康市一搏工业产品设计有限公司
    上海博路工业设计有限公司
    考克（福建）工业设计有限公司
    宁波明锐工业产品设计有限公司
    泉州迪特工业产品设计有限公司
    深圳市白狐工业设计有限公司
    艺可意工业设计（北京）有限公司
    武汉华夏星光工业产品设计有限公司
    山东鼎意工业设计有限公司
    陕西阿米工业设计有限公司
    深圳宇朔工业设计有限公司
    深圳市万有引力工业设计有限公司
    深圳市美霖工业设计有限公司
    佛山市典石工业设计有限公司
    深圳市冰点工业设计有限公司
    深圳市嘉升藤工业创新设计有限公司
    深圳市德嘉工业产品造型设计有限公司
    深圳大国智造设计有限公司
    深圳市浪恒工业设计有限公司
    深圳市英派来工业设计有限公司
    深圳市卡蒙工业产品设计有限公司
    台湾无限设计有限公司深圳分部(原联邦设计)
    深圳市名之鹰工业设计有限公司
    深圳市拓腾世纪工业设计有限公司
    深圳市霸王设计有限公司
    深圳善本致和工业设计有限公司
    深圳瞬尖工业设计工作室
    深圳市笔尖之上设计有限公司
    深圳洛斯奇工业设计有限公司
    深圳市雷明工业设计有限公司
    成都拓成工业产品设计有限公司
    佛山达奇工业设计有限公司
    深圳市博拉图工业设计有限公司
    无锡简约工业产品设计有限公司
    深圳市牧本工业设计有限公司
    深圳市禾马工业产品设计有限公司
    深圳市巴哈伊工业设计有限公司
    深圳市四象工业设计有限公司
    深圳市畅为工业设计有限公司
    深圳市融一工业设计有限公司
    深圳市人本意匠工业产品设计有限公司
    深圳市派尔工业设计有限公司
    深圳市元拓工业产品设计有限公司
    深圳市麦锡工业产品策划有限公司
    深圳市零零柒工业产品设计有限公司
    深圳市森渡工业产品设计有限公司
    深圳市蓝鲸工业产品造型开发设计有限公司
    深圳市久鸿工业设计有限公司
    深圳市国龙工业设计有限公司
    深圳市鑫科工业产品设计中心
    深圳市艾姆思杰工业产品设计有限公司
    深圳市擎天开拓工业设计有限公司
    深圳市百份一工业产品设计有限公司
    深圳市瀚翔工业设计有限公司
    深圳市源创尚品工业设计有限公司
    深圳市凯博工业产品设计有限公司
    深圳市心雷工业产品设计有限公司
    深圳市索艺工业产品设计有限公司
    深圳市子午线工业产品造型设计有限公司
    成都艾玛工业设计有限公司
    深圳市中佰工业设计有限公司
    深圳市银河工业产品设计有限公司
    深圳市怡美工业设计有限公司
    深圳市壹零壹工业设计有限公司
    深圳市无限空间工业设计有限公司
    深圳市问鼎工业设计有限公司
    深圳市东旭产品设计有限公司
    深圳市东来工业产品造型设计有限公司
    深圳市东海浪潮工业设计有限公司
    深圳市迪特格工业产品设计有限公司
    深圳市大典工业产品设计有限公司
    深圳市艾德方工业产品设计有限公司
    创世零壹工业设计(深圳)有限公司
    深圳市绿创工业设计有限公司
    上海甲秀工业设计有限公司
    上海意田工业设计公司
    富乐工业设计（上海）有限公司
    陈慎任工业设计有限公司
    上海泛思工业设计有限公司
    浩汉工业产品设计(上海)有限公司
    上海高图工业设计有限公司
    齐思工业设计咨询(上海)有限公司
    千方工业设计（上海）有限公司
    上海意图工业设计有限公司
    上海贺风工业产品设计有限公司
    上海极星工业设计有限公司
    喜多俊之工业产品设计咨询（上海）有限公司
    上海溯洄工业产品设计有限公司
    广州市科途工业产品设计有限公司
    东莞市品臣工业设计有限公司
    广州乐玛工业产品设计有限公司
    深圳市康源工业设计有限公司
    深圳市品悟工业设计有限公司
    南京欧爱工业设计
    宁波市昊物设计
    中山市尚物工业设计
    佛山市顺德古今工业设计有限公司
    深圳市贝贝高工业设计有限公司
    长沙九十八号工业设计有限公司
    深圳汉诺威设计有限公司
    佛山市顺德区唯点工业设计
    佛山基准工业设计有限公司
    熊松工业设计有限公司
    广东顺德极目工业设计有限公司
    壹格工业产品策划(顺德)有限公司
    艾迪工业设计有限公司
    佛山市蓝翼创想工业设计有限公司
     佛山市简奥工业设计有限公司
    无锡帝造工业设计
    深圳石头智慧工业设计有限公司
    深圳市黑谷工业设计有限公司
    深圳市伊诺工业设计有限公司
    深圳市四六区工业产品策划有限公司
    佛山久形工业设计有限公司
    成都思睿工业设计有限公司
    南京灵犀工业设计有限公司
    广州哈士奇产品设计有限公司
    天瑞联创（北京）科技发展有限公司
    天津意道思考工业产品设计有限公司
    广州亿豪电子科技有限公司
    深圳市盼兮科技有限公司
    佛山市风锐工业设计有限公司
    广州物原工业设计有限公司
    深圳锐致设计
    佛山市集品工业设计有限公司
    深圳市氧气设计服务有限公司
    广州品一产品设计有限公司
    广东顺德心雷工业产品策划有限公司
    广东顺德米壳工业设计有限公司
    上海余木工业设计有限公司
    东莞市一花一木工业设计有限公司
    深圳市新丝路设计有限公司
    成都市火熊科技有限责任公司
    杭州象天工业设计有限公司
    杭州九合形物工业设计有限公司
    深圳艺有道创新设计有限公司
    北京盒而特科技有限公司
    杭州顾道工业设计有限公司
    深圳市甲由设计顾问机构有限公司
    汇智工业产品设计公司
    无锡锐意工业设计有限公司
    宁波意得工业设计有限公司
    深圳二十一克产品设计有限公司
    东莞市意玛工业设计有限公司
    东莞意象工业设计有限公司
    深圳市岸木工业设计有限公司
    武汉也琪工业设计有限公司
    上海坚果工业产品设计有限公司
    玛雅工业设计有限公司
    温州红点工业产品设计中心
    佛山市雪兰工业设计有限公司
    温州左岸工业设计
    广东顺德和壹设计咨询有限公司
    上海意途工业产品设计有限公司
    杭州易舍工业产品设计有限公司
    意浪产品设计工作室
    杭州淘博工业设计有限公司
    上海索果工业设计公司
    上海扬舟工业设计有限公司
    上海巍德工业产品设计有限公司
    上海时创工业产品设计有限公司
    深圳市东川工业设计有限公司
    深圳ENVO银河设计公司
    上海方宇工业设计有限公司
    上海岸峰工业产品设计有限公司
    上海约兹工业产品设计有限公司
    佛山市顺德区德腾工业设计有限公司
    深圳市创意格林设计有限公司
    上海飞米工业设计有限公司
    上海木创
    为肯工业设计公司
    沃和丘工业设计（上海）有限公司
    Geedesign
    天津思度工业设计
    10的n次方
    华新产品设计有限公司
    青岛普睿谷设计有限公司
    深圳富思豪工业设计有限公司
    深圳智造工业设计有限公司
    深圳市金标源创工业设计有限公司
    深圳市道集工业设计有限公司
    熔点设计有限公司
    广州朗威工业设计有限公司
    北京简盟产品设计有限公司
    滨湖区巴木创意设计中心
    北京奥思工业设计有限公司
    Kaleidoscope (美资万花筒)设计公司
    唐恩（北京）产品设计研发有限公司
    杭州鸿鹄工业设计有限公司
    宁波左右设计
    杭州水者工业设计有限公司
    北京赛佳图工业设计有限公司
    海飞工业设计有限公司
    深圳市唯可设计咨询有限公司
    创恒工业设计室
    苏州原点工业设计有限公司
    杭州腾赢工业设计有限公司
    宁波柯怡工业设计有限公司
    凝意工业设计有限公司
    深圳感叹号产品设计有限公司
    深圳市青花工业产品设计有限公司
    深圳市艾度工业设计有限公司
    宁波易尚工业产品设计有限公司
    橙果工业设计有限公司
    杭州奔汉工业设计有限公司
    深圳市鸿领工业产品策划设计有限公司
    广州大道工业设计有限公司
    佛山市顺德区三力工业设计有限公司
    广州大宇工业设计有限公司
    上海呈创工业产品设计有限公司
    苏州斑马工业设计有限公司
    深圳市红点工业设计有限公司
    北京零靖创新产品设计顾问
    宁波易凡工业设计有限公司
    皓景（中山古镇/佛山顺德）设计有限公司
    山东蓝逊工业设计公司
    宁波道和工业设计有限公司
    深圳市道影工业设计有限公司
    朱古力设计咨询（深圳)有限公司
    深圳启元设计有限公司
    杭州金瑞工业产品设计有限公司
    一川设计广州有限公司
    深圳市灰度工业设计有限公司
    佛山市大震工业设计有限公司
    昆山市雪莱工业产品设计有限公司
    幻想设计上海中心
    台州市黄岩先驱设计有限公司
    泉州育成工业产品设计有限公司
    深圳市禾尔马工业产品设计有限公司
    杭州艾迪工业产品设计有限公司
    温州东帝工业设计有限公司
    永康市原野工业产品设计有限公司
    淮安帝欧工业设计有限公司
    深圳市灵井工业设计有限公司
    无锡易辰工业设计有限公司
    青岛上和产品设计
    北京格物乐道科技有限公司
    中山黑火设计有限公司
    合众工业设计有限公司
    广州涟漪工业设计有限公司
    佛山市顺德区容桂道可工业设计
    迪然工业设计
    深圳正钧尚设计咨询有限公司
    北京波普新创工业设计
    南通万喜至工业设计有限公司
    东莞万喜至工业设计
    东莞市柏森工业设计有限公司
    鼎丰家庭用品（南京）有限公司（深圳分公司）
    深圳卓源工业设计有限公司
    戊名工业设计有限公司
    南京博创工业产品设计有限公司
    杭州宗匠工业设计有限公司
    永康市无印尚品产品设计有限公司
    无锡无极限工业设计有限公司
    慈溪市飞扬工业产品设计有限公司
    天津角度工业产品设计有限公司
    深圳市太阳森林工业设计有限公司
    人本造物（广州）产品设计有限公司
    慈溪市合一工业设计有限公司
    广州维博产品设计有限公司
    拙雅科技有限公司
    深圳市橄榄树工业设计有限公司
    杭州博达设计咨询有限公司
    易用（广州/郑州/广西）设计有限公司
    深圳鑫奇石工业设计公司
    佛山市形科工业设计有限公司
    上海汉猿工业产品设计有限公司（在宁波也有办公点）
    广东东莞布鲁斯工业设计有限公司（在青岛和意大利有公司）
    深圳市橙子工业设计有限公司
    江苏省淮安品向工业设计有限公司
    深圳市知行创新工业设计有限公司
    宁波艺佳意工业设计有限公司
    南京本物工业设计有限公司
    北京首时工业设计有限公司
    北京锦簇工业设计有限责任公司 
    北京益为工业设计有限公司
    北京尚品格工业设计有限公司
    北京云沌工业设计有限公司
    北京锦澄嘉创工业设计有限公司
    斐鲁萨工业设计（北京）有限公司
    中瑞德科（北京）工业设计有限公司
    北京金典致晟工业设计有限公司
    易造工业设计（北京）有限公司
    北京艾摩讯工业设计有限公司 
    北京迪希工业设计创意开发有限公司
    艺可意工业设计（北京）有限公司 
    北京点易工业设计有限公司
    异向国际工业设计（北京）有限公司 
    北京世纪摩玛工业设计有限公司
    北京想想再工业设计有限公司
    北京千策良品工业设计有限公司
    北京宇朔创意工业设计有限责任公司
    北京东秩创新工业设计有限公司
    北京航天真科工业设计有限公司
    博砚清艺（北京）工业设计有限公司
    北京思乘创新工业设计有限公司
    菲迪拉（北京）工业设计有限公司
    北京天创易造工业设计有限公司
    北京原点高健工业设计有限公司
    米可创新工业设计（北京）有限责任公司
    深圳市亚克斯设计有限公司
    郑州越尚工业设计有限公司
    上海都市工业设计中心有限公司
    沈阳梵天工业设计有限公司
    圣泓工业设计创意有限公司
    浙江高越工业设计有限公司
    杭州飞神工业设计有限公司
    山东东华未来工业设计有限公司
    厦门大端工业设计有限公司
    宿迁优博工业设计有限公司
    江苏亿鑫工业设计有限公司
    苏州大上工业设计有限公司
    青岛宙庆工业设计有限公司
    武汉光谷楚创空间工业设计有限公司
    山东创瑞工业设计有限公司
    安徽后青春工业设计研究院有限公司
    昆山纽斯步工业设计有限公司
    泉州盈佳图工业设计有限公司
    苏州致幻工业设计有限公司
    合肥维卡工业设计有限公司
    深圳市八千里工业设计有限公司
    青岛舜维工业设计有限公司
    浦乐博工业设计有限公司
    山东创融工业设计有限公司
    北京安迪智慧工业设计有限公司
    北京万象创新工业设计有限公司
    北京品意工业设计有限公司
    北京凡朴工业设计有限公司
    北京空间无限工业设计有限公司
    北京梦树工业设计有限公司
    北京彩格工业设计有限公司
    北京橙点工业设计有限公司
    北京同基原点工业产品设计中心
    北京心觉工业设计有限责任公司
    北京科之华工业设计有限公司
    瑞观智选工业设计（北京）有限公司
    北京伯原明禄工业设计有限公司
    北京博物新智工业产品设计有限公司
    北京大尘工业设计有限责任公司
    思睿维度（北京）工业设计有限公司
    北京亚美森工业设计有限公司
    北京微智达工业设计有限公司
    北京艺有道工业设计有限公司
    北京辐轩工业设计有限公司
    松小屋工业设计（北京）有限公司
    贰拾叁（北京）工业设计有限责任公司
    意匠工业设计（北京）有限责任公司
    北京爱灵思工业设计有限公司
    北京艾欧克工业产品设计发展有限公司
    北京东西创新工业设计有限公司
    北京元品工业设计有限公司
    北京灵动空间工业设计有限公司
    北京梦想者工业设计有限公司
    北京艺宇工业设计有限公司
    成都意町工业产品设计有限公司
    成都匠造工业设计有限公司
    四川嘉泰工业产品设计有限责任公司
    成都蓝豚工业设计有限公司
    成都思睿工业产品设计有限公司
    成都沙苑工业产品设计有限公司
    成都爱笛迩工业产品设计有限公司
    成都品粹工业设计服务有限公司
    成都虹达工业产品设计有限公司
    成都铭鉴工业产品设计有限公司
    成都厚生工业设计有限公司
    成都天开工业设计有限公司
    四川睿深工业产品设计有限公司
    成都鸿瑞达工业设计有限公司
    成都几合工业产品设计有限公司
    成都优逸工业设计有限公司
    成都英莱工业设计有限公司
    成都鹈鹕工业设计有限公司
    成都物语工业设计有限公司
    四川蓝格工业设计有限公司
    德阳市艾璐工业设计有限公司
    成都埃森工业产品设计有限公司
    成都九十度工业产品设计有限公司
    成都市白色工业产品设计有限公司
    成都朗立工业产品设计有限公司
    绵阳灵锐意匠工业设计有限公司
    成都普瑞玛工业产品设计有限公司
    成都倬睿工业设计有限公司
    成都西之铭工业设计有限公司
    成都厘米工业设计有限公司
    成都几美工业产品设计有限公司
    四川天鸟工业设计有限责任公司
    成都完形工业设计有限公司
    成都于悦工业设计有限公司
    成都色空工业设计有限公司
    绵阳菲尔工业设计科技有限公司
    成都三千水上工业产品设计有限公司
    成都云尚创意工业产品设计有限公司
    成都奥创工业设计有限公司
    成都天问工业设计有限公司
    河北唐韵工业设计有限公司
    河北洛普工业设计有限公司
    河北启创工业设计有限公司
    河北智佳工业设计有限公司
    河北翼源工业设计有限公司
    秦皇岛北木工业设计有限公司
    石家庄简佳工业设计有限公司
    秦皇岛豪洁尚森工业产品设计有限公司
    保定市巨橙工业设计有限公司
    沧州意达工业设计服务有限公司
    保定可大可为工业产品设计有限公司
    天津戴维工业设计有限公司
    天津希图工业产品设计有限公司
    天津汉德工业设计有限公司
    天津埃迪森工业产品设计有限公司
    天津市爱迪工业设计有限公司
    天津爱谷工业设计有限公司
    天津麦田工业产品设计有限公司
    天津挚诚必诚工业产品设计有限公司
    天津北欧工业设计研发有限公司
    天津立达工业产品设计有限公司
    天津金戈工业设计有限公司
    天津北马工业设计有限公司
    天津兴杰工业设计有限公司
    天津凯迪工业设计有限公司
    天津知物工业设计有限公司
    天津阿尔特工业产品设计有限公司
    天津维立方工业设计有限公司
    天津中森工业设计有限公司
    天津京汉工业设计有限公司
    天津锜创工业设计有限公司
    天津思度工业设计有限公司
    天津嘿十工业设计有限公司
    天津意生天工业设计有限公司
    天津明觉创物工业产品设计有限公司
    天津伟度工业设计有限公司
    天津美格工业设计有限公司
    天津韵点工业设计有限公司
    天津艾迪工设工业设计有限公司
    天津市创恒工业产品设计有限公司
    天津市普凡工业设计有限公司
    苏州博弈工业产品设计有限公司
    南京贝奇工业设计有限公司
    常州市天高工业设计有限公司
    苏州云尚工业设计有限公司
    南京英达迪赛工业设计有限公司
    苏州新天地工业产品设计有限公司
    无锡迪可工业设计有限公司
    无锡阿维工业设计有限公司
    南京虎步工业设计有限公司
    无锡奥泰克工业设计有限公司
    无锡名迪工业设计有限公司
    江苏锐度品牌策划有限公司
    苏州市和谐康工业设计有限公司
    江苏美图工业设计有限公司
    宿迁市创智工业设计有限公司
    江苏新源工业设计咨询有限公司
    无锡普菲特工业产品设计有限公司
    苏州优诺工业设计有限公司
    苏州维卡工业设计有限公司
    苏州麦唯多工业设计有限公司
    无锡雷蒙德工业设计有限公司
    无锡创瀚工业设计有限公司 
    无锡尚格工业设计有限公司
    常州简奥工业设计有限公司
    常州市六零九零工业设计有限公司
    常州优易工业设计有限公司
    常州智丰工业设计有限公司
    无锡阳通工业设计有限公司
    南通润昌工业设计有限公司
    无锡海润达工业设计有限公司
    南京奇汇享工业设计有限公司
    南京中汇工业产品设计有限公司
    苏州智道通工业设计有限公司
    太仓耀泰工业设计有限公司
    无锡在创工业设计有限公司
    常州市鼎坊工业产品设计有限公司
    苏州爱信达工业设计有限公司
    扬州蓝极工业设计有限公司
    南京品象工业设计有限公司
    南京尚诺工业设计有限公司
    无锡品源工业设计有限公司
    南京摩屉工业设计有限公司
    苏州意展工业设计有限公司
    苏州昆仑工业设计有限公司
    江苏创品工业设计有限公司
    苏州阿尔西工业设计有限公司
    江苏万喜至工业设计有限公司
    江苏江鹤工业设计有限公司
    江苏奥成工业设计有限公司
    江苏紫东工业设计服务有限公司
    苏州晶智鑫工业产品设计有限公司
    连云港小桔灯工业设计有限公司
    江苏仓海工业设计有限公司
    江苏智泉工业设计有限公司
    苏州傲途工业设计有限公司
    宿迁市艺新工业设计有限公司
    无锡市帝造工业设计有限公司
    金箍棒工业产品设计江阴有限公司
    常州中航达索工业设计有限公司
    常州英钠微特工业设计有限公司
    苏州汇诚智造工业设计有限公司
    徐州晨鸣工业设计有限公司
    南京苏博工业设计有限公司
    南京翔睿工业设计有限公司
    无锡蜜蜂工业设计有限公司
    南京捷悠工业设计有限公司
    常州元道工业设计有限公司
    南京多喜工业设计有限公司
    苏州萨伯工业设计有限公司
    无锡最印象工业设计有限公司
    苏州飓风工业设计有限公司
    徐州水滴石工业设计有限公司
    南通壹选工业设计有限公司
    昆山蓝鼎工业设计有限公司
    宿迁市简一工业设计有限公司
    淮安市艾迪斯工业设计有限公司
    南京亚爱帝工业设计有限公司
    苏州迪赞工业设计有限公司
    淮安品向工业设计有限公司
    南通尚工工业设计有限公司
    南京睿德工业设计有限公司
    无锡思迪工业设计有限公司
    常州五色谱工业设计有限公司
    无锡鼎辉工业设计有限公司
    南京先拓工业设计有限公司
    南京汉星工业设计有限公司
    苏州流金工业设计有限公司
    南京怡觉工业设计有限公司
    苏州意中人工业设计有限公司
    常州浦氏工业设计有限公司
    苏州之所以工业设计有限公司
    无锡优弧工业设计有限公司
    无锡观悦工业设计有限公司
    苏州微格工业设计有限公司
    无锡卓悦工业设计有限公司
    南京桑榆工业设计有限公司
    苏州之意工业设计有限公司
    无锡玛佐工业设计有限公司
    常州攀高工业设计有限公司
    南京知物工业设计有限公司
    徐州凌云工业设计有限公司
    常州维度工业设计有限公司
    苏州风迷工业设计有限公司
    常州市齐天工业设计有限公司
    苏州千寻工业设计有限公司
    南通齐阳工业设计有限公司
    苏州红尘天工业设计有限公司
    无锡市猛犸工业设计有限公司
    无锡市寸园工业设计有限公司
    南京欲见工业设计有限公司
    南京古檤工业设计有限公司
    太原拾佳伯乐工业设计有限公司
    太原一品思创工业设计有限公司
    山西中远工业创意设计有限责任公司
    太原卓创工业设计咨询有限公司
    重庆集创家工业设计有限公司
    重庆安福汇工业设计有限公司
    重庆戌日东升工业产品设计有限公司
    重庆道合工业设计有限公司
    重庆索奇工业设计有限公司
    重庆捷途工业设计有限公司
    重庆嘉立豪工业设计有限公司
    重庆集智创享工业设计有限公司
    重庆绿箩轩工业产品设计有限公司
    重庆维根工业设计有限公司
    重庆奥力新工业设计有限公司
    重庆在线工业设计有限公司
    重庆锦恩纳图工业设计中心
    重庆睿捷工业设计有限公司
    重庆巍颐工业产品设计有限责任公司
    重庆神龙尺工业设计有限公司
    重庆木子木工业设计有限公司
    重庆意衡工业设计有限公司
    重庆同捷工业设计有限公司
    重庆腾通工业设计有限公司
    重庆雯兰工业设计有限公司
    重庆新派工业设计有限公司
    重庆沃德工业设计有限公司
    重庆瀚智工业设计有限公司
    重庆净土工业设计有限公司
    重庆博捷工业设计有限公司
    重庆金诺工业设计有限公司
    重庆焕译工业产品设计有限公司
    重庆杰欧工业设计有限公司
    重庆合艺工业设计有限公司
    青岛沃尔工业设计有限公司
    山东久和工业设计有限公司
    青岛中南工业设计有限公司
    青岛科海创新工业设计有限公司
    青岛匦居工业设计服务有限公司
    青岛蓝晶工业设计有限公司
    青岛中家院工业设计有限公司
    青岛佳佰纳工业设计有限公司
    青岛众设计工业设计有限公司
    青岛利达创新工业设计有限公司
    青岛可爱工业设计有限公司
    青岛博源工业设计有限公司
    青岛长策工业产品设计咨询有限公司
    青岛木马工业设计有限公司
    济南宙庆工业设计有限公司
    青岛高迪工业设计有限公司
    青岛拜特工业设计有限公司
    山东后现代工业设计有限公司
    青岛汉华工业设计有限公司
    日照工业设计中心有限公司
    青岛佳乐智安工业设计有限公司
    山东曈睿工业设计有限公司
    淄博象外工业设计有限责任公司
    山东标恒雷根工业设计有限公司
    青岛沃尔德工业设计有限公司
    山东巨象工业设计有限公司
    山东帝三七工业设计有限公司
    Gee-design
    朱古力设计咨询(深圳)有限公司
    中山尚物工业设计有限公司
    浙江中科联创工业设计有限公司
    彦辰设计（深圳）有限公司  
    武汉奥思工业设计有限公司
    沃伦设计（上海）有限公司
    温州先临左岸工业设计有限公司
    万象设计江苏有限责任公司
    天盯科技（深圳）有限公司
    斯巴科（北京）科技有限公司
    曙光信息产业股份有限公司
    深圳市中世纵横设计有限公司
    深圳市源创尚品工业设计有限公司 
    深圳市映山红模型设计有限公司 
    深圳市意谷设计有限公司 
    深圳市王者设计有限公司  
    深圳市盛世长城工业设计有限公司 
    深圳市洛可可工业设计有限公司
    深圳市立桥产品设计有限公司  
    深圳市浪尖设计有限公司
    深圳市浪尖工业产品造型设计有限公司 
    深圳市飓风电子产品外形设计有限公司 
    深圳市嘉兰图设计有限公司
    深圳市嘉兰图工业设计有限公司 
    深圳市红度工业产品策划有限公司 
    深圳市灏域设计有限公司  
    深圳市汉诺威设计有限公司 
    深圳市海维海工业设计有限公司 
    深圳市格林工业设计有限公司 
    深圳市宝嘉能源有限公司
    深圳市巴哈伊工业设计有限公司 
    上海为肯工业设计公司
    上海木码艺术设计有限公司
    上海木马工业设计有限公司
    上海木创工业设计发展有限公司
    上海洛可可整合设计有限公司
    上海龙域工业设计有限公司
    上海龙创汽车设计股份有限公司
    上海汉猿工业产品设计有限公司
    上海迪然工业设计有限公司
    山东汇强重工科技有限公司
    厦门市拙雅科技有限公司
    青岛海高设计制造有限公司
    宁波蓝领工业科技有限公司
    宁波大业设计有限公司
    麦田致尚（北京）工业设计有限公司
    马鞍山江东工业设计发展有限公司
    开思工业设计（杭州）有限公司
    江苏潜能工业设计有限公司
    江苏蒎圣屋工业科技有限公司
    合肥为先产品设计有限公司
    杭州正负极工业设计有限公司
    杭州序点工业产品设计有限公司
    杭州新晟工业设计有限公司
    杭州未末工业设计有限公司
    杭州微原素工业设计有限公司
    杭州微客工业产品设计有限公司
    杭州天恩工业设计有限公司
    杭州提格科技有限公司
    杭州膳佳家居用品有限公司
    杭州瑞德设计股份有限公司
    杭州朴上寸村文化艺术有限公司
    杭州木心设计机构
    杭州摩斯凯文工业产品设计有限公司
    杭州联动工业产品设计有限公司
    杭州跨界科技有限公司
    杭州爵品工业设计有限公司
    杭州火虫工业产品设计有限公司
    杭州合西行工业设计有限公司
    杭州格瑞斯工业设计有限公司
    杭州浮岸工业设计有限公司
    杭州风向工业设计有限公司
    杭州菲尔造型艺术设计有限公司
    杭州非同工业产品设计有限公司
    杭州博乐工业产品设计有限公司
    杭州柏树工业产品设计有限公司
    广州易用设计有限公司
    广东东莞布鲁斯工业设计有限公司
    福乐门（上海）工业设计有限公司
    佛山市大业工业设计有限公司
    佛山卡蛙电子科技有限公司
    佛山简奥工业设计有限公司
    东莞艺加意工业设计有限公司
    鼎丰家庭用品（南京）有限公司
    慈溪大业工业设计有限公司
    创世零壹工业设计(深圳)有限公司 
    重庆福瑞兰达科技有限公司
    北京洛可可科技有限公司
    北京迪沃客文化创意有限公司
    """
    l = str.split('\n')
    l = []
    for i in l:
        name = i.strip()
        if name:
            try:
                design_company = DesignCompany.objects(name=name).first()
                # 如果存在，则跳过
                if design_company:
                    print("公司已存在: %s" % name)
                    continue

                design_company = DesignCompany(name=name, kind=1)
                ok = True
                #ok = design_company.save()
                if ok:
                    print("创建成功: %s\n" % name)
                else:
                    print("创建失败: %s\n" % name)
            except(Exception) as e:
                print(e)


# 根据提供的公司名称创建公司--平面设计
@celery.task()
def generate_plane_company():
    data = []
    str = """
    重庆桔禾文化创意策划有限公司	https://www.juheplan.com
    刘宾品牌咨询与设计	http://www.lewbin.com
    重庆王双企业形象设计有限公司	http://www.wsdesign.cc
    重庆创写广告有限公司	http://www.cqcxgg.com
    重庆优道品牌设计广告有限公司	http://www.udaoo.net
    重庆茁麦文化传播有限公司	http://www.dreambc.com
    五觉品牌设计公司	http://www.cq5jdesign.com
    重庆朗优品牌设计有限公司	http://www.longu1.com
    重庆西略文化传播有限公司	http://www.xlccbrand.com
    重庆德纳图广告有限公司	http://www.denato.com.cn
    北京主动一点平面设计有限公司	http://www.59ilogo.com.cn/
    北京正邦品牌设计公司	http://www.zhengbang.com.cn/
    北京东道形象设计制作有限责任公司	http://www.dongdao.net/
    北京早晨设计顾问有限公司	www.morningdesign.com.cn
    深圳韩家英设计公司	http://www.hanjiaying.com
    北京理想创意艺术设计有限公司	http://www.bjideal.com
    北京始创国际企划有限公司	http://www.aici.cn
    深圳朗图企业形象设计有限公司	http://www.rito.cn
    石家庄晏钧设计工作室	http://www.yanjun.net
    成都黑蚁设计有限责任公司	http://www.blackant.cn
    上海梅高创意咨询有限公司	http://www.meikao.com
    天津艺点意创科技有限公司	http://www.vipyidian.com/
    北京朗顿设计顾问有限公司	http://www.randodesign.com
    高塔品牌管理（北京）有限公司	http://www.gaota.cn
    上海十树品牌管理咨询有限公司	http://www.shishubrand.com/
    李华清国际品牌设计有限公司	http://www.lihuaqing.com
    北京灵智飞扬广告有限公司	http://www.lingzhifeiyang.cn
    深圳市南风盛世企业形象策划有限公司	http://www.sznfss.com
    北京清美未来广告设计有限公司	http://www.highestchina.com
    北京形意达艺术设计有限公司	http://www.x-yd.com
    上海博尚包装设计有限公司	http://www.posher.cn
    柏林视觉品牌顾问（北京）有限公司	http://www.blvisual.com
    北京东方尚企业策划设计有限公司	http://www.dongfangshang.com
    杭州巴顿品牌设计有限公司	http://www.hzvis.com
    广州集和品牌顾问有限公司	http://www.bicobrand.com
    众耀伟业文化发展（北京）有限公司	http://www.zpopdesign.com
    美御品牌设计	http://www.mroyal.cn
    北京吾言吾道品牌咨询有限公司	http://www.shejidesign.com
    陈幼坚设计公司	www.alanchandesign.com
    北京妙集国际广告设计有限公司	http://www.miaojibrand.com/
    北京博创高地国际广告设计有限公司	http://www.boflydesign.com
    靳刘高设计	http://www.klandk.com
    深圳优华氏企业形象设计有限公司	http://www.eovas.net
    广州和一品牌设计顾问有限公司	http://www.bibrand.com
    李永铨设计有限公司	http://www.tommylidesign.com
    上海博微设计有限公司	http://www.bfitbrand.com
    上海沈浩鹏平面设计有限公司	http://www.hopesun.com
    杭州兰龙品牌设计有限公司	http://www.vislogo.com
    深圳市锐意纵横品牌策划有限公司	http://www.ryzhch.cn
    柯力品牌设计（上海）有限公司	http://www.kelidesign.com
    济南干将莫邪企业形象设计有限公司	http://www.123ci.com
    深圳市伙伴传祺创意设计有限公司	http://www.shenzhensheji.com/
    上海三松品牌策划设计有限公司	http://www.sunsonchina.com/
    上海硕谷品牌设计有限公司	http://www.gsvis.com
    深圳力锐品牌策划有限公司	http://www.laserbrand.hk/
    深圳市火狼企业形象设计有限公司	http://www.fw119.com/
    正午设计顾问有限公司	http://www.12-brand.com
    北京中美视觉文化传播有限公司	http://www.zhongmeishijue.net
    深圳市欧兰格广告设计有限公司	http://www.olgmedia.com/
    深圳市卓纳设计有限公司	http://www.zona.cn
    深圳市牛势广告有限公司	http://www.szniushi.com
    上海火太阳品牌设计有限公司	http://www.flamesun.com/
    上海欧赛斯文化创意有限公司	http://www.osens.cn
    深圳幕恩品牌设计有限公司	http://www.moonbrand.cn
    深圳市陈宋品牌顾问有限公司	http://www.csbrand.cn
    沈阳熙云谷企业形象设计有限公司	http://www.xiyungu.com/
    北京兰旗之道文化发展有限公司	http://www.lanqi.com
    宁波市海曙形而上广告设计有限公司	http://www.sensbc.com
    雅能品牌策划设计公司	http://www.enengcy.com
    DDG设计有限公司	http://www.ddg.com.tw
    无锡市菩提树品牌设计有限公司	http://www.pts99.com
    广东华丽时代品牌设计顾问有限公司	http://www.gtall.cn
    杭州重墨堂品牌设计有限公司	http://www.zmt.cn/
    苏州零全设计有限公司	http://www.newtree.cn
    惠州市威碧恩设计有限公司	http://www.vbn.hk/
    四川古格王朝品牌设计顾问公司	http://www.ycguge.com
    成都费思道文化传播有限公司	http://www.feisidao.com
    青岛弘睿品牌管理顾问有限公司	http://www.hr1949.com/
    索曼斯(新疆)设计咨询有限公司	http://www.sommesedesign.com
    大连精睿创想设计有限公司	http://www.jingruicehua.com
    成都奥动品牌设计传播有限公司	http://www.adonschina.com
    长春市大马品牌设计有限公司	http://www.damabrand.cn
    创意共和（大连）设计有限公司	http://www.ideacn.com
    逗号品牌顾问服务机构	http://www.dohao.cn
    深圳心铭舍设计顾问有限公司	http://www.xinming.sg
    深圳晴朗品牌设计机构	http://www.smiledesign.cn
    深圳市全力形象设计有限公司	http://www.szquanli.com
    广州甲壳虫设计有限公司	http://www.gzjkc.com
    杭州朗威品牌策划有限公司	http://www.lkg.cc
    赤风品牌策划与设计有限公司	http://www.redwind.cn
    贤草品牌顾问有限公司	http://www.visdom.cn
    天津深度广告传播有限责任公司	http://www.sigad.com.cn
    念相品牌设计咨询（上海）有限公司	http://www.nx-design.net
    唯秀企业形象策划(上海)有限公司	http://www.vshow.net
    石家庄尚品牌设计有限公司	http://www.spinpai.com
    石家庄一横设计传播有限公司	http://www.1heng.net/
    石家庄乐观品牌设计有限公司	http://www.woleguan.com
    石家庄合一品牌设计顾问有限公司	http://herovi.lofter.com
    河北美格广告有限公司	http://www.zkingbrand.com
    河北零度视点设计顾问有限公司	http://www.zerovision.com.cn
    林佑品牌设计有限公司	http://www.linyousheji.com
    石家庄上维企划设计公司	http://www.cn-sunv.com
    后众设计有限公司	http://www.hero-ad.com
    上海上知营销策划有限公司	http://www.soundsplan.com
    朗意品牌管理顾问有限公司	http://www.lonbrand.com
    广州哲仕企业形象设计有限公司	http:/www.thisbrand.cn
    龙堂品牌设计与传播有限公司	http://www.helloddc.com
    广州知尖广告有限公司	http://betop365.com
    观唐-途创品牌策划设计有限公司	http://www.2umj.com/home.html
    联合创智广州广告公司	http://www.nfyxtime.com
    海智狮锐广告有限公司	http://www.hzbrand.cn/about.asp?sortid=1
    深圳市红苹果企业形象策划有限公司	http://www.szredapple.cn/
    深圳北辰品牌设计有限公司	http://www.brandstardesign.com
    深圳市标派视觉品牌设计有限公司	http://www.szbpvis.com
    左右格局（深圳）品牌整合创新体	http://www.zoyoo.net
    深圳市壹心视觉品牌顾问有限公司	http://www.yixinshijue.com/
    西可（天津）品牌设计有限公司	http://www.seekbrand.net
    共鸣创意顾问机构	www.gm-idea.cn
    商鼎天下品牌设计顾问有限公司	http://www.shangdingteam.com
    天津雅顿品牌设计有限公司	http://www.tjyadun.com
    天津绝策品牌设计有限公司	http://www.u-ad.org
    三人形思企业形象策划（天津）有限公司	http://www.sense-bd.com
    艾茉尔品牌设计公司	http://www.amoimedia.com
    天津启源创意科技有限公司	http://www.tjqiyuan.com
    天津嘉鹤广告有限公司	http://www.caho-ad.com
    杭州好西好品牌策划有限公司	http://www.haoxhao.com
    杭州东韵广告策划有限公司	http://www.hzdyad.com
    杭州亦又品牌设计有限公司	http://www.yiubd.com
    杭州知物设计有限公司	http://www.zhiwudesign.com
    善美品牌设计有限公司	http://www.somebrand.cn
    杭州出位设计有限公司	http://www.true-way.cn/
    杭州艾都广告有限公司	http://www.idocis.cn
    沐客品牌策划有限公司	http://www.mukeued.com
    南京唐韵品牌管理有限公司	http://www.sbschina.com
    允承文化发展有限公司	http://www.yunchengcn.com
    可可青设计顾问机构	http://www.cogreendesign.com
    南京方卓文化传播有限公司	http://www.njfzad.com
    南京六朝品牌策划有限公司	http://www.lclogo.com
    汉迪品牌策略设计顾问公司	http://www.njhandy.com
    时创邦品牌设计有限公司	http://www.shichuang-nj.co
    大川品牌设计机构	http://www.78vi.com
    南京灵光企业形象设计有限公司	http://www.lingual.cn
    柠檬创意有限公司	http://www.lemonn.cn
    济南麦道平面设计中心	http://www.jnmaidao.cn
    济南果实品牌设计有限公司	http://www.gainsee.com
    海右博纳品牌管理公司	http://www.hibona.cn
    非蝉品牌设计机构	http://www.facons.cn
    济南吾将广告有限公司	http://www.wujoon.cn
    济南上玄唯象品牌策划有限公司	http://www.sxwxci.com
    济南向北广告有限公司	http://www.dbb2008.cn
    济南太歌广告有限公司	http://www.jinantaige.com
    青岛迈致品牌创意有限公司	https://www.img.ltd
    山岛设计有限公司	http://www.tianyudesign.com
    本生品牌设计有限公司	http://www.benshengsheji.com
    青岛荣德品牌策划有限公司	http://www.adronge.com/index.aspx
    青岛悟本正奇广告有限公司	http://www.hd3s.com/
    优尔品牌营销策划有限公司	http://www.usersbrand.com
    青岛左晨品牌策划有限公司	http://www.zochenbrand.com
    鑫立方设计有限公司	http://www.design3.cc/
    艺达思广告装饰有限公司	http://www.haozy33.cn/
    青岛盛元方略品牌策划有限公司	http://www.syfled.com
    大连艾森品牌传播有限公司	http://www.aissenbrand.com
    相同创意营销策划（大连）有限公司	http://www.xiangtong1975.com
    大连旨一传媒有限公司	http://www.genie-idea.com
    大连壹品形象设计有限公司	http://www.ypin.net
    大连汤迈创意传媒有限公司	http://www.tommimade.com
    大连集田品牌设计有限公司	http://www.jitiandesign.cn
    大连润悟设计有限公司	http://www.runwellbrand.com
    大连壹鸣品牌设计有限责任公司	http://www.yimingdl.com
    中邦品牌设计有限公司	http://www.zonbon.net
    宁波麟石广告设计有限公司	http://www.flint-crea.com
    宁波本来印象企业形象设计有限公司	http://www.nbvis.com
    百特品牌策划有限公司	http://www.nbbt.cn
    宁波盛道美创品牌设计有限公司	http://www.sd-mc.com
    融圣智扬广告有限公司	http://www.holywis.com
    宁波优合传美广告传播有限公司	http://www.yhcm.net
    汉瑞品牌设计创作室	http://www.herogroup.org
    宁波智慧天成广告有限公司	http://www.nbzhihui.com
    宁波力创品牌设计有限公司	http://lcbrand.com
    厦门軒視策划设计有限公司	http://www.xmxuanshi.com
    智再品牌策划有限公司	http://www.zz-ad.com
    合袁(厦门)品牌设计事务所有限公司	http://www.heyedesign.com
    厦门幻想美广告有限公司	http://www.hxmad.com
    厦门东晨视界文化传播有限公司	http://www.xmchange.com
    厦门九智品牌策划有限公司	http://www.xiangvi.com
    厦门大鱼广告有限公司	http://www.maxjob.cn/
    杜微白品牌策划机构	http://www.duweibai.com
    厦门壹笔品牌管理有限公司	http://www.yibivi.com
    成都彼安迪广告设计有限公司	http://www.bd2001.com/
    成都九田品牌设计顾问有限公司	http://www.cd9tian.com
    成都九一堂品牌设计有限公司	http://www.jyt2004.com
    成都瞳创广告有限公司	http://www.tocreate.cc
    成都蜥奎概念品牌设计公司	http://www.cdsecret.com/
    成都火之鸟广告有限公司	http://www.028bird.com
    武汉市摩纳广告有限公司	http://www.whmona.com
    武汉莯恩设计策略有限公司	http://mu-en.com
    武汉艾的尔广告设计有限公司	http://www.adersj.com
    武汉上辰品牌形象有限公司	http://www.sc-vis.com
    武汉十方道合文化传媒有限公司	http://www.sfdhbrand.com
    武汉傅敏设计	http://www.fm312.com/
    楚韵意品文化创意有限公司	http://cyypsheji.com
    武汉光禾创想广告有限公司	http://www.whghcx.com
    武汉良玉设计有限公司	https://iworld.market
    武汉锐联品牌设计有限公司	http://www.whruilian.com
    哈尔滨浅渚企业形象策划有限公司	http://www.qianzhu.cc
    哈尔滨金泽广告有限公司	http://jzgolden.com
    哈尔滨力天企业形象设计有限公司	http://www.dulitian.com
    哈尔滨邦德品牌形象设计公司	http://www.bangdegg.com
    黑龙江省布凡设计有限责任公司	http://www.hljjingyi.com
    哈尔滨多维广告有限公司	http://www.dwvis.com/
    哈尔滨世纪蜂鸟文化传播有限公司	http://www.hrbfnwh.com
    哈尔滨首巷品牌设计公司	http://0451000.com
    哈尔滨彩韵堂设计印务有限公司	http://www.hrbcyt.com
    简高品牌设计有限公司	http://www.concis.cn
    妙集广告设计有限公司	http://www.symiaoji.com
    沈阳禅墨品牌策划有限公司	http://www.sychanmo.com
    卓摩品牌设计有限公司	http://www.zoomvi.com
    沈阳丹田设计有限公司	http://www.dantianfly.com
    沈阳艾的企业顾问有限公司	http://www.a-idear.com
    沈阳视金石广告设计有限公司	http://www.sjs588.com/
    沈阳维多曼广告策划有限公司	http://www.vidoman.com
    沈阳壹度广告有限公司	http://www.yiduad.com
    沈阳鲜道视觉创意设计	http://www.123vis.com
    西安格尚品牌营销策划	http://www.xageshang.com/anli.php
    西安开端品牌设计有限公司	http://www.kaiduan.cc
    本易品牌机构有限公司	http://www.xabenyi.com
    西安壹南品牌文化传播有限公司	http://www.onesouth.cn
    西安必然广告文化传播有限公司	http://www.birancc.cc
    西安灵波深智广告有限公司	http://www.mimad.cn
    西安泰勒广告有限公司	http://xataile.com
    西安十方营销策划有限公司	http://ideafine.com
    西安荣智广告文化传播有限公司	http://www.rz2011.com
    非同广告设计机构	http://www.ficton.com.cn
    长春佐旗品牌策划设计有限公司	http://www.zuoqisheji.com
    长春茗尊文化传播有限公司	http://www.ccmz.cn
    吉林省致远品牌设计有限公司	http://www.zhiyuansheji.com
    长春市兰韵企业形象设计有限责任公司	http://www.cclanyun.com
    长春真象设计有限公司	http://www.zhenxiangsj.com
    吉林省麒禹天下营销策划有限公司	http://www.jlqiyu.com
    长春汇象品牌设计有限公司	http://www.c362.com/
    长春市亦品九画品牌设计有限公司	http://www.ccypjh.com
    长春北邦品牌设计有限公司	http://www.ndesign.cn
    湖南美艺品牌管理有限公司	http://www.csmy.cn
    长沙核桃广告设计有限公司	http://www.2012heart.com
    远行品牌管理顾问	http://www.cnyuanxing.com
    长沙正正品牌设计事务所	http://www.zhengsheji.com
    长沙融策品牌设计有限公司	http://www.rocher.cc
    长沙赤松品牌设计工作室	http://www.hncsbrand.com
    湖南汇智远扬设计有限公司	http://www.cstw.cn
    湖南大和品牌设计有限公司	http://www.andbrand.com.cn
    长沙市正扬品牌策划有限公司	http://www.zhengyangcs.com
    长沙在意品牌策划有限公司	http://www.zaiyiad.cn
    上良（福州）品牌形象设计有限公司	http://www.slbrand.cn
    无限度 ( 福州 ) 品牌传播机构	http://www.vasdo.cn
    福建弘度文化传播有限公司	http://www.hondc.com
    麦智品牌设计公司	http://www.mi-ze.com
    福州蓝禾品牌设计有限公司	http://www.lanham.cn
    福州立众文化传媒有限公司	http://www.risenmedia.cn
    柒俊景品牌设计有限公司	http://www.7ovdesign.com
    福州牧格广告有限公司	http://www.mo-ge.cn
    福州市原色文化传播有限公司	http://www.fzyswh.com
    思维攻略(福建)设计有限公司	http://www.sividesign.com
    澜际品牌（郑州）设计策划有限公司	http://www.lonege.com
    勤略品牌顾问机构	http://www.qinluecn.com
    郑州惟度品牌设计有限公司	http://www.welldodesign.com
    言十品牌整合机构	http://www.yanshiji.com
    无形品牌策划有限公司	http://www.wuxingcehua.com
    新大陆品牌整合机构	http://www.newlandds.com
    郑州唯创品牌设计有限公司	http://www.zzvchuang.com
    河南蜂鸟文化传播有限公司	http://www.fengniaosj.com
    郑州凸凹品牌设计有限公司	http://www.tuaobrand.com/
    郑州天右同道企业形象设计有限公司	http://www.topiobrand.com
    苏州上马设计有限公司	http://szsmcc.com
    苏州上活文化艺术传播有限公司	http://www.onvie.net/
    苏州新年华品牌策划有限公司	http://www.carnival-2005sz.com
    苏州其道品牌策划有限公司	http://www.qidaoad.com
    苏州熏墨堂品牌设计有限公司	http://www.centmo.com
    苏州视尊广告有限公司	http://www.hellovisun.com
    苏州傲美设计有限公司	http://www.aomei-design.com
    苏州磐石设计有限公司	http://www.panshi-d.com
    苏州市嘉禾金马广告有限公司	http://www.szjm.cn
    苏州美太广告传播有限公司	http://meitaiad.com
    佛山市灵灵柒品牌设计有限公司	http://www.007db.com
    汇点品牌策划有限公司	http://www.hopead168.com
    佛山市东睿文化传播有限公司	http://www.fsdongrui.cn
    何国辉设计有限公司	http://www.heguohuidesign.com
    佛山市智野创意广告有限公司	http://www.zhiyead.com
    佛山市三十七计品牌设计有限公司	http://www.37idea.com
    佛山红星品象文化策划有限公司	http://www.reds-star.com/
    佛山灵成广告有限公司	http://www.fslcad.com
    通道品牌设计有限公司	http://www.dautonhk.com
    佛山市锐艺广告策划有限公司	http://www.a068.com
    广东视维品牌营销咨询有限公司	http://www.sivibrand.com
    程刚广告有限公司	http://www.dg80.cn
    墨象序品牌策划设计创意机构	http://www.begooo.cn
    锦色乾坤广告设计有限公司	http://www.daoccn.com/
    东莞市合奇道品牌设计有限公司	http://www.dghqd.com
    东莞市五源企业形象设计有限公司	http://www.f5vi.com
    东莞市视道品牌策划设计有限公司	http://www.visdao.com/video/
    东莞市龙大品牌设计有限公司	http://www.dragon-vi.com
    东莞市源素品牌设计有限公司	http://www.yesobrand.com
    CBD品牌设计有限公司	http://www.cbdbrand.com
    巴木创意设计中心	http://www.bamuidea.com/
    无锡易视创意广告有限公司	http://www.eastdesign.cc
    无锡岑越企业形象策划有限公司	http://logo.sxl.cn/
    百乐士广告有限公司	http://www.wxblaze.com
    无锡市博邦品牌设计有限公司	http://www.bobang.news
    朗睿品牌设计有限公司	http://www.86vi.cn
    世联视觉营销设计机构	http://www.wisdomunion.com.cn
    无锡米一创意设计有限公司	http://www.miyi-china.com
    无锡创知文化发展有限公司	http://www.wxtrans.com
    山西创见文化传播有限公司	http://www.xuchuangsheji.com
    太原德音文化传播有限公司	http://www.deyinwenhua.cn
    山西零点设计有限公司	http://www.sxzero.com
    LISO贾艺峰品牌资产管理公司	http://www.liso2005.com
    山西黑与白包装制品有限公司	http://hybsj.cn
    山西浪涛品牌设计有限公司	http://www.sxbzsj.com
    山西焰雨文化创意有限公司	http://www.sxyanyu.com
    太原中睿品牌设计有限公司	http://www.wisee.net
    典创品牌设计机构	http://www.shanxidc.com
    山西汉墨堂广告有限公司	http://www.shanxihanmotang.com
    四夕堂品牌设计有限公司	http://www.sixidesign.com
    曦芝品牌设计有限公司	http://www.sunwar.com.cn
    合肥翰思雅品牌设计有限公司	http://www.hfhansel.com
    合肥芒致品牌设计有限公司	http://www.hfvis.com
    合肥伊赛文化传播有限公司	http://www.yisaiwenhua.com
    合肥尚也广告传媒有限公司	http://www.hfshangye.com
    智漾设计有限公司	http://www.wis-team.com
    风火锐意企业管理有限公司	http://www.fenghuoruiyi.net
    合肥天麦道道品牌视觉设计有限公司	http://www.ahtomer.com/
    威视计企业形象设计有限公司	http://www.hfcis.com
    懿木品牌设计有限公司	http://www.emuvis.com
    南昌品至营销策划有限公司	http://www.pinzhif.com
    南昌水蓝设计广告有限公司	http://www.ncwbd.com
    引力文化传播有限公司	http://www.jxylsj.cn
    天睿品牌形象设计管理机构	http://www.truibrand.com
    南昌天水传媒有限公司	http://www.nctscm.com
    南昌星际品牌设计有限公司	http://www.jxxjzz.com
    江西奇可文化传播有限公司	http://www.chic998.com
    南昌思蜕广告设计有限公司	http://www.siitui.com
    广西赛朗文化传媒有限公司	http://www.sambrand.cn
    广西大界文化传媒有限公司	http://www.letrue.cn
    和壹品牌设计有限公司	http://www.hoit.cn
    合岸品牌设计顾问有限公司	https://www.lancbd.com
    广西南宁兰韵文化传播有限公司	http://www.gxlanyun.com
    壹零零柒品牌设计有限公司	http://1007ad.cn
    万聚品牌策划设计	http://www.gxwanju.com
    如鱼品牌设计有限公司	http://www.520ruyu.com
    天地汇品牌设计机构	http://www.gxtdh.net
    仪通设计有限公司	http://www.yitongsheji.com
    昆明极佳品牌设计有限公司	http://logovi.com
    昆明上维品牌设计有限公司	http://sunvi.net
    昆明金弦品牌策划设计有限公司	http://www.jx1995.com
    灵狐品牌设计有限公司	http://www.kmsfbd.com
    水墨文化传播（昆明）有限公司	http://www.smc919.com
    肖恩品牌设计有限公司	http://www.seanzxh.com
    昆明市西山区目音广告工作室	http://my-08.com
    昆明新设绘企业形象设计有限公司	http://www.xsh168.com/
    昆明锐力营销策划有限公司	http://www.reray.com
    昆明红门创意广告有限公司	http://www.homenad.com/###
    温州三形品牌设计有限公司	http://www.sanxan.com
    先觉品牌设计有限公司	http://www.muzzibrand.com
    温州形上品牌设计策划有限公司	http://www.ifdesign.cc
    温州智合设计有限公司	http://www.wzchiho.com
    温州超视觉设计有限公司	http://chaovds.com
    温州柏宏品牌设计有限公司	http://www.hoho-d.com
    温州之尚艺术设计有限公司	http://www.shang-design.com.cn
    佐尚形象策划工作室	http://www.z-sch.com
    温州标志工场	http://www.logo581.com
    温州斐格品牌设计有限公司	http://www.figobrand.com
    乌鲁木齐美无画品牌设计	http://www.meiwuhua.com
    新疆大印象广告有限公司	http://www.dyxad.com
    乌鲁木齐山水品牌设计工作室	http://www.xjsheji.com
    乌鲁木齐合合创想广告有限公司	http://www.xjhehesheji.com
    上行设计有限公司	http://sunsund.com
    灵熙（贵阳）品牌设计顾问有限公司	http://www.cnclemon.com
    贵州179品牌设计有限公司	http://www.gz179.com
    贵州传说品牌设计有公司  http://www.chuan-shuo.net
    贵州言思品牌设计有限公司	http://www.yesbrandcc.com
    贵州之彩广告设计有限公司	http://www.zhicaiad.com
    贵州步道设计有限公司	http://www.budo4a.com
    贵州乐意智作文化传媒有限公司	http://www.gzlyzz.com
    贵州灵智天创传媒有限公司	http://www.tccnvis.com
    酷站设计有限公司	http://www.koozhan.com
    """
    l = str.split('\n')
    l = []
    for i in l:
        row_arr = i.split('	')
        if len(row_arr) != 2:
            print(row_arr)
            continue

        print(row_arr)
        name = row_arr[0].strip()
        url = row_arr[1].strip()
        if name:
            try:
                design_company = DesignCompany.objects(name=name).first()
                # 如果存在，则跳过
                if design_company:
                    print("公司已存在: %s" % name)
                    continue

                design_company = DesignCompany(name=name, url=url, kind=2)
                ok = True
                #ok = design_company.save()
                if ok:
                    print("创建成功: %s\n" % name)
                else:
                    print("创建失败: %s\n" % name)
            except(Exception) as e:
                print(e)

        
# 删除公司
@celery.task()
def delete_company():
    page = 1
    perPage = 100
    isEnd = False
    total = 0
    query = {}
    query['craw_user_id'] = 0

    while not isEnd:
        data = DesignCompany.objects(**query).order_by('-created_at').paginate(page=page, per_page=perPage)
        if not data:
            print("get data is empty! \n")
            continue

        # 过滤数据
        for i, d in enumerate(data.items):
            # 删除
            company = DesignCompany.objects(_id=d._id)
            #ok = company.delete()
            ok = True
            if not ok:
                print("删除失败!\n")

            print("删除成功!\n")
            total += 1

        print("current page %s: \n" % page)
        #page += 1
        if len(data.items) < perPage:
            isEnd = True

    print("is over execute count %s\n" % total)

# 格式化转换注册资金
@celery.task()
def registered_capital_format():
    page = 1
    perPage = 100
    isEnd = False
    total = 0
    query = {}

    while not isEnd:
        data = DesignCompany.objects(**query).order_by('-created_at').paginate(page=page, per_page=perPage)
        if not data:
            print("get data is empty! \n")
            continue

        # 过滤数据
        for i, d in enumerate(data.items):
            if not d.registered_capital:
                print("注册资金为空: %s\n" % d.name)

            if d.registered_capital_format:
                continue

            print("注册资金: %s" % d.registered_capital)
            strMoney = d.registered_capital
            strFormatMoney = 0.0
            if '万人民币' in strMoney:
                if '(人民币)' in strMoney:
                    strMoney = strMoney.replace('(人民币)', '')

                strMoney = strMoney.replace('万人民币', '')
                strFormatMoney = force_float_2(strMoney, 0)

            elif '人民币万元' in strMoney:
                strMoney = strMoney.replace('人民币万元', '')
                strFormatMoney = force_float_2(strMoney, 0)

            elif '万元人民币' in strMoney:
                strMoney = strMoney.replace('万元人民币', '')
                strFormatMoney = force_float_2(strMoney, 0)

            elif ' 万元 人民币' in strMoney:
                strMoney = strMoney.replace(' 万元 人民币', '')
                strFormatMoney = force_float_2(strMoney, 0)
                
            elif '万美元' in strMoney:
                strMoney = strMoney.replace('万美元', '')
                strFormatMoney = force_float_2(strMoney, 0)
                strFormatMoney = strFormatMoney * 6.3

            strFormatMoney = force_float_2(strFormatMoney, 0)
                    
            print("格式化：%.2f" % strFormatMoney)

            newMoney = 0
            if strFormatMoney > 0 and strFormatMoney <= 100:
                newMoney = 1
            elif strFormatMoney > 100 and strFormatMoney <= 500:
                newMoney = 2
            elif strFormatMoney > 500 and strFormatMoney <= 1000:
                newMoney = 3
            elif strFormatMoney > 1000 and strFormatMoney <= 5000:
                newMoney = 4
            elif strFormatMoney > 5000:
                newMoney = 5
                
            print("范围输出: %d\n" % newMoney)

            ok = True
            ok = d.update(registered_capital_format=newMoney)
            if not ok:
                print("更新失败!\n")
                continue

            print("更新成功!\n")
            total += 1

        print("current page %s: \n" % page)
        page += 1
        if len(data.items) < perPage:
            isEnd = True

    print("is over execute count %s\n" % total)
    

# 批量设置公司类型
@celery.task()
def batch_set_field():
    page = 1
    perPage = 100
    isEnd = False
    total = 0
    query = {}

    while not isEnd:
        data = DesignCompany.objects(**query).order_by('-created_at').paginate(page=page, per_page=perPage)
        if not data:
            print("get data is empty! \n")
            continue

        # 过滤数据
        for i, d in enumerate(data.items):
            if d.kind:
                continue

            ok = True
            #ok = d.update(kind=1)
            if not ok:
                print("更新失败!\n")
                continue

            print("更新成功!\n")
            total += 1

        print("current page %s: \n" % page)
        page += 1
        if len(data.items) < perPage:
            isEnd = True

    print("is over execute count %s\n" % total)


    
