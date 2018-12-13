# -*- coding:utf-8 -*-

# 获取所含站点信息
def platform_options(id=0):
    data = [
        {'id': 0, 'name': '--', 'type': 0},
        {'id': 1, 'name': '京东众筹', 'type': 2},
        {'id': 2, 'name': '淘宝众筹', 'type': 2},
        {'id': 3, 'name': '米家', 'type': 2},
        {'id': 4, 'name': '一条', 'type': 1},
        {'id': 5, 'name': '二更', 'type': 1},
        {'id': 6, 'name': '差评', 'type': 1},
        {'id': 7, 'name': '其它', 'type': 0}
    ]

    if id == 0:
        return data
    else:
        for d in data:
            if d['id'] == id:
                return d
    return {'id': 0, 'name': ''}


# 获取网站模式
def platform_type(id=0):
    if id == 1:
        return '正常销售'
    elif id == 2:
        return '众筹'
    elif id == 3:
        return '-'
    else:
        return '--'


# 企业规模
def company_scale_options(id=0):
    data = [
        {'id': 0, 'name': '--'},
        {'id': 1, 'name': '20人以下'},
        {'id': 2, 'name': '20-50人'},
        {'id': 3, 'name': '50-100人'},
        {'id': 4, 'name': '100-300人'},
        {'id': 5, 'name': '300人以上'},
        {'id': 6, 'name': '其它'},
    ]

    if id == 0:
        return data
    else:
        for d in data:
            if d['id'] == id:
                return d
    return {'id': 0, 'name': ''}


# 企业性质
def company_nature_options(id=0):
    data = [
        {'id': 0, 'name': '--'},
        {'id': 1, 'name': '私企'},
        {'id': 2, 'name': '国企'},
        {'id': 3, 'name': '事业单位'},
        {'id': 4, 'name': '外企'},
        {'id': 5, 'name': '合资企业'},
        {'id': 6, 'name': '其它'},
    ]

    if id == 0:
        return data
    else:
        for d in data:
            if d['id'] == id:
                return d
    return {'id': 0, 'name': ''}


# 企业注册资金
def company_registered_capital_format_options(id=0):
    data = [
        {'id': 0, 'name': '--'},
        {'id': 1, 'name': '1~100万'},
        {'id': 2, 'name': '101~500万'},
        {'id': 3, 'name': '501~1000万'},
        {'id': 4, 'name': '1001~5000万'},
        {'id': 5, 'name': '5000万以上'},
    ]

    if id == 0:
        return data
    else:
        for d in data:
            if d['id'] == id:
                return d
    return {'id': 0, 'name': ''}


# 企业排行维度选项
def design_dimension_options(mark=''):
    data = [
        {'id': 1, 'mark': 'base', 'name': '基础运作力', 'short_name': '基础运作', 'field': 'base_score', 'group': 'base_group',
         'average': 'base_average', 'color': '#778899'},
        {'id': 2, 'mark': 'business', 'name': '商业决策力', 'short_name': '商业决策', 'field': 'business_score',
         'group': 'business_group', 'average': 'business_average', 'color': '#9932CC'},
        {'id': 3, 'mark': 'innovate', 'name': '创新交付力', 'short_name': '创新交付', 'field': 'innovate_score',
         'group': 'innovate_group', 'average': 'innovate_average', 'color': '#00BFFF'},
        {'id': 4, 'mark': 'design', 'name': '品牌溢价力', 'short_name': '品牌溢价', 'field': 'design_score',
         'group': 'design_group', 'average': 'design_average', 'color': '#F08080'},
        {'id': 5, 'mark': 'effect', 'name': '客观公信力', 'short_name': '客观公信', 'field': 'effect_score',
         'group': 'effect_group', 'average': 'effect_average', 'color': '#4169E1'},
        {'id': 6, 'mark': 'credit', 'name': '风险应激力', 'short_name': '风险应激', 'field': 'credit_score',
         'group': 'credit_group', 'average': 'credit_average', 'color': '#66CDAA'},
    ]

    if mark == '':
        return data
    else:
        for d in data:
            if d['mark'] == mark:
                return d
    return {'id': 0, 'mark': '', 'name': ''}


