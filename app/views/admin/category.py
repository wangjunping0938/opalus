# -*- coding:utf-8 -*-

from flask import render_template, request, current_app, url_for, jsonify, g, flash
from . import admin
from app.models.category import Category
from app.helpers.pager import Pager
from app.forms.category import SaveForm, setStatus

@admin.route('/category/list')
def category_list():
    meta = {
        'title': '分类管理',
        'css_nav_sub_category': 'active',
        'css_nav_system': 'active'
    }
    query = {}
    page = int(request.args.get('page', 1))
    per_page = int(request.args.get('per_page', 100))
    status = int(request.args.get('status', 0))
    kind = int(request.args.get('kind', 0))
    deleted = int(request.args.get('deleted', 0))
    if kind:
        query['kind'] = kind
        if kind == 1:
            meta['css_doc'] = 'active'
        elif kind == 2:
            meta['css_image'] = 'active'
        elif kind == 3:
            meta['css_other'] = 'active'
        else:
            meta['css_all'] = 'active'
    else:
        meta['css_all'] = 'active'

    if status == -1:
        query['status'] = 0
    elif status == 1:
        query['status'] = 1
    else:
        pass

    query['deleted'] = deleted

    page_url = url_for('admin.category_list', page="#p#", status=status, kind=kind, per_page=per_page)
    data = Category.objects(**query).order_by('-created_at').paginate(page=page, per_page=per_page)
    total_count = Category.objects(**query).count()

    # 过滤数据
    for i, d in enumerate(data.items):
        kind_label = '--'
        if d.kind == 1:
            kind_label = '文档'
        elif d.kind == 2:
            kind_label = '素材'
        else:
            kind_label = '备用'
            
        data.items[i].kind_label = kind_label

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
    meta['referer_url'] = request.environ.get('HTTP_REFERER') if request.environ.get('HTTP_REFERER') else ''
    id = int(request.args.get('id', 0))
    meta['data'] = None
    if id != 0:
        category = Category.objects(_id=id).first()
        meta['data'] = category

    form = SaveForm()

    meta['category_kind_options'] = Category.category_kind_options()
    meta['parent_options'] = Category.fetch_parent_options()

    current_app.logger.debug('aaa')
    current_app.logger.debug(type(Category.fetch_parent_options()))
    
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
            flash('操作成功!', 'success')
            redirect_to = request.form.get('referer_url') if request.form.get('referer_url') else url_for('admin.category_list')
            return jsonify(success=True, message='操作成功!', redirect_to = redirect_to)
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

## 操作状态
@admin.route('/category/set_status', methods=['POST'])
def category_set_status():
    meta = {}

    form = setStatus()
    if form.validate_on_submit():
        id = request.form.get('id')
        
        try:
            category = form.set_status()
        except(Exception) as e:
            return jsonify(success=False, message=str(e))

        if category:
            return jsonify(success=True, message='操作成功!')
        else:
            return jsonify(success=False, message='操作失败!')
    else:
        return jsonify(success=False, message=str(form.errors))
