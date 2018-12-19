# -*- coding:utf-8 -*-

from flask import render_template, request, current_app, url_for, jsonify, flash
from . import admin
from app.models.user import User
from app.helpers.pager import Pager
from app.helpers.common import force_int
from app.forms.user import SaveForm

@admin.route('/user/list')
def user_list():
    meta = {
        'title': '用户管理',
        'css_nav_sub_user': 'active',
        'css_nav_system': 'active'
    }

    query = {}
    page = int(request.args.get('page', 1))
    per_page = int(request.args.get('per_page', 100))
    status = int(request.args.get('status', 0))

    t = int(request.args.get('t', 1))
    q = request.args.get('q', '')

    if q:
        if t==1:
            query['_id'] = force_int(q.strip(), 0)
        if t==2:
            query['account'] = {"$regex": q.strip()}
        if t==3:
            query['phone'] = q.strip()
        if t==4:
            query['email'] = q.strip()

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

    page_url = url_for('admin.user_list', page="#p#", q=q, t=t, status=status)
    data = User.objects(**query).order_by('-created_at').paginate(page=page, per_page=per_page)
    total_count = User.objects(**query).count()
    meta['data'] = data.items
    meta['total_count'] = total_count
    pager = Pager(page, per_page, total_count, page_url)
    meta['pager'] = pager.render_view()

    return render_template('admin/user/list.html', meta=meta)

@admin.route('/user/submit')
def user_submit():
    meta = {
        'title': '用户管理',
        'css_nav_sub_user': 'active',
        'css_nav_system': 'active'
    }
    meta['referer_url'] = request.environ.get('HTTP_REFERER') if request.environ.get('HTTP_REFERER') else ''
    id = int(request.args.get('id', 0))
    meta['data'] = None
    if id != 0:
        user = User.objects(_id=id).first()
        meta['data'] = user

    form = SaveForm()

    #current_app.logger.debug(id)
    
    return render_template('admin/user/submit.html', meta=meta, form=form)

@admin.route('/user/save', methods=['POST'])
def user_save():
    meta = {
        'title': '用户管理',
        'css_nav_sub_user': 'active',
        'css_nav_system': 'active'
    }

    form = SaveForm()
    if form.validate_on_submit():
        user = form.update_one();
        if user:
            flash('操作成功!', 'success')
            redirect_to = request.form.get('referer_url') if request.form.get('referer_url') else url_for('admin.user_list')
            return jsonify(success=True, message='操作成功!', redirect_to = redirect_to)
        else:
            return jsonify(success=False, message='操作失败!')
    else:
        return jsonify(success=False, message=str(form.errors))
    
