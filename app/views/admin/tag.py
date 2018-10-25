# -*- coding:utf-8 -*-

from flask import render_template, request, current_app, url_for, jsonify, g, flash
from . import admin
from app.models.tag import Tag
from app.helpers.pager import Pager
from app.helpers.role import check_role
from app.forms.tag import SaveForm, setStatus
from bson import ObjectId

metaInit = {
    'title': '标签管理',
    'css_nav_sub_tag': 'active',
    'css_nav_image': 'active'
}

## 列表
@admin.route('/tag/list')
def tag_list():
    meta = metaInit.copy()
    query = {}
    page = int(request.args.get('page', 1))
    per_page = 20
    status = int(request.args.get('status', 0))
    deleted = int(request.args.get('deleted', 0))
    page_url = url_for('admin.tag_list', page="#p#", status=status)
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

    data = Tag.objects(**query).order_by('-created_at').paginate(page=page, per_page=per_page)
    total_count = Tag.objects(**query).count()

    meta['data'] = data.items

    pager = Pager(page, per_page, total_count, page_url)
    meta['pager'] = pager.render_view()

    return render_template('admin/tag/list.html', meta=meta)

## 编辑
@admin.route('/tag/submit')
def tag_submit():
    meta = metaInit.copy()
    meta['referer_url'] = request.environ.get('HTTP_REFERER') if request.environ.get('HTTP_REFERER') else ''
    id = request.args.get('id', None)
    meta['data'] = None
    if id:
        tag = Tag.objects(_id=ObjectId(id)).first()
        meta['data'] = tag

    form = SaveForm()

    #current_app.logger.debug(id)
    
    return render_template('admin/tag/submit.html', meta=meta, form=form)

## 保存
@admin.route('/tag/save', methods=['POST'])
def tag_save():
    meta = metaInit.copy()

    form = SaveForm()
    if form.validate_on_submit():
        id = request.form.get('id')
        
        try:
            if id:
                tag = form.update()
            else:
                tag = form.save(user_id=g.user._id)
        except(Exception) as e:
            return jsonify(success=False, message=str(e))

        if tag:
            flash('操作成功!', 'success')
            redirect_to = request.form.get('referer_url') if request.form.get('referer_url') else url_for('admin.tag_list')
            return jsonify(success=True, message='操作成功!', redirect_to=redirect_to)
        else:
            return jsonify(success=False, message='操作失败!')
    else:
        return jsonify(success=False, message=str(form.errors))

## 操作状态
@admin.route('/tag/set_status', methods=['POST'])
def tag_set_status():
    meta = {}

    form = setStatus()
    if form.validate_on_submit():
        id = request.form.get('id')
        
        try:
            tag = form.set_status()
        except(Exception) as e:
            return jsonify(success=False, message=str(e))

        if tag:
            return jsonify(success=True, message='操作成功!')
        else:
            return jsonify(success=False, message='操作失败!')
    else:
        return jsonify(success=False, message=str(form.errors))
    
    
## 删除
@admin.route('/tag/delete', methods=['POST'])
def tag_delete():
    meta = {}

    ids = request.values.get('ids', '')
    type = request.values.get('type', 1)
    if not ids:
        return jsonify(success=False, message='缺少请求参数!')
    
    try:
        arr = ids.split(',')
        for d in arr:
            tag = Tag.objects(_id=ObjectId(d)).first()
            if tag:
                is_pass = check_role(tag.role)
                if is_pass:
                    tag.mark_delete() if tag else None
    except(Exception) as e:
        return jsonify(success=False, message=str(e))

    return jsonify(success=True, message='操作成功!', data={'ids': ids, 'type':type}, redirect_to=url_for('admin.tag_list'))



