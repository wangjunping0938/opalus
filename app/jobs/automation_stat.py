# coding: utf-8
from app.extensions import celery
from app.models.company_queue import CompanyQueue
from app.models.design_conf import DesignConf
from app.models.design_record import DesignRecord
from flask import current_app, jsonify
from app.helpers.common import force_int, force_float_2
from app.jobs.company import create_company, d3in_company_one, award_stat_one
from app.jobs.design_case import d3in_case_one_stat
from app.jobs.company_stat import company_stat_core, ave_update_d3in, average_stat_core
import requests
import json
import time
from app.env import cf

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
                d.update(number=companyResult['data']['number'])
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

                # 生成排行数据
                print("生成排行数据...")
                print(company)

                mark = cf.get('rank', 'mark')
                no = cf.getint('rank', 'no') 
                conf = DesignConf.objects(mark=mark).first()
                if not conf:
                    print("配置文件不存在！")
                    d.update(in_grap=2)
                    continue

                rankOpt = {
                    'company': company,
                    'conf': conf,
                    'mark': mark,
                    'no': no
                }
                genRank = company_stat_core(**rankOpt)
                if not genRank['success']:
                    print(genRank['message'])
                    d.update(in_grap=2)
                    continue

                query = {'mark': mark, 'no': no, 'status': 1, 'deleted': 0}
                nSortVal = '-ave_score'

                maxBase = DesignRecord.objects(**query).order_by('-base_score', nSortVal).first()   # 基础运作力
                maxBusiness = DesignRecord.objects(**query).order_by('-business_score', nSortVal).first()   # 商业决策力
                maxInnovate = DesignRecord.objects(**query).order_by('-innovate_score', nSortVal).first()   # 创新交付力
                maxDesign = DesignRecord.objects(**query).order_by('-design_score', nSortVal).first()   # 品牌溢价力
                maxEffect = DesignRecord.objects(**query).order_by('-effect_score', nSortVal).first()   # 客观公信力
                maxCredit = DesignRecord.objects(**query).order_by('-credit_score', nSortVal).first()   # 风险应激力

                options = {
                    'max_base': maxBase,
                    'max_business': maxBusiness,
                    'max_innovate': maxInnovate,
                    'max_design': maxDesign,
                    'max_effect': maxEffect,
                    'max_credit': maxCredit,
                    'f': 1,
                    'bs': 60,
                    'bf': 0.4
                }
                aveRes = average_stat_core(genRank['data'], **options)
                if not aveRes['success']:
                    print(aveRes['message'])
                    d.update(in_grap=2)
                    continue

                aveUpD3in = ave_update_d3in(aveRes['data'].d3in_id, aveRes['data'])
                if not aveUpD3in['success']:
                    print(aveUpD3in['message'])
                    d.update(in_grap=2)
                    continue

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