# 企业排行字段对照说明
def design_fields_label_options(field=''):
    data = [
        # 基础
        {'field': 'in_d3ing', 'name': '入驻铟果', 'group': 'base'},
        {'field': 'key_personnel_count', 'name': '主要人员', 'group': 'base'},
        {'field': 'shareholder_count', 'name': '股东信息', 'group': 'base'},
        {'field': 'chage_record_count', 'name': '变更记录', 'group': 'base'},
        {'field': 'affiliated_agency_count', 'name': '分支机构', 'group': 'base'},
        {'field': 'financing_count', 'name': '融资', 'group': 'base'},
        {'field': 'core_team_count', 'name': '核心团队', 'group': 'base'},
        {'field': 'enterprise_business_count', 'name': '企业业务', 'group': 'base'},
        {'field': 'competitor_count', 'name': '竞品信息', 'group': 'base'},
        {'field': 'bid_count', 'name': '招投标', 'group': 'base'},
        # 商业力
        {'field': 'scale', 'name': '公司规模', 'group': 'business'},
        {'field': 'registered_capital_format', 'name': '注册资金', 'group': 'business'},
        {'field': 'investment_abroad_count', 'name': '对外投资', 'group': 'business'},
        {'field': 'annual_return_count', 'name': '公司年报', 'group': 'business'},
        {'field': 'branch', 'name': '分公司数', 'group': 'business'},
        {'field': 'company_count', 'name': '法人公司数', 'group': 'business'},
        # 创新力
        {'field': 'trademark_count', 'name': '商标', 'group': 'innovate'},
        {'field': 'patent_count', 'name': '专利', 'group': 'innovate'},
        {'field': 'software_copyright_count', 'name': '软件著作权', 'group': 'innovate'},
        {'field': 'works_copyright_count', 'name': '作品著作权', 'group': 'innovate'},
        {'field': 'icp_count', 'name': '网站备案', 'group': 'innovate'},
        # 设计力
        {'field': 'design_center', 'name': '设计中心', 'group': 'design'},
        {'field': 'design_case_count', 'name': '抓取作品数', 'group': 'design'},
        {'field': 'd3in_case_count', 'name': '铟果作品数', 'group': 'design'},
        {'field': 'red_star_award_count', 'name': '红星奖', 'group': 'design'},
        {'field': 'innovative_design_award_count', 'name': '红棉奖', 'group': 'design'},
        {'field': 'china_design_award_count', 'name': '中国好设计奖', 'group': 'design'},
        {'field': 'dia_award_count', 'name': '中国设计智造大奖', 'group': 'design'},
        {'field': 'if_award_count', 'name': 'if奖', 'group': 'design'},
        {'field': 'red_dot_award_count', 'name': '红点奖', 'group': 'design'},
        {'field': 'idea_award_count', 'name': 'IDEA工业设计奖', 'group': 'design'},
        {'field': 'gmark_award_count', 'name': 'G-Mark设计奖', 'group': 'design'},
        # 影响力
        {'field': 'is_high_tech', 'name': '高新企业', 'group': 'effect'},
        {'field': 'ty_score', 'name': '天眼查分数', 'group': 'effect'},
        {'field': 'ty_view_count', 'name': '天眼查浏览数', 'group': 'effect'},
        {'field': 'bd_hot_count', 'name': '百度热度', 'group': 'effect'},
        {'field': 'certification_count', 'name': '资质证书', 'group': 'effect'},
        {'field': 'cida_credit_rating', 'name': '工会认证', 'group': 'effect'},
        {'field': 'wx_public_count', 'name': '公号', 'group': 'effect'},
        # 社会信誉
        {'field': 'action_at_law_count', 'name': '法律诉讼', 'group': 'credit'},
        {'field': 'court_announcement_count', 'name': '法院公告', 'group': 'credit'},
        {'field': 'dishonest_person_count', 'name': '失信人', 'group': 'credit'},
        {'field': 'person_subject_count', 'name': '被执行人', 'group': 'credit'},
        {'field': 'announcement_court_count', 'name': '开庭公告', 'group': 'credit'},
        {'field': 'abnormal_operation_count', 'name': '经营异常', 'group': 'credit'},
        {'field': 'administrative_penalty_count', 'name': '行政处罚', 'group': 'credit'},
        {'field': 'break_law_count', 'name': '严重违法', 'group': 'credit'},
        {'field': 'equity_pledged_count', 'name': '股权出质', 'group': 'credit'},
        {'field': 'chattel_mortgage_count', 'name': '动产抵押', 'group': 'credit'},
        {'field': 'tax_notice_count', 'name': '欠税公告', 'group': 'credit'},
        {'field': 'judicial_sale_count', 'name': '司法拍卖', 'group': 'credit'},
        {'field': 'tax_rating_count', 'name': '税务评级', 'group': 'credit'},
        {'field': 'credit_enter_extra', 'name': '入驻加分', 'group': 'credit'},
    ]

    if field == '':
        return data
    else:
        for d in data:
            if d['field'] == field:
                return d
    return {'field': '', 'name': '', 'group': ''}


