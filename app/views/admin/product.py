# -*- coding:utf-8 -*-

from flask import render_template, request, current_app, url_for, jsonify, g
from . import admin
from app.models.product import Product
from app.helpers.pager import Pager
from app.forms.product import SaveForm
from app.helpers.constant import platform_options, platform_type
import bson

## 列表
@admin.route('/product/list')
def product_list():
    meta = {
        'title': '产品管理',
        'css_nav_sub_product': 'active',
        'css_nav_reptile': 'active'
    }
    query = {}
    page = int(request.args.get('page', 1))
    per_page = 100
    status = int(request.args.get('status', 0))
    deleted = int(request.args.get('deleted', 0))
    page_url = url_for('admin.product_list', page="#p#", status=status)
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

    data = Product.objects(**query).order_by('-created_at').paginate(page=page, per_page=per_page)
    total_count = Product.objects(**query).count()

    # 过滤数据
    for i, d in enumerate(data.items):
        if d.site_from == 0:
            data.items[i].site_from_label
            data.items[i].site_type_label
        else:
            label = platform_options(d.site_from)
            data.items[i].site_from_label = label['name']
            
        data.items[i].site_type_label = platform_type(d.site_type)
        data.items[i].category_tags_s = ','.join(d.category_tags)
        data.items[i].tags_s = ','.join(d.tags)

    meta['data'] = data.items

    pager = Pager(page, per_page, total_count, page_url)
    meta['pager'] = pager.render_view()

    return render_template('admin/product/list.html', meta=meta)

## 编辑
@admin.route('/product/submit')
def product_submit():
    meta = {
        'title': '产品管理',
        'css_nav_sub_product': 'active',
        'css_nav_reptile': 'active'
    }
    id = request.args.get('id', None)
    meta['data'] = None
    if id:
        product = Product.objects(_id=bson.objectid.ObjectId(id)).first()
        meta['data'] = product

    form = SaveForm()

    #current_app.logger.debug(id)
    
    return render_template('admin/product/submit.html', meta=meta, form=form)

## 保存
@admin.route('/product/save', methods=['POST'])
def product_save():
    meta = {
        'title': '产品管理',
        'css_nav_sub_product': 'active',
        'css_nav_reptile': 'active'
    }

    form = SaveForm()
    if form.validate_on_submit():
        id = request.form.get('id')
        
        try:
            if id:
                product = form.update_one()
            else:
                product = form.save(user_id=g.user._id)
        except(Exception) as e:
            return jsonify(success=False, message=str(e))

        if product:
            return jsonify(success=True, message='操作成功!', redirect_to=url_for('admin.product_list'))
        else:
            return jsonify(success=False, message='操作失败!')
    else:
        return jsonify(success=False, message=str(form.errors))
    
    
## 删除
@admin.route('/product/delete', methods=['POST'])
def product_delete():
    meta = {
        'title': '产品管理',
        'css_nav_sub_product': 'active',
        'css_nav_reptile': 'active'
    }

    ids = request.values.get('ids', '')
    type = request.values.get('type', 1)
    if not ids:
        return jsonify(success=False, message='缺少请求参数!')
    
    try:
        arr = ids.split(',')
        for d in arr:
            product = Product.objects(_id=bson.objectid.ObjectId(d)).first()
            product.mark_delete() if product else None
    except(Exception) as e:
        return jsonify(success=False, message=str(e))

    return jsonify(success=True, message='操作成功!', data={'ids': ids, 'type':type}, redirect_to=url_for('admin.product_list'))


