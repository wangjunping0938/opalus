from flask import render_template, request, current_app, url_for, redirect,jsonify, g, flash
from . import admin
from app.models.column_zone import ColumnZone
from app.models.column import Column
from app.helpers.pager import Pager
from app.helpers.common import force_int
from app.forms.column_zone import SaveForm

from bson import ObjectId
import re

metaInit = {
    'title': '栏目管理',
    'css_nav_sub_column_zone': 'active',
    'css_nav_column': 'active',
    'css_all': 'active'
}


# 栏目位置信息列表
@admin.route('/column_zone/list')
def column_zone_list():
    meta = metaInit.copy()
    query = {}
    page = force_int(request.args.get('page', 1))
    per_page = force_int(request.args.get('per_page', 100))
    status = force_int(request.args.get('status', 0))
    deleted = force_int(request.args.get('deleted', 0))
    kind = force_int(request.args.get('kind', 0))

    t = force_int(request.args.get('t', 1), 1)
    q = request.args.get('q', '')

    if q:
        if t == 1:
            query['_id'] = ObjectId(q.strip())
        if t == 2:
            query['title'] = q.strip()
        if t == 3:
            query['column_zone_id'] = force_int(q.strip())
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

    if deleted == 1:
        query['deleted'] = 1
        meta['css_deleted'] = 'active'
    else:
        query['deleted'] = 0

    if not status and not deleted:
        meta['css_all'] = 'active'
    else:
        meta['css_all'] = ''

    page_url = url_for('admin.column_zone_list', page="#p#", q=q, t=t, kind=kind, status=status,
                       deleted=deleted)
    data = ColumnZone.objects(**query).order_by('-created_at').paginate(page=page, per_page=per_page)

    total_count = ColumnZone.objects(**query).count()

    meta['data'] = data.items
    meta['total_count'] = total_count

    pager = Pager(page, per_page, total_count, page_url)
    meta['pager'] = pager.render_view()

    return render_template('admin/column_zone/list.html', meta=meta)


# 栏目位置编辑
@admin.route('/column_zone/submit')
def column_zone_submit():
    meta = metaInit.copy()
    id = request.args.get('id', None)
    meta['data'] = None
    meta['is_edit'] = False
    if id:
        item = ColumnZone.objects(_id=ObjectId(id)).first()
        if not item:
            return jsonify(success=False, message='内容不存在!')
        meta['data'] = item
        meta['is_edit'] = True

    form = SaveForm()

    meta['referer_url'] = request.environ.get('HTTP_REFERER') if request.environ.get('HTTP_REFERER') else ''

    return render_template('admin/column_zone/submit.html', meta=meta, form=form)


# 栏目位置保存
@admin.route('/column_zone/save', methods=["POST"])
def column_zone_save():
    meta = metaInit.copy()

    form = SaveForm()
    if form.validate_on_submit():
        id = request.form.get('id')

        try:
            if id:
                column_zone1 = form.update()
            else:
                column_zone1 = form.save(user_id=g.user._id)
        except(Exception) as e:
            return jsonify(success=False, message=str(e))

        if column_zone1:
            redirect_to = request.form.get('referer_url') if request.form.get('referer_url') else url_for(
                'admin.column_zone_list')
            return jsonify(success=True, message='操作成功!', redirect_to=redirect_to)
        else:
            return jsonify(success=False, message='操作失败!')
    else:
        return jsonify(success=False, message=str(form.errors))


# 栏目位置查看栏目内容
@admin.route('/column_zone/target')
def column_zone_target():
    meta = metaInit.copy()
    id = request.args.get('id')
    if id:
        column1 = Column.objects(column_zone_id=id).first()
        if column1:
            return redirect(url_for('admin.column_list',t=1,q=str(column1._id)))

        else:
            return jsonify(success=False, message='内容不存在!')
    else:
        return jsonify(success=False, message='操作失败!')

# 栏目位置删除
@admin.route('/column_zone/delete', methods=['POST'])
def column_zone_delete():
    meta = {}

    ids = request.values.get('ids', '')
    type = request.values.get('type', 1)
    if not ids:
        return jsonify(success=False, message='缺少请求参数!')

    try:
        arr = ids.split(',')
        for d in arr:
            item = Column.objects(_id=ObjectId(d)).first()
            item.mark_delete() if item else None
    except(Exception) as e:
        return jsonify(success=False, message=str(e))

    return jsonify(success=True, message='操作成功!', data={'ids': ids, 'type': type},
                   redirect_to=url_for('admin.column_zone_list'))

# 栏目位置恢复
@admin.route('/column_zone/recovery',methods=['POST'])
def column_zone_recovery():
    ids = request.values.get('ids', '')
    type = request.values.get('type', 1)
    if not ids:
        return jsonify(success=False, message='缺少请求参数!')

    try:
        arr = ids.split(',')
        for d in arr:
            item = ColumnZone.objects(_id=ObjectId(d)).first()
            item.mark_recovery() if item else None
    except(Exception) as e:
        return jsonify(success=False, message=str(e))

    return jsonify(success=True, message='操作成功!', data={'ids': ids, 'type': type},
                   redirect_to=url_for('admin.column_zone_list'))
