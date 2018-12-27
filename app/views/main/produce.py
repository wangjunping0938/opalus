from flask import render_template, current_app, request, jsonify, url_for, flash, redirect, g
from . import main
from app.helpers.common import force_int
from app.helpers.constant import prize_options
from app.helpers.pager import Pager
from app.models.produce import Produce
from app.models.brand import Brand
from app.models.category import Category
from app.helpers.block import get_column
from app.transformer.produce import t_produce_view, t_produce_list

from bson import ObjectId

from . import main

metaInit = {
    'title': '产品库',
    'css_nav_image': 'active',
}


@main.route('/produce')
def produce_index():
    meta = metaInit.copy()
    query = {
        'stick': 1,
        'status': 1,
        'deleted': 0,
    }
    stickList = Produce.objects(**query).order_by('-stick_on')[:4]
    # 过滤数据
    sticks = []
    for i, d in enumerate(stickList):
        row = t_produce_view(d)
        sticks.append(row)
    meta['sticks'] = sticks

    meta['index_home_slide'] = get_column('image_index_slider', 10)
    meta['image_home_fine'] = get_column('image_home_fine', 3)
    meta['image_home_special'] = get_column('image_home_special', 2)
    return render_template('produce/index.html', meta=meta)


@main.route('/produce/list')
def produce_list():
    meta = metaInit.copy()
    query = {}
    page = force_int(request.args.get('page', 1))
    per_page = force_int(request.args.get('per_page', 20))
    status = force_int(request.args.get('status', 1))
    deleted = force_int(request.args.get('deleted', 0))
    kind = force_int(request.args.get('kind', 1))
    prize_id = force_int(request.args.get('prize_id', 0))
    category_id = force_int(request.args.get('category_id', 0))
    tag = request.args.get('tag', '')

    t = force_int(request.args.get('t', 1), 1)
    q = request.args.get('q', '')

    if q:
        if t == 1:
            query['title'] = {"$regex": q.strip()}
        if t == 2:
            query['channel'] = q.strip()
        if t == 3:
            query['evt'] = force_int(q.strip())

    if prize_id:
        query['prize'] = {'$elemMatch': {'id': int(prize_id)}}

    if category_id:
        query['category_id'] = category_id

    if tag:
        query['total_tags'] = tag

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

    page_url = url_for('main.produce_list', page="#p#", q=q, t=t, tag=tag, prize_id=prize_id, category_id=category_id, kind=kind, status=status,
                       deleted=deleted)

    data = Produce.objects(**query).order_by('-edit_on', '-editor_level').paginate(page=page, per_page=per_page)
    total_count = Produce.objects(**query).count()

    # 过滤数据
    rows = t_produce_list(data)

    meta['data'] = rows
    meta['total_count'] = total_count
    meta['prize_options'] = prize_options()

    categories = Category.objects(kind=2, status=1, deleted=0)[:30]
    meta['categories'] = categories

    pager = Pager(page, per_page, total_count, page_url)
    meta['pager'] = pager.render_view()
    return render_template('produce/list.html', meta=meta)


# 详情
@main.route('/produce/view')
def produce_view():
    meta = metaInit.copy()

    id = request.args.get('id', None)
    if not id:
        flash('ID不存在!', 'warning')
        return redirect(url_for('main.produce_index'))

    if not len(id) == 24:
        flash('ID非法！', 'warning')
        return redirect(url_for('main.produce_index'))

    item = Produce.objects(_id=ObjectId(id)).first()

    if not item:
        flash('内容不存在！', 'warning')
        return redirect(url_for('main.produce_index'))

    if item.deleted == 1:
        flash('内容已删除！', 'warning')
        return redirect(url_for('main.produce_index'))

    meta['title'] = "%s-素材库" % item['title']
    return render_template('produce/view.html', meta=meta, form=t_produce_view(item))

@main.route('/produce/ajx_del')
def produce_ajx_del():
    id = request.args.get('id', '')
    if not id:
        return jsonify(code=500, message='缺少请求参数！')

    try:
        asset = Produce.objects(_id=ObjectId(id)).first()
        if not asset:
            return jsonify(code=500, message='内容不存在！')
        if g.user._id != asset.user_id:
            return jsonify(code=500, message='没有权限！')

        ok = asset.mark_delete()
        return jsonify(code=0, message='success')
    except(Exception) as e:
        return jsonify(code=500, message=str(e))
