# -*- coding:utf-8 -*-

from flask import render_template, request, current_app, url_for, jsonify, g, flash
from . import admin
from app.models.design_case import DesignCase
from app.helpers.pager import Pager
from app.forms.design_case import SaveForm, setStatus
from bson import ObjectId
from app.helpers.common import force_int

## 列表
@admin.route('/design_case/list')
def design_case_list():
    meta = {
        'title': '设计作品管理',
        'css_nav_sub_design_case': 'active',
        'css_nav_design': 'active'
    }
    query = {}
    page = force_int(request.args.get('page', 1))
    per_page = force_int(request.args.get('per_page', 100))
    status = force_int(request.args.get('status', 0))
    deleted = force_int(request.args.get('deleted', 0))
    prize_label = request.args.get('prize_label', '')

    t = force_int(request.args.get('t', 1), 1)
    q = request.args.get('q', '')

    if q:
        if t==1:
            try:
                query['_id'] = ObjectId(q.strip())
            except(Exception) as e:
                query['_id'] = ''
        if t==2:
            query['title'] = {"$regex": q.strip()}

    if prize_label:
        query['prize_label'] = prize_label

    if status == -1:
        meta['css_disable'] = 'active'
        query['status'] = 0
    if status == 1:
        query['status'] = 1
        meta['css_enable'] = 'active'
    else:
        meta['css_all'] = 'active'

    query['deleted'] = deleted

    page_url = url_for('admin.design_case_list', page="#p#", q=q, t=t, prize_label=prize_label, status=status)

    data = DesignCase.objects(**query).order_by('-created_at').paginate(page=page, per_page=per_page)
    total_count = DesignCase.objects(**query).count()

    # 过滤数据
    for i, d in enumerate(data.items):
        pass

    meta['data'] = data.items

    pager = Pager(page, per_page, total_count, page_url)
    meta['pager'] = pager.render_view()

    return render_template('admin/design_case/list.html', meta=meta)

## 编辑
@admin.route('/design_case/submit')
def design_case_submit():
    meta = {
        'title': '设计作品管理',
        'css_nav_sub_design_case': 'active',
        'css_nav_design': 'active'
    }
    id = request.args.get('id', None)
    meta['data'] = None
    if id:
        item = DesignCase.objects(_id=ObjectId(id)).first()
        item.tags_label = ','.join(item.tags)
        meta['data'] = item

    form = SaveForm()

    meta['referer_url'] = request.environ.get('HTTP_REFERER') if request.environ.get('HTTP_REFERER') else ''
    
    return render_template('admin/design_case/submit.html', meta=meta, form=form)

## 保存
@admin.route('/design_case/save', methods=['POST'])
def design_case_save():
    meta = {
        'title': '设计作品管理',
        'css_nav_sub_design_case': 'active',
        'css_nav_design': 'active'
    }

    form = SaveForm()
    if form.validate_on_submit():
        id = request.form.get('id')
        
        try:
            if id:
                item = form.update()
            else:
                item = form.save(user_id=g.user._id)
        except(Exception) as e:
            return jsonify(success=False, message=str(e))

        if item:
            flash('操作成功!', 'success')
            redirect_to = request.form.get('referer_url') if request.form.get('referer_url') else url_for('admin.design_case_list')
            return jsonify(success=True, message='操作成功!', redirect_to = redirect_to)
        else:
            return jsonify(success=False, message='操作失败!')
    else:
        return jsonify(success=False, message=str(form.errors))

## 操作状态
@admin.route('/design_case/set_status', methods=['POST'])
def design_case_set_status():
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
@admin.route('/design_case/delete', methods=['POST'])
def design_case_delete():
    meta = {}

    ids = request.values.get('ids', '')
    type = request.values.get('type', 1)
    if not ids:
        return jsonify(success=False, message='缺少请求参数!')
    
    try:
        arr = ids.split(',')
        for d in arr:
            item = DesignCase.objects(_id=ObjectId(d)).first()
            item.mark_delete() if item else None
    except(Exception) as e:
        return jsonify(success=False, message=str(e))

    return jsonify(success=True, message='操作成功!', data={'ids': ids, 'type':type}, redirect_to=url_for('admin.design_case_list'))


