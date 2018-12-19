# -*- coding:utf-8 -*-

from flask import render_template, request, current_app, url_for, jsonify, g, flash
from . import admin
from app.models.site import Site
from app.helpers.pager import Pager
from app.helpers.constant import platform_options, platform_type
from app.forms.site import SaveForm, setStatus
import bson

## 列表
@admin.route('/site/list')
def site_list():
    meta = {
        'title': '网站管理',
        'css_nav_sub_site': 'active',
        'css_nav_reptile': 'active'
    }
    query = {}
    page = int(request.args.get('page', 1))
    per_page = int(request.args.get('per_page', 20))
    status = int(request.args.get('status', 0))
    deleted = int(request.args.get('deleted', 0))
    page_url = url_for('admin.site_list', page="#p#", status=status)
    if status == -1:
        meta['css_disable'] = 'active'
        query['status'] = 0
    if status == 1:
        query['status'] = 1
        meta['css_enable'] = 'active'
    else:
        meta['css_all'] = 'active'

    query['deleted'] = deleted

    data = Site.objects(**query).order_by('-created_at').paginate(page=page, per_page=per_page)
    total_count = Site.objects(**query).count()

    # 过滤数据
    for i, d in enumerate(data.items):
        if d.site_from == 0:
            data.items[i].site_from_label = platform_options()
        else:
            label = platform_options(d.site_from)
            data.items[i].site_from_label = label['name']
            
        data.items[i].site_type_label = platform_type(d.site_type)

    meta['data'] = data.items

    pager = Pager(page, per_page, total_count, page_url)
    meta['pager'] = pager.render_view()

    return render_template('admin/site/list.html', meta=meta)

## 编辑
@admin.route('/site/submit')
def site_submit():
    meta = {
        'title': '配置管理',
        'css_nav_sub_site': 'active',
        'css_nav_reptile': 'active'
    }
    id = request.args.get('id', None)
    meta['data'] = None
    if id:
        site = Site.objects(_id=bson.objectid.ObjectId(id)).first()
        meta['data'] = site

    form = SaveForm()

    meta['platform_options'] = platform_options()
    meta['referer_url'] = request.environ.get('HTTP_REFERER') if request.environ.get('HTTP_REFERER') else ''
    
    return render_template('admin/site/submit.html', meta=meta, form=form)

## 保存
@admin.route('/site/save', methods=['POST'])
def site_save():
    meta = {
        'title': '网站管理',
        'css_nav_sub_site': 'active',
        'css_nav_reptile': 'active'
    }

    form = SaveForm()
    if form.validate_on_submit():
        id = request.form.get('id')
        
        try:
            if id:
                site = form.update()
            else:
                site = form.save(user_id=g.user._id)
        except(Exception) as e:
            return jsonify(success=False, message=str(e))

        if site:
            flash('操作成功!', 'success')
            redirect_to = request.form.get('referer_url') if request.form.get('referer_url') else url_for('admin.site_list')
            return jsonify(success=True, message='操作成功!', redirect_to = redirect_to)
        else:
            return jsonify(success=False, message='操作失败!')
    else:
        return jsonify(success=False, message=str(form.errors))

## 操作状态
@admin.route('/site/set_status', methods=['POST'])
def site_set_status():
    meta = {}

    form = setStatus()
    if form.validate_on_submit():
        id = request.form.get('id')
        
        try:
            site = form.set_status()
        except(Exception) as e:
            return jsonify(success=False, message=str(e))

        if site:
            return jsonify(success=True, message='操作成功!')
        else:
            return jsonify(success=False, message='操作失败!')
    else:
        return jsonify(success=False, message=str(form.errors))
    
    
## 删除
@admin.route('/site/delete', methods=['POST'])
def site_delete():
    meta = {
        'title': '网站管理',
        'css_nav_sub_site': 'active',
        'css_nav_reptile': 'active'
    }

    ids = request.values.get('ids', '')
    type = request.values.get('type', 1)
    if not ids:
        return jsonify(success=False, message='缺少请求参数!')
    
    try:
        arr = ids.split(',')
        for d in arr:
            site = Site.objects(_id=bson.objectid.ObjectId(d)).first()
            site.mark_delete() if site else None
    except(Exception) as e:
        return jsonify(success=False, message=str(e))

    return jsonify(success=True, message='操作成功!', data={'ids': ids, 'type':type}, redirect_to=url_for('admin.site_list'))


