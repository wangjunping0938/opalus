# coding: utf-8
from app.extensions import celery
from app.helpers.common import force_int
from app.models.design_conf import DesignConf
from app.models.design_company import DesignCompany
from app.models.design_record import DesignRecord
from flask import current_app, jsonify
import requests
import json
from werkzeug.datastructures import MultiDict

# 统计奖项数量
@celery.task()
def company_stat(mark, no):

    conf = DesignConf.objects(mark=mark).first()
    if not conf:
        print("配置文件不存在！")
        return

    page = 1
    perPage = 100
    isEnd = False
    successStatCount = 0
    failStatCount = 0
    query = {}
    query['deleted'] = 0
    query['status'] = 1

    while not isEnd:
        data = DesignCompany.objects(**query).order_by('-created_at').paginate(page=page, per_page=perPage)
        if not data:
            print("get data is empty! \n")
            continue

        # 过滤数据
        for i, d in enumerate(data.items):
            ## 是否入驻铟果
            is_d3in = 0
            ## 基本信息统计
            baseConf = {
                'in_d3ing': 0,
                'key_personnel_count': 0,
                'chage_record_count': 0,
                'affiliated_agency_count': 0,
                'financing_count': 0,
                'core_team_count': 0,
                'enterprise_business_count': 0,
                'competitor_count': 0,
                'bid_count': 0,
            }
            # 入驻铟果
            if d.d3ing_id:
                is_d3in = 1
                baseConf['in_d3ing'] = conf['in_d3ing']
            # 主要成员
            if d.key_personnel_count:
                baseConf['key_personnel_count'] = d.key_personnel_count * conf['key_personnel_count']
            # 股东信息
            if d.shareholder_count:
                baseConf['shareholder_count'] = d.shareholder_count * conf['shareholder_count']
            # 变更信息
            if d.chage_record_count:
                baseConf['chage_record_count'] = d.chage_record_count * conf['chage_record_count']
            # 分支机构
            if d.affiliated_agency_count:
                baseConf['affiliated_agency_count'] = d.affiliated_agency_count * conf['affiliated_agency_count']
            # 融资
            if d.financing_count:
                baseConf['financing_count'] = d.financing_count * conf['financing_count']
            # 核心团队
            if d.core_team_count:
                baseConf['core_team_count'] = d.core_team_count * conf['core_team_count']
            # 企业业务
            if d.enterprise_business_count:
                baseConf['enterprise_business_count'] = d.enterprise_business_count * conf['enterprise_business_count']
            # 竞品信息
            if d.competitor_count:
                baseConf['competitor_count'] = d.competitor_count * conf['competitor_count']
            # 招投标
            if d.bid_count:
                baseConf['bid_count'] = d.bid_count * conf['bid_count']

            ## 统计基本信息分值
            baseScore = 0
            for k, v in baseConf.items():
                baseScore += v


            ## 商业力指数
            businessConf = {
                'scale': 0,
                'registered_capital_format': 0,
                'investment_abroad_count': 0,
                'annual_return_count': 0,
                'branch': 0,
                'company_count': 0,
            }

            # 公司规则
            if d.scale:
                if d.scale == 1:
                    businessConf['scale'] = conf['scale_a']
                elif d.scale == 2:
                    businessConf['scale'] = conf['scale_b']
                elif d.scale == 3:
                    businessConf['scale'] = conf['scale_c']
                elif d.scale == 4:
                    businessConf['scale'] = conf['scale_d']
                elif d.scale == 5:
                    businessConf['scale'] = conf['scale_e']

            # 注册资金
            if d.registered_capital_format:
                if d.registered_capital_format == 1:
                    businessConf['registered_capital_format'] = conf['registered_capital_format_a']
                elif d.registered_capital_format == 2:
                    businessConf['registered_capital_format'] = conf['registered_capital_format_b']
                elif d.registered_capital_format == 3:
                    businessConf['registered_capital_format'] = conf['registered_capital_format_c']
                elif d.registered_capital_format == 4:
                    businessConf['registered_capital_format'] = conf['registered_capital_format_d']
                elif d.registered_capital_format == 5:
                    businessConf['registered_capital_format'] = conf['registered_capital_format_e']

            # 对外投资
            if d.investment_abroad_count:
                businessConf['investment_abroad_count'] = d.investment_abroad_count * conf['investment_abroad_count']
            # 公司年报
            if d.annual_return_count:
                businessConf['annual_return_count'] = d.annual_return_count * conf['annual_return_count']
            # 分公司数
            if d.branch:
                businessConf['branch'] = force_int(d.branch) * conf['branch']
            # 法人公司数
            if d.company_count:
                businessConf['company_count'] = force_int(d.company_count) * conf['company_count']


            ## 统计商业力指数分值
            businessScore = 0
            for k, v in businessConf.items():
                businessScore += v


            ## 创新力指数
            innovateConf = {
                'trademark_count': 0,
                'patent_count': 0,
                'software_copyright_count': 0,
                'works_copyright_count': 0,
                'icp_count': 0,
            }

            # 商标
            if d.trademark_count:
                if d.trademark_count < 5:
                    innovateConf['trademark_count'] = conf['trademark_count_a']
                elif d.trademark_count >= 5 and d.trademark_count < 10:
                    innovateConf['trademark_count'] = conf['trademark_count_b']
                elif d.trademark_count >= 10 and d.trademark_count < 50:
                    innovateConf['trademark_count'] = conf['trademark_count_c']
                elif d.trademark_count >= 50 and d.trademark_count < 100:
                    innovateConf['trademark_count'] = conf['trademark_count_d']
                elif d.trademark_count >= 100 and d.trademark_count < 500:
                    innovateConf['trademark_count'] = conf['trademark_count_e']
                elif d.trademark_count >= 500:
                    innovateConf['trademark_count'] = conf['trademark_count_f']

            # 专利
            if d.patent_count:
                if d.patent_count < 5:
                    innovateConf['patent_count'] = conf['patent_count_a']
                elif d.patent_count >= 5 and d.patent_count < 10:
                    innovateConf['patent_count'] = conf['patent_count_b']
                elif d.patent_count >= 10 and d.patent_count < 50:
                    innovateConf['patent_count'] = conf['patent_count_c']
                elif d.patent_count >= 50 and d.patent_count < 100:
                    innovateConf['patent_count'] = conf['patent_count_d']
                elif d.patent_count >= 100 and d.patent_count < 500:
                    innovateConf['patent_count'] = conf['patent_count_e']
                elif d.patent_count >= 500:
                    innovateConf['patent_count'] = conf['patent_count_f']
            # 软件著作权
            if d.software_copyright_count:
                if d.software_copyright_count < 5:
                    innovateConf['software_copyright_count'] = conf['software_copyright_count_a']
                elif d.software_copyright_count >= 5 and d.software_copyright_count < 10:
                    innovateConf['software_copyright_count'] = conf['software_copyright_count_b']
                elif d.software_copyright_count >= 10 and d.software_copyright_count < 50:
                    innovateConf['software_copyright_count'] = conf['software_copyright_count_c']
                elif d.software_copyright_count >= 50 and d.software_copyright_count < 100:
                    innovateConf['software_copyright_count'] = conf['software_copyright_count_d']
                elif d.software_copyright_count >= 100 and d.software_copyright_count < 500:
                    innovateConf['software_copyright_count'] = conf['software_copyright_count_e']
                elif d.software_copyright_count >= 500:
                    innovateConf['software_copyright_count'] = conf['software_copyright_count_f']

            # 作品著作权
            if d.works_copyright_count:
                if d.works_copyright_count < 5:
                    innovateConf['works_copyright_count'] = conf['works_copyright_count_a']
                elif d.works_copyright_count >= 5 and d.works_copyright_count < 10:
                    innovateConf['works_copyright_count'] = conf['works_copyright_count_b']
                elif d.works_copyright_count >= 10 and d.works_copyright_count < 50:
                    innovateConf['works_copyright_count'] = conf['works_copyright_count_c']
                elif d.works_copyright_count >= 50 and d.works_copyright_count < 100:
                    innovateConf['works_copyright_count'] = conf['works_copyright_count_d']
                elif d.works_copyright_count >= 100 and d.works_copyright_count < 500:
                    innovateConf['works_copyright_count'] = conf['works_copyright_count_e']
                elif d.works_copyright_count >= 500:
                    innovateConf['works_copyright_count'] = conf['works_copyright_count_f']
            # 网站备案
            if d.icp_count:
                innovateConf['icp_count'] = d.icp_count * conf['icp_count']

            ## 统计创新力指数分值
            innovateScore = 0
            for k, v in innovateConf.items():
                innovateScore += v


            ## 设计力指数
            designConf = {
                'design_center': 0,
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
            }

            # 设计中心--省级/国家级
            if d.is_design_center:
                if d.is_design_center == 1:
                    designConf['design_center'] = conf['design_center_province']
                elif d.is_design_center == 2:
                    designConf['design_center'] = conf['design_center_county']

            # 抓取作品数
            if d.design_case_count:
                designConf['design_case_count'] = d.design_case_count * conf['design_case_count']
            # 铟果作品数
            if d.d3in_case_count:
                designConf['d3in_case_count'] = d.d3in_case_count * conf['d3in_case_count']

            # 红星奖
            if d.red_star_award_count:
                designConf['red_star_award_count'] = d.red_star_award_count * conf['red_star_award_count']
            # 红棉奖
            if d.innovative_design_award_count:
                designConf['innovative_design_award_count'] = d.innovative_design_award_count * conf['innovative_design_award_count']
            # 中国好设计奖
            if d.china_design_award_count:
                designConf['china_design_award_count'] = d.china_design_award_count * conf['china_design_award_count']
            # 中国设计智造大奖
            if d.dia_award_count:
                designConf['dia_award_count'] = d.dia_award_count * conf['dia_award_count']
            # if奖
            if d.if_award_count:
                designConf['if_award_count'] = d.if_award_count * conf['if_award_count']
            # 红点奖
            if d.red_dot_award_count:
                designConf['red_dot_award_count'] = d.red_dot_award_count * conf['red_dot_award_count']
            # IDEA工业设计奖
            if d.idea_award_count:
                designConf['idea_award_count'] = d.idea_award_count * conf['idea_award_count']
            # G-Mark设计奖
            if d.gmark_award_count:
                designConf['gmark_award_count'] = d.gmark_award_count * conf['gmark_award_count']

            ## 统计设计力指数分值
            designScore = 0
            for k, v in designConf.items():
                designScore += v


            ## 影响力指数
            effectConf = {
                'is_high_tech': 0,
                'ty_score': 0,
                'ty_view_count': 0,
                'certification_count': 0,
                'cida_credit_rating': 0,
                'wx_public_count': 0,
            }

            # 高新企业
            if d.is_high_tech:
                effectConf['is_high_tech'] = conf['is_high_tech']
            # 天眼查分数
            if d.ty_score:
                effectConf['ty_score'] = d.ty_score * conf['ty_score']
            # 天眼查浏览数
            if d.ty_view_count:
                if d.ty_view_count < 100:
                    effectConf['ty_view_count'] = conf['ty_view_count_a']
                elif d.ty_view_count >= 100 and d.ty_view_count < 500:
                    effectConf['ty_view_count'] = conf['ty_view_count_b']
                elif d.ty_view_count >= 500 and d.ty_view_count < 2000:
                    effectConf['ty_view_count'] = conf['ty_view_count_c']
                elif d.ty_view_count >= 2000 and d.ty_view_count < 5000:
                    effectConf['ty_view_count'] = conf['ty_view_count_d']
                elif d.ty_view_count >= 5000 and d.ty_view_count < 10000:
                    effectConf['ty_view_count'] = conf['ty_view_count_e']
                elif d.ty_view_count >= 10000:
                    effectConf['ty_view_count'] = conf['ty_view_count_f']

            # 资质证书
            if d.certification_count:
                effectConf['certification_count'] = d.certification_count * conf['certification_count']

            # 工会认证
            if d.cida_credit_rating:
                if d.cida_credit_rating == 1:
                    designConf['cida_credit_rating'] = conf['cida_credit_rating_a']
                elif d.cida_credit_rating == 2:
                    designConf['cida_credit_rating'] = conf['cida_credit_rating_b']
                elif d.cida_credit_rating == 3:
                    designConf['cida_credit_rating'] = conf['cida_credit_rating_c']

            # 公号
            if d.wx_public_count:
                designConf['wx_public_count'] = d.wx_public_count * conf['wx_public_count']


            ## 统计影响力指数分值
            effectScore = 0
            for k, v in effectConf.items():
                effectScore += v


            ## 社会信誉
            creditConf = {
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
                'tax_rating_count': 0,
            }

            # 法律诉讼
            if d.action_at_law_count:
                 creditConf['action_at_law_count'] = d.action_at_law_count * conf['action_at_law_count']
            # 法院公告
            if d.court_announcement_count:
                 creditConf['court_announcement_count'] = d.court_announcement_count * conf['court_announcement_count']
            # 失信人
            if d.dishonest_person_count:
                 creditConf['dishonest_person_count'] = d.dishonest_person_count * conf['dishonest_person_count']
            # 被执行人
            if d.person_subject_count:
                 creditConf['person_subject_count'] = d.person_subject_count * conf['person_subject_count']
            # 开庭公告
            if d.announcement_court_count:
                 creditConf['announcement_court_count'] = d.announcement_court_count * conf['announcement_court_count']
            # 经营异常
            if d.abnormal_operation_count:
                 creditConf['abnormal_operation_count'] = d.abnormal_operation_count * conf['abnormal_operation_count']
            # 行政处罚
            if d.administrative_penalty_count:
                 creditConf['administrative_penalty_count'] = d.administrative_penalty_count * conf['administrative_penalty_count']
            # 严重违法
            if d.break_law_count:
                 creditConf['break_law_count'] = d.break_law_count * conf['break_law_count']
            # 股权出质
            if d.equity_pledged_count:
                 creditConf['equity_pledged_count'] = d.equity_pledged_count * conf['equity_pledged_count']
            # 动产抵押
            if d.chattel_mortgage_count:
                 creditConf['chattel_mortgage_count'] = d.chattel_mortgage_count * conf['chattel_mortgage_count']
            # 欠税公告
            if d.tax_notice_count:
                 creditConf['tax_notice_count'] = d.tax_notice_count * conf['tax_notice_count']
            # 司法拍卖
            if d.judicial_sale_count:
                 creditConf['judicial_sale_count'] = d.judicial_sale_count * conf['judicial_sale_count']
            # 税务评级
            if d.tax_rating_count:
                creditConf['tax_rating_count'] = d.tax_rating_count * conf['tax_rating_count']


            ## 统计社会信誉分值
            creditScore = 100
            for k, v in creditConf.items():
                creditScore += v


            ## 统计总分数
            # baseConf  businessConf  innovateConf  designConf  effectConf  creditConf
            totalScore = baseScore + businessScore + innovateScore + designScore + effectScore + creditScore


            row = {
                'mark': mark,
                'no': no,
                'number': str(d.number),
                'is_d3in': is_d3in,
                'base_score': baseScore,
                'base_group': baseConf,
                'business_score': businessScore,
                'business_group': businessConf,
                'innovate_score': innovateScore,
                'innovate_group': innovateConf,
                'design_score': designScore,
                'design_group': designConf,
                'effect_score': effectScore,
                'effect_group': effectConf,
                'credit_score': creditScore,
                'credit_group': creditConf,
                'total_score': totalScore,
            }

            recordQuery = {
                'mark': mark,
                'no': no,
                'number': str(d.number),
            }
            try:
                item = DesignRecord.objects(**recordQuery).first()
                if item:
                    if item.deleted == 1:
                        row['deleted'] = 0
                    ok = item.update(**row)
                else:
                    item = DesignRecord(**row)
                    ok = item.save()
                    
                if not ok:
                    print("数据保存失败: %s" % str(ok))
                    continue
            except(Exception) as e:
                print("数据保存异常: %s" % str(e))
                continue
            
            successStatCount += 1
            print("stat success: %s" % d.number)
            print("------------------\n")

        print("current page %s: \n" % page)
        page += 1
        if len(data.items) < perPage:
            isEnd = True

    print("is over execute SuccessCount %d ---- failCount: %d\n" % (successStatCount, failStatCount))


