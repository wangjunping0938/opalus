# -*- coding:utf-8 -*-

from flask import render_template, request, current_app, url_for, jsonify, g
from . import admin
from app.models.block import Block
from app.helpers.pager import Pager
from app.forms.block import SaveForm
import bson

## 列表
@admin.route('/block/list')
def block_list():
    meta = {
        'title': '配置管理',
        'css_nav_sub_block': 'active',
        'css_nav_system': 'active'
    }
    query = {}
    page = int(request.args.get('page', 1))
    per_page = 20
    status = int(request.args.get('status', 0))
    deleted = int(request.args.get('deleted', 0))
    page_url = url_for('admin.block_list', page="#p#", status=status)
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

    data = Block.objects(**query).order_by('create_at').paginate(page=page, per_page=per_page)
    total_count = Block.objects(**query).count()

    meta['data'] = data.items

    pager = Pager(page, per_page, total_count, page_url)
    meta['pager'] = pager.render_view()

    return render_template('admin/block/list.html', meta=meta)

## 编辑
@admin.route('/block/submit')
def block_submit():
    meta = {
        'title': '配置管理',
        'css_nav_sub_block': 'active',
        'css_nav_system': 'active'
    }
    meta['referer_url'] = request.environ.get('HTTP_REFERER') if request.environ.get('HTTP_REFERER') else ''
    id = request.args.get('id', None)
    meta['data'] = None
    if id:
        block = Block.objects(_id=bson.objectid.ObjectId(id)).first()
        meta['data'] = block

    form = SaveForm()

    #current_app.logger.debug(id)
    
    return render_template('admin/block/submit.html', meta=meta, form=form)

## 保存
@admin.route('/block/save', methods=['POST'])
def block_save():
    meta = {
        'title': '配置管理',
        'css_nav_sub_block': 'active',
        'css_nav_system': 'active'
    }

    form = SaveForm()
    if form.validate_on_submit():
        id = request.form.get('id')
        
        try:
            if id:
                block = form.update_one()
            else:
                block = form.save(user_id=g.user._id)
        except(Exception) as e:
            return jsonify(success=False, message=str(e))

        if block:
            redirect_to = request.form.get('referer_url') if request.form.get('referer_url') else url_for('admin.block_list')
            return jsonify(success=True, message='操作成功!', redirect_to=redirect_to)
        else:
            return jsonify(success=False, message='操作失败!')
    else:
        return jsonify(success=False, message=str(form.errors))
    
    
## 删除
@admin.route('/block/delete', methods=['POST'])
def block_delete():
    meta = {
        'title': '配置管理',
        'css_nav_sub_block': 'active',
        'css_nav_system': 'active'
    }

    ids = request.values.get('ids', '')
    type = request.values.get('type', 1)
    if not ids:
        return jsonify(success=False, message='缺少请求参数!')
    
    try:
        arr = ids.split(',')
        for d in arr:
            block = Block.objects(_id=bson.objectid.ObjectId(d)).first()
            block.mark_delete() if block else None
    except(Exception) as e:
        return jsonify(success=False, message=str(e))

    return jsonify(success=True, message='操作成功!', data={'ids': ids, 'type':type}, redirect_to=url_for('admin.block_list'))


