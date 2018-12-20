# -*- coding:utf-8 -*-

from flask import render_template, request, current_app, url_for, jsonify, g, flash
from . import admin
from app.models.color import Color
from app.helpers.pager import Pager
from app.forms.color import SaveForm, setStatus
from app.transformer.color import t_color_list
from bson import ObjectId

metaInit = {
    'title': '色值管理',
    'css_nav_sub_color': 'active',
    'css_nav_image': 'active',
    'css_all': 'active'
}

## 列表
@admin.route('/color/list')
def color_list():
    meta = metaInit.copy()
    query = {}
    page = int(request.args.get('page', 1))
    per_page = 100
    status = int(request.args.get('status', 0))
    deleted = int(request.args.get('deleted', 0))
    page_url = url_for('admin.color_list', page="#p#", status=status)
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

    data = Color.objects(**query).order_by('-created_at').paginate(page=page, per_page=per_page)
    total_count = Color.objects(**query).count()

    # 过滤数据
    rows = t_color_list(data)

    meta['data'] = rows
    meta['total_count'] = total_count
    pager = Pager(page, per_page, total_count, page_url)
    meta['pager'] = pager.render_view()

    return render_template('admin/color/list.html', meta=meta)

## 编辑
@admin.route('/color/submit')
def color_submit():
    meta = metaInit.copy()
    meta['referer_url'] = request.environ.get('HTTP_REFERER') if request.environ.get('HTTP_REFERER') else ''
    id = request.args.get('id', None)
    meta['data'] = None
    if id:
        item = Color.objects(_id=ObjectId(id)).first()
        meta['data'] = item

    form = SaveForm()

    #current_app.logger.debug(id)
    
    return render_template('admin/color/submit.html', meta=meta, form=form)

## 保存
@admin.route('/color/save', methods=['POST'])
def color_save():
    meta = metaInit.copy()

    form = SaveForm()
    if form.validate_on_submit():
        id = request.form.get('id')
        
        try:
            if id:
                color = form.update()
            else:
                color = form.save(user_id=g.user._id)
        except(Exception) as e:
            return jsonify(success=False, message=str(e))

        if color:
            flash('操作成功!', 'success')
            redirect_to = request.form.get('referer_url') if request.form.get('referer_url') else url_for('admin.color_list')
            return jsonify(success=True, message='操作成功!', redirect_to=redirect_to)
        else:
            return jsonify(success=False, message='操作失败!')
    else:
        return jsonify(success=False, message=str(form.errors))

## 操作状态
@admin.route('/color/set_status', methods=['POST'])
def color_set_status():
    meta = {}

    form = setStatus()
    if form.validate_on_submit():
        id = request.form.get('id')
        
        try:
            color = form.set_status()
        except(Exception) as e:
            return jsonify(success=False, message=str(e))

        if color:
            return jsonify(success=True, message='操作成功!')
        else:
            return jsonify(success=False, message='操作失败!')
    else:
        return jsonify(success=False, message=str(form.errors))
    
    
## 删除
@admin.route('/color/delete', methods=['POST'])
def color_delete():
    meta = {}

    ids = request.values.get('ids', '')
    type = request.values.get('type', 1)
    if not ids:
        return jsonify(success=False, message='缺少请求参数!')
    
    try:
        arr = ids.split(',')
        for d in arr:
            color = Color.objects(_id=ObjectId(d)).first()
            if color:
                color.mark_delete() if color else None
    except(Exception) as e:
        return jsonify(success=False, message=str(e))

    return jsonify(success=True, message='操作成功!', data={'ids': ids, 'type':type}, redirect_to=url_for('admin.color_list'))



