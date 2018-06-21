# coding: utf-8
from app.extensions import celery
from app.models.company_queue import CompanyQueue
from flask import current_app, jsonify
from app.helpers.common import force_int, force_float_2
from app.jobs.design_case import d3in_case_one_stat
import requests
import json
import time
import datetime

# 更新/创建公司列队
@celery.task()
def submit_company_queue(name, d3in_id):
    result = {'success': False, 'message': ''}
    data = {}
    item = CompanyQueue.objects(name=name, deleted=0).first()
    if item:
        data['in_grap'] = 0
        data['inc__grap_times'] = 1
        data['last_on'] = datetime.datetime.now()
        ok = item.update(**data)
    else:
        data['name'] = name
        data['d3in_id'] = d3in_id
        data['last_on'] = datetime.datetime.now()
        data['status'] = 1
        item = CompanyQueue(**data)
        ok = item.save()

    if not ok:
        result['message'] = '操作失败'
        return result
    result['success'] = True
    result['data'] = item
    return result
        
