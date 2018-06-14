# -*- coding:utf-8 -*-

from flask import render_template, request, current_app, url_for, jsonify, g, flash
from . import admin
from app.models.company_queue import CompanyQueue
from app.helpers.pager import Pager
from app.forms.company_queue import setStatus
from bson import ObjectId

## 列表
@admin.route('/company_queue/list')
def company_queue_list():
    meta = {
        'title': '待执行队列',
        'css_nav_sub_company_queue': 'active',
        'css_nav_design': 'active',
        'css_all': 'active'
    }
    query = {}
    page = int(request.args.get('page', 1))
    per_page = 20
    status = int(request.args.get('status', 0))
    deleted = int(request.args.get('deleted', 0))
    page_url = url_for('admin.company_queue_list', page="#p#", status=status)
    if status == -1:
        meta['css_disable'] = 'active'
        query['status'] = 0
    elif status == 1:
        query['status'] = 1
        meta['css_verify'] = 'active'
    elif status == 5:
        query['status'] = 5
        meta['css_success'] = 'active'
    else:
        meta['css_all'] = 'active'

    query['deleted'] = deleted
    current_app.logger.debug(type(g.user))

    data = CompanyQueue.objects(**query).order_by('-created_at').paginate(page=page, per_page=per_page)
    total_count = CompanyQueue.objects(**query).count()

    meta['data'] = data.items

    pager = Pager(page, per_page, total_count, page_url)
    meta['pager'] = pager.render_view()

    return render_template('admin/company_queue/list.html', meta=meta)


## 操作状态
@admin.route('/company_queue/set_status', methods=['POST'])
def company_queue_set_status():
    meta = {}

    form = setStatus()
    if form.validate_on_submit():
        id = request.form.get('id')
        
        try:
            item = form.set_status()
        except(Exception) as e:
            return jsonify(success=False, message=str(e))

        if item:
            return jsonify(success=True, message='操作成功!')
        else:
            return jsonify(success=False, message='操作失败!')
    else:
        return jsonify(success=False, message=str(form.errors))
    
    
## 删除
@admin.route('/company_queue/delete', methods=['POST'])
def company_queue_delete():
    meta = {}

    ids = request.values.get('ids', '')
    type = request.values.get('type', 1)
    if not ids:
        return jsonify(success=False, message='缺少请求参数!')
    
    try:
        arr = ids.split(',')
        for d in arr:
            item = CompanyQueue.objects(_id=ObjectId(d)).first()
            if item:
                item.delete() if item else None
    except(Exception) as e:
        return jsonify(success=False, message=str(e))

    return jsonify(success=True, message='操作成功!', data={'ids': ids, 'type':type}, redirect_to=url_for('admin.company_queue_list'))



