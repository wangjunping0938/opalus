# -*- coding:utf-8 -*-

from flask import render_template, request, current_app, url_for, jsonify, g, flash
from . import admin
from app.models.design_conf import DesignConf
from app.helpers.pager import Pager
from app.helpers.common import force_int
from app.forms.design_conf import SaveForm, setStatus
from bson import ObjectId

## 列表
@admin.route('/design_conf/list')
def design_conf_list():
    meta = {
        'title': '设计公司配置管理',
        'css_nav_sub_design_conf': 'active',
        'css_nav_design': 'active'
    }
    query = {}
    page = force_int(request.args.get('page', 1))
    per_page = force_int(request.args.get('per_page', 100))
    status = force_int(request.args.get('status', 0))
    deleted = force_int(request.args.get('deleted', 0))

    t = force_int(request.args.get('t', 1), 1)
    q = request.args.get('q', '')

    if q:
        if t==1:
            query['mark'] = q.strip()
        if t==2:
            query['name'] = {"$regex": q.strip()}

    if status == -1:
        meta['css_disable'] = 'active'
        query['status'] = 0
    if status == 1:
        query['status'] = 1
        meta['css_enable'] = 'active'
    else:
        meta['css_all'] = 'active'

    query['deleted'] = deleted

    page_url = url_for('admin.design_conf_list', page="#p#", q=q, t=t, status=status)

    data = DesignConf.objects(**query).order_by('-created_at').paginate(page=page, per_page=per_page)
    total_count = DesignConf.objects(**query).count()

    # 过滤数据
    for i, d in enumerate(data.items):
        pass

    meta['data'] = data.items
    meta['total_count'] = total_count
    pager = Pager(page, per_page, total_count, page_url)
    meta['pager'] = pager.render_view()

    return render_template('admin/design_conf/list.html', meta=meta)

## 编辑
@admin.route('/design_conf/submit')
def design_conf_submit():
    meta = {
        'title': '设计公司配置管理',
        'css_nav_sub_design_conf': 'active',
        'css_nav_design': 'active'
    }
    id = request.args.get('id', None)
    meta['data'] = None
    if id:
        design_conf = DesignConf.objects(_id=ObjectId(id)).first()
        meta['data'] = design_conf

    form = SaveForm()

    meta['referer_url'] = request.environ.get('HTTP_REFERER') if request.environ.get('HTTP_REFERER') else ''
    
    return render_template('admin/design_conf/submit.html', meta=meta, form=form)

## 保存
@admin.route('/design_conf/save', methods=['POST'])
def design_conf_save():
    meta = {
        'title': '设计公司配置管理',
        'css_nav_sub_design_conf': 'active',
        'css_nav_design': 'active'
    }

    form = SaveForm()
    if form.validate_on_submit():
        id = request.form.get('id')
        
        try:
            if id:
                design_conf = form.update()
            else:
                design_conf = form.save(user_id=g.user._id)
        except(Exception) as e:
            return jsonify(success=False, message=str(e))

        if design_conf:
            flash('操作成功!', 'success')
            redirect_to = request.form.get('referer_url') if request.form.get('referer_url') else url_for('admin.design_conf_list')
            return jsonify(success=True, message='操作成功!', redirect_to = redirect_to)
        else:
            return jsonify(success=False, message='操作失败!')
    else:
        return jsonify(success=False, message=str(form.errors))

## 操作状态
@admin.route('/design_conf/set_status', methods=['POST'])
def design_conf_set_status():
    meta = {}

    form = setStatus()
    if form.validate_on_submit():
        id = request.form.get('id')
        
        try:
            design_conf = form.set_status()
        except(Exception) as e:
            return jsonify(success=False, message=str(e))

        if design_conf:
            return jsonify(success=True, message='操作成功!')
        else:
            return jsonify(success=False, message='操作失败!')
    else:
        return jsonify(success=False, message=str(form.errors))
    
    
## 删除
@admin.route('/design_conf/delete', methods=['POST'])
def design_conf_delete():
    meta = {
        'title': '设计公司配置管理',
        'css_nav_sub_design_conf': 'active',
        'css_nav_design': 'active'
    }

    ids = request.values.get('ids', '')
    type = request.values.get('type', 1)
    if not ids:
        return jsonify(success=False, message='缺少请求参数!')
    
    try:
        arr = ids.split(',')
        for d in arr:
            design_conf = DesignConf.objects(_id=ObjectId(d)).first()
            design_conf.mark_delete() if design_conf else None
    except(Exception) as e:
        return jsonify(success=False, message=str(e))

    return jsonify(success=True, message='操作成功!', data={'ids': ids, 'type':type}, redirect_to=url_for('admin.design_conf_list'))


