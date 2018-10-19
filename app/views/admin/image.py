# -*- coding:utf-8 -*-

from flask import render_template, request, current_app, url_for, jsonify, g, flash
from . import admin
from app.models.image import Image
from app.helpers.pager import Pager
from app.helpers.common import force_int
from app.forms.image import SaveForm, setStatus
from bson import ObjectId

## 列表
@admin.route('/image/list')
def image_list():
    meta = {
        'title': '设计公司管理',
        'css_nav_sub_image': 'active',
        'css_nav_design': 'active',
        'css_all': 'active'
    }
    query = {}
    page = force_int(request.args.get('page', 1))
    per_page = force_int(request.args.get('per_page', 100))
    status = force_int(request.args.get('status', 0))
    deleted = force_int(request.args.get('deleted', 0))
    kind = force_int(request.args.get('kind', 0))

    t = force_int(request.args.get('t', 1), 1)
    q = request.args.get('q', '')

    if q:
        if t==1:
            query['id'] = force_int(q.strip())
        if t==2:
            query['name'] = {"$regex": q.strip()}

    if kind:
        if kind == 1:
            meta['css_industry'] = 'active'
        elif kind == 2:
            meta['css_plane'] = 'active'
        meta['css_all'] = ''
        query['kind'] = kind

    if status == -1:
        meta['css_disable'] = 'active'
        query['status'] = 0
    if status == 1:
        query['status'] = 1
        meta['css_enable'] = 'active'
    else:
        pass

    query['deleted'] = deleted

    page_url = url_for('admin.image_list', page="#p#", q=q, t=t, kind=kind, status=status)

    data = Image.objects(**query).order_by('-created_at').paginate(page=page, per_page=per_page)
    total_count = Image.objects(**query).count()

    # 过滤数据
    for i, d in enumerate(data.items):
        if data.items[i].kind == 1:
            kind_label = '工业设计'
        elif data.items[i].kind == 2:
            kind_label = '平台设计'
        else:
            kind_label = '--'
        data.items[i].kind_label = kind_label

    meta['data'] = data.items

    pager = Pager(page, per_page, total_count, page_url)
    meta['pager'] = pager.render_view()

    return render_template('admin/image/list.html', meta=meta)

## 编辑
@admin.route('/image/submit')
def image_submit():
    meta = {
        'title': '设计公司管理',
        'css_nav_sub_image': 'active',
        'css_nav_design': 'active'
    }
    id = request.args.get('id', None)
    meta['data'] = None
    if id:
        image = Image.objects(_id=ObjectId(id)).first()
        image.tags_label = ','.join(image.tags)
        meta['data'] = image

    form = SaveForm()

    meta['company_scale_options'] = company_scale_options()
    meta['company_nature_options'] = company_nature_options()
    meta['company_registered_capital_format'] = company_registered_capital_format_options()
    meta['referer_url'] = request.environ.get('HTTP_REFERER') if request.environ.get('HTTP_REFERER') else ''
    
    return render_template('admin/image/submit.html', meta=meta, form=form)

## 保存
@admin.route('/image/save', methods=['POST'])
def image_save():
    meta = {
        'title': '设计公司管理',
        'css_nav_sub_image': 'active',
        'css_nav_design': 'active'
    }

    form = SaveForm()
    if form.validate_on_submit():
        id = request.form.get('id')
        
        try:
            if id:
                image = form.update()
            else:
                image = form.save(user_id=g.user._id)
        except(Exception) as e:
            return jsonify(success=False, message=str(e))

        if image:
            flash('操作成功!', 'success')
            redirect_to = request.form.get('referer_url') if request.form.get('referer_url') else url_for('admin.image_list')
            return jsonify(success=True, message='操作成功!', redirect_to = redirect_to)
        else:
            return jsonify(success=False, message='操作失败!')
    else:
        return jsonify(success=False, message=str(form.errors))

## 操作状态
@admin.route('/image/set_status', methods=['POST'])
def image_set_status():
    meta = {}

    form = setStatus()
    if form.validate_on_submit():
        id = request.form.get('id')
        
        try:
            image = form.set_status()
        except(Exception) as e:
            return jsonify(success=False, message=str(e))

        if image:
            return jsonify(success=True, message='操作成功!')
        else:
            return jsonify(success=False, message='操作失败!')
    else:
        return jsonify(success=False, message=str(form.errors))
    
    
## 删除
@admin.route('/image/delete', methods=['POST'])
def image_delete():
    meta = {
        'title': '设计公司管理',
        'css_nav_sub_image': 'active',
        'css_nav_design': 'active'
    }

    ids = request.values.get('ids', '')
    type = request.values.get('type', 1)
    if not ids:
        return jsonify(success=False, message='缺少请求参数!')
    
    try:
        arr = ids.split(',')
        for d in arr:
            image = Image.objects(_id=ObjectId(d)).first()
            image.mark_delete() if image else None
    except(Exception) as e:
        return jsonify(success=False, message=str(e))

    return jsonify(success=True, message='操作成功!', data={'ids': ids, 'type':type}, redirect_to=url_for('admin.image_list'))