# 设计奖项
def prize_options(flag=''):
    data = [
<<<<<<< HEAD
        {'id': 1, 'name': '德国红点设计奖'},
        {'id': 2, 'name': '德国IF设计奖'},
        {'id': 3, 'name': 'IDEA工业设计奖'},
        {'id': 4, 'name': '中国红星奖'},
        {'id': 5, 'name': '中国红棉奖'},
        {'id': 6, 'name': '台湾金点奖'},
        {'id': 7, 'name': '香港DFA设计奖'},
        {'id': 8, 'name': '日本G-Mark设计奖'},
        {'id': 9, 'name': '韩国好设计奖'},
        {'id': 10, 'name': '新加坡设计奖'},
        {'id': 11, 'name': '意大利—Compasso d`Oro设计奖'},
        {'id': 12, 'name': '英国设计奖'},
        {'id': 13, 'name': '中国优秀工业设计奖'},
        {'id': 14, 'name': 'DIA中国设计智造大奖'},
        {'id': 15, 'name': '中国好设计奖'},
        {'id': 16, 'name': '澳大利亚国际设计奖'},
        {'id': 17, 'name': '美国IDEA工业设计优秀奖'},
        {'id': 18, 'name': '中国设计智造大奖'},
        {'id': 19, 'name': '德国红点奖'},
        {'id': 20, 'name': 'DBA设计效能奖'},
        {'id': 21, 'name': '东莞杯国际工业设计大奖'},
        {'id': 22, 'name': '中国家具设计金点奖'},
        {'id': 23, 'name': 'A 设计大奖'},

        {'id': -1, 'name': '其它'}
    ]
=======
                {'id':1, 'name': '德国红点设计奖'},
                {'id':2, 'name': '德国IF设计奖'},
                {'id':3, 'name': 'IDEA工业设计奖'},
                {'id':4, 'name': '中国红星奖'},
                {'id':5, 'name': '中国红棉奖'},
                {'id':6, 'name': '台湾金点奖'},
                {'id':7, 'name': '香港DFA设计奖'},
                {'id':8, 'name': '日本G-Mark设计奖'},
                {'id':9, 'name': '韩国好设计奖'},
                {'id':10, 'name': '新加坡设计奖'},
                {'id':11, 'name': '意大利—Compasso d`Oro设计奖'},
                {'id':12, 'name': '英国设计奖'},
                {'id':13, 'name': '中国优秀工业设计奖'},
                {'id':14, 'name': 'DIA中国设计智造大奖'},
                {'id':15, 'name': '中国好设计奖'},
                {'id':16, 'name': '澳大利亚国际设计奖'},
                {'id':17, 'name': '美国IDEA工业设计优秀奖'},
                {'id':18, 'name': '中国设计智造大奖'},
                {'id':20, 'name': 'DBA设计效能奖'},
                {'id':21, 'name': '东莞杯国际工业设计大奖'},
                {'id':22, 'name': '中国家具设计金点奖'},

                {'id':-1, 'name': '其它'}
            ]
>>>>>>> origin/ts
    if not flag:
        return data
    if isinstance(flag, int):
        for d in data:
            if d['id'] == flag:
                return d
    elif isinstance(flag, str):
        for d in data:
            if flag in d['name'] or d['name'] == flag:
                return d
    return {'id': 0, 'name': ''}
