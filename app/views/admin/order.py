# -*- coding:utf-8 -*-

from flask import render_template, request, current_app, url_for, jsonify, g
from . import admin
from app.models.order import Order
from app.helpers.pager import Pager
from app.forms.order import SaveForm
import bson

## 列表
@admin.route('/order/list')
def order_list():
    meta = {
        'title': '订单管理',
        'css_nav_sub_order': 'active',
        'css_nav_reptile': 'active'
    }
    query = {}
    page = int(request.args.get('page', 1))
    per_page = 20
    status = int(request.args.get('status', 0))
    deleted = int(request.args.get('deleted', 0))
    page_url = url_for('admin.order_list', page="#p#", status=status)
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

    data = Order.objects(**query).order_by('create_at').paginate(page=page, per_page=per_page)
    total_count = Order.objects(**query).count()

    meta['data'] = data.items

    pager = Pager(page, per_page, total_count, page_url)
    meta['pager'] = pager.render_view()

    return render_template('admin/order/list.html', meta=meta)

## 编辑
@admin.route('/order/submit')
def order_submit():
    meta = {
        'title': '订单管理',
        'css_nav_sub_order': 'active',
        'css_nav_reptile': 'active'
    }
    id = request.args.get('id', None)
    meta['data'] = None
    if id:
        order = Order.objects(_id=bson.objectid.ObjectId(id)).first()
        meta['data'] = order

    form = SaveForm()

    #current_app.logger.debug(id)
    
    return render_template('admin/order/submit.html', meta=meta, form=form)

## 保存
@admin.route('/order/save', methods=['POST'])
def order_save():
    meta = {
        'title': '订单管理',
        'css_nav_sub_order': 'active',
        'css_nav_reptile': 'active'
    }

    form = SaveForm()
    if form.validate_on_submit():
        id = request.form.get('id')
        
        try:
            if id:
                order = form.update_one()
            else:
                order = form.save(user_id=g.user._id)
        except(Exception) as e:
            return jsonify(success=False, message=str(e))

        if order:
            return jsonify(success=True, message='操作成功!', redirect_to=url_for('admin.order_list'))
        else:
            return jsonify(success=False, message='操作失败!')
    else:
        return jsonify(success=False, message=str(form.errors))
    
    
## 删除
@admin.route('/order/delete', methods=['POST'])
def order_delete():
    meta = {
        'title': '订单管理',
        'css_nav_sub_order': 'active',
        'css_nav_reptile': 'active'
    }

    ids = request.values.get('ids', '')
    type = request.values.get('type', 1)
    if not ids:
        return jsonify(success=False, message='缺少请求参数!')
    
    try:
        arr = ids.split(',')
        for d in arr:
            order = Order.objects(_id=bson.objectid.ObjectId(d)).first()
            order.mark_delete() if order else None
    except(Exception) as e:
        return jsonify(success=False, message=str(e))

    return jsonify(success=True, message='操作成功!', data={'ids': ids, 'type':type}, redirect_to=url_for('admin.order_list'))


