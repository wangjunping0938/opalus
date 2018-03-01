# -*- coding:utf-8 -*-

from flask import render_template, request, current_app, url_for, jsonify, g
from . import admin
from app.models.growth_record import GrowthRecord
from app.models.product import Product
from app.helpers.pager import Pager
from app.helpers.constant import platform_options, platform_type
from bson import ObjectId

## 列表
@admin.route('/growth/list')
def growth_list():
    meta = {
        'title': '增长值记录',
        'css_nav_sub_growth': 'active',
        'css_nav_reptile': 'active'
    }
    query = {}
    page = int(request.args.get('page', 1))
    per_page = 20
    status = int(request.args.get('status', 0))
    deleted = int(request.args.get('deleted', 0))
    target_id = request.args.get('target_id', '')
    day = request.args.get('day', '')
    if day:
        query['day'] = int(day)
        meta['day'] = day
    if target_id:
        query['target_id'] = int(target_id)
        meta['target_id'] = target_id
    page_url = url_for('admin.growth_list', page="#p#", status=status)
    if status == -1:
        meta['css_disable'] = 'active'
        query['status'] = 0
    if status == 1:
        query['status'] = 1
        meta['css_enable'] = 'active'
    else:
        meta['css_all'] = 'active'

    query['deleted'] = deleted

    data = GrowthRecord.objects(**query).order_by('-created_at').paginate(page=page, per_page=per_page)
    total_count = GrowthRecord.objects(**query).count()

    # 过滤数据
    for i, d in enumerate(data.items):
        if d.site_from == 0:
            data.items[i].site_from_label
            data.items[i].site_type_label
        else:
            label = platform_options(d.site_from)
            data.items[i].site_from_label = label['name']
        if d.target_id:
            product = Product.objects(_id=d.target_id).first()
            if product:
                data.items[i].product = product
            else:
                data.items[i].product = {}

            data.items[i].site_type_label = platform_type(d.site_type)

    meta['data'] = data.items

    pager = Pager(page, per_page, total_count, page_url)
    meta['pager'] = pager.render_view()

    return render_template('admin/growth/list.html', meta=meta)
    
    
## 删除
@admin.route('/growth/delete', methods=['POST'])
def growth_delete():
    meta = {
        'title': '增长值记录',
        'css_nav_sub_growth': 'active',
        'css_nav_system': 'active'
    }

    ids = request.values.get('ids', '')
    type = request.values.get('type', 1)
    if not ids:
        return jsonify(success=False, message='缺少请求参数!')
    
    try:
        arr = ids.split(',')
        for d in arr:
            growth_record = GrowthRecord.objects(_id=ObjectId(d)).first()
            growth_record.mark_delete() if growth_record else None
    except(Exception) as e:
        return jsonify(success=False, message=str(e))

    return jsonify(success=True, message='操作成功!', data={'ids': ids, 'type':type}, redirect_to=url_for('admin.growth_list'))


