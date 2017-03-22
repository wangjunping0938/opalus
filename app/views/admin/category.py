# -*- coding:utf-8 -*-

from flask import render_template, request, current_app, url_for, jsonify, g
from . import admin
from app.models.category import Category
from app.helpers.pager import Pager
from app.forms.category import SaveForm

@admin.route('/category/list')
def category_list():
    meta = {
        'title': '分类管理',
        'css_nav_sub_category': 'active',
        'css_nav_system': 'active'
    }
    query = {}
    page = int(request.args.get('page', 1))
    per_page = 20
    status = int(request.args.get('status', 0))
    deleted = int(request.args.get('deleted', 0))
    page_url = url_for('admin.category_list', page="#p#", status=status)
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

    data = Category.objects(**query).order_by('create_at').paginate(page=page, per_page=per_page)
    total_count = Category.objects(**query).count()
    meta['data'] = data.items

    pager = Pager(page, per_page, total_count, page_url)
    meta['pager'] = pager.render_view()

    return render_template('admin/category/list.html', meta=meta)

@admin.route('/category/submit')
def category_submit():
    meta = {
        'title': '分类管理',
        'css_nav_sub_category': 'active',
        'css_nav_system': 'active'
    }
    id = int(request.args.get('id', 0))
    meta['data'] = None
    if id != 0:
        category = Category.objects(_id=id).first()
        meta['data'] = category

    form = SaveForm()

    meta['category_kind_options'] = Category.category_kind_options()

    #current_app.logger.debug(id)
    
    return render_template('admin/category/submit.html', meta=meta, form=form)

@admin.route('/category/save', methods=['POST'])
def category_save():

    form = SaveForm()
    if form.validate_on_submit():
        id = request.form.get('id')
        
        try:
            if id:
                category = form.update()
            else:
                category = form.save(user_id=g.user._id)
        except(Exception) as e:
            return jsonify(success=False, message=str(e))

        if category:
            return jsonify(success=True, message='操作成功!', redirect_to=url_for('admin.category_list'))
        else:
            return jsonify(success=False, message='操作失败!')
    else:
        return jsonify(success=False, message=str(form.errors))
    
## 删除
@admin.route('/category/delete', methods=['POST'])
def category_delete():
    meta = {
        'title': '分类管理',
        'css_nav_sub_category': 'active',
        'css_nav_system': 'active'
    }

    ids = request.values.get('ids', '')
    type = request.values.get('type', 1)
    if not ids:
        return jsonify(success=False, message='缺少请求参数!')
    
    try:
        arr = ids.split(',')
        for d in arr:
            category = Category.objects(_id=d).first()
            category.mark_delete() if category else None
    except(Exception) as e:
        return jsonify(success=False, message=str(e))

    return jsonify(success=True, message='操作成功!', data={'ids': ids, 'type':type}, redirect_to=url_for('admin.category_list'))
