# -*- coding:utf-8 -*-

from flask import render_template, request, current_app, url_for, jsonify, g, flash
from . import admin
from app.models.asset import Asset
from app.helpers.pager import Pager
from app.helpers.common import force_int
from app.forms.asset import SaveForm, setStatus
from bson import ObjectId

metaInit = {
    'title': '附件管理',
    'css_nav_sub_asset': 'active',
    'css_nav_system': 'active',
    'css_all': 'active'
}

## 列表
@admin.route('/asset/list')
def asset_list():
    meta = metaInit.copy()
    query = {}
    page = force_int(request.args.get('page', 1))
    per_page = force_int(request.args.get('per_page', 100))
    assetType = force_int(request.args.get('asset_type', 0))
    status = force_int(request.args.get('status', 0))
    deleted = force_int(request.args.get('deleted', 0))
    kind = force_int(request.args.get('kind', 0))
    domain = request.args.get('domain', '')

    t = force_int(request.args.get('t', 1), 1)
    q = request.args.get('q', '')

    if q:
        if t==1:
            query['_id'] = ObjectId(q)
        if t==2:
            query['name'] = {"$regex": q.strip()}

    if assetType:
        query['asset_type'] = assetType

    if domain:
        query['domain'] = domain

    if status == -1:
        meta['css_disable'] = 'active'
        query['status'] = 0
    if status == 1:
        query['status'] = 1
        meta['css_enable'] = 'active'
    else:
        pass

    if deleted == 1:
        query['deleted'] = 1
        meta['css_deleted'] = 'active'
    else:
        query['deleted'] = 0

    if not status and not deleted:
        meta['css_all'] = 'active'
    else:
        meta['css_all'] = ''

    page_url = url_for('admin.asset_list', page="#p#", q=q, t=t, kind=kind, status=status)

    data = Asset.objects(**query).order_by('-created_at').paginate(page=page, per_page=per_page)
    total_count = Asset.objects(**query).count()

    # 过滤数据
    for i, d in enumerate(data.items):
        data.items[i]._id = str(d._id)
        data.items[i].thumb = d.get_thumb_path()

    meta['data'] = data.items
    meta['total_count'] = total_count

    pager = Pager(page, per_page, total_count, page_url)
    meta['pager'] = pager.render_view()

    return render_template('admin/asset/list.html', meta=meta)

## 编辑
@admin.route('/asset/submit')
def asset_submit():
    meta = metaInit.copy()
    id = request.args.get('id', None)
    meta['data'] = None
    if id:
        item = Asset.objects(_id=ObjectId(id)).first()
        if not item:
            return jsonify(success=False, message='内容不存在!')
        meta['data'] = item

    form = SaveForm()

    meta['referer_url'] = request.environ.get('HTTP_REFERER') if request.environ.get('HTTP_REFERER') else ''
    
    return render_template('admin/asset/submit.html', meta=meta, form=form)

## 保存
@admin.route('/asset/save', methods=['POST'])
def asset_save():
    meta = {}

    form = SaveForm()
    if form.validate_on_submit():
        id = request.form.get('id')
        
        try:
            if id:
                asset = form.update()
            else:
                asset = form.save(user_id=g.user._id)
        except(Exception) as e:
            return jsonify(success=False, message=str(e))

        if asset:
            flash('操作成功!', 'success')
            redirect_to = request.form.get('referer_url') if request.form.get('referer_url') else url_for('admin.asset_list')
            return jsonify(success=True, message='操作成功!', redirect_to = redirect_to)
        else:
            return jsonify(success=False, message='操作失败!')
    else:
        return jsonify(success=False, message=str(form.errors))

## 操作状态
@admin.route('/asset/set_status', methods=['POST'])
def asset_set_status():
    meta = {}

    form = setStatus()
    if form.validate_on_submit():
        id = request.form.get('id')
        
        try:
            asset = form.set_status()
        except(Exception) as e:
            return jsonify(success=False, message=str(e))

        if asset:
            return jsonify(success=True, message='操作成功!')
        else:
            return jsonify(success=False, message='操作失败!')
    else:
        return jsonify(success=False, message=str(form.errors))
    
    
## 删除
@admin.route('/asset/delete', methods=['POST'])
def asset_delete():
    meta = {}

    ids = request.values.get('ids', '')
    type = request.values.get('type', 1)
    if not ids:
        return jsonify(success=False, message='缺少请求参数!')
    
    try:
        arr = ids.split(',')
        for d in arr:
            item = Asset.objects(_id=ObjectId(d)).first()
            item.mark_delete() if item else None
    except(Exception) as e:
        return jsonify(success=False, message=str(e))

    return jsonify(success=True, message='操作成功!', data={'ids': ids, 'type':type}, redirect_to=url_for('admin.asset_list'))

## 恢复
@admin.route('/asset/recovery', methods=['POST'])
def asset_recovery():
    meta = {}

    ids = request.values.get('ids', '')
    type = request.values.get('type', 1)
    if not ids:
        return jsonify(success=False, message='缺少请求参数!')
    
    try:
        arr = ids.split(',')
        for d in arr:
            item = Asset.objects(_id=ObjectId(d)).first()
            item.mark_recovery() if item else None
    except(Exception) as e:
        return jsonify(success=False, message=str(e))

    return jsonify(success=True, message='操作成功!', data={'ids': ids, 'type':type}, redirect_to=url_for('admin.asset_list'))


## 移除--从数据库直接删除，同时删除七牛数据
@admin.route('/asset/remove', methods=['POST'])
def asset_remove():
    meta = {}

    ids = request.values.get('ids', '')
    type = request.values.get('type', 1)
    if not ids:
        return jsonify(success=False, message='缺少请求参数!')
    
    try:
        arr = ids.split(',')
        for d in arr:
            item = Asset.objects(_id=ObjectId(d)).first()
            if item and item.deleted==1:
                item.delete()
    except(Exception) as e:
        return jsonify(success=False, message=str(e))

    return jsonify(success=True, message='操作成功!', data={'ids': ids, 'type':type}, redirect_to=url_for('admin.asset_list'))
