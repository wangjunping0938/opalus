from flask import render_template, current_app, request, jsonify, url_for, flash, redirect, g
from . import main
from app.helpers.common import force_int
from app.helpers.constant import prize_options
from app.helpers.pager import Pager
from app.models.image import Image
from app.models.brand import Brand
from app.helpers.block import get_column
from app.transformer.image import t_image_view, t_image_list

from bson import ObjectId

from . import main

metaInit = {
    'title': '素材库',
    'css_nav_image': 'active',
}


@main.route('/image')
def image_index():
    meta = metaInit.copy()
    query = {
        'stick': 1,
        'status': 1,
        'deleted': 0,
    }
    stickList = Image.objects(**query).order_by('-stick_on')[:4]
    # 过滤数据
    sticks = []
    for i, d in enumerate(stickList):
        row = {
            '_id': str(d._id),
            'title': d.title,
            'thumb': d.get_thumb_path(),
        }
        sticks.append(row)
    meta['sticks'] = sticks

    meta['index_home_slide'] = get_column('image_index_slider', 10)
    meta['image_home_fine'] = get_column('image_home_fine', 3)
    meta['image_home_special'] = get_column('image_home_special', 2)
    return render_template('image/index.html', meta=meta)


@main.route('/image/list')
def image_list():
    meta = metaInit.copy()
    query = {}
    page = force_int(request.args.get('page', 1))
    per_page = force_int(request.args.get('per_page', 20))
    status = force_int(request.args.get('status', 1))
    deleted = force_int(request.args.get('deleted', 0))
    kind = force_int(request.args.get('kind', 1))
    prize_id = force_int(request.args.get('prize_id', 0))
    tag = request.args.get('tag', '')

    t = force_int(request.args.get('t', 1), 1)
    q = request.args.get('q', '')

    if q:
        if t == 1:
            query['_id'] = ObjectId(q.strip())
        if t == 2:
            query['channel'] = q.strip()
        if t == 3:
            query['evt'] = force_int(q.strip())

    if tag:
        query['total_tags'] = tag

    if prize_id:
        query['prize_id'] = prize_id

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

    page_url = url_for('main.image_list', page="#p#", q=q, t=t, tag=tag, prize_id=prize_id, kind=kind, status=status,
                       deleted=deleted)

    data = Image.objects(**query).order_by('random').paginate(page=page, per_page=per_page)
    total_count = Image.objects(**query).count()

    # 过滤数据
    for i, d in enumerate(data.items):
        prize_label = ''
        brand = None
        data.items[i]._id = str(d._id)
        data.items[i].thumb = d.get_thumb_path()
        if d.prize_id:
            prize_label = prize_options(d.prize_id)['name']
        if d.brand_id:
            brand = Brand.objects(_id=d.brand_id).first()

        data.items[i].prize_label = prize_label
        data.items[i].brand = brand

    # 过滤数据
    rows = t_image_list(data)

    meta['data'] = rows
    meta['total_count'] = total_count
    meta['prize_options'] = prize_options()

    pager = Pager(page, per_page, total_count, page_url)
    meta['pager'] = pager.render_view()
    return render_template('image/list.html', meta=meta)


# 详情
@main.route('/image/view')
def image_view():
    meta = metaInit.copy()

    id = request.args.get('id', None)
    if not id:
        flash('ID不存在!', 'warning')
        return redirect(url_for('main.image_index'))

    if not len(id) == 24:
        flash('ID非法！', 'warning')
        return redirect(url_for('main.image_index'))

    image = Image.objects(_id=ObjectId(id)).first()

    if not image:
        flash('内容不存在！', 'warning')
        return redirect(url_for('main.image_index'))

    if image.deleted == 1:
        flash('内容已删除！', 'warning')
        return redirect(url_for('main.image_index'))

    # image = tranform

    meta['title'] = "%s-素材库" % image['title']
    return render_template('image/view.html', meta=meta, form=t_image_view(image))


@main.route('/image/ajx_list')
def image_ajx_list():
    page = int(request.args.get('page', 1))
    per_page = int(request.args.get('per_page', 10))
    target_id = request.args.get('target_id', '')
    asset_type = int(request.args.get('asset_type', 2))
    cover_id = request.args.get('cover_id', '')

    meta = {}
    query = {}
    if target_id:
        query['target_id'] = target_id
    query['asset_type'] = asset_type
    query['deleted'] = 0

    try:
        data = Image.objects(**query).order_by('-created_at').paginate(page=page, per_page=per_page)
        total_count = Image.objects(**query).count()

        # 过滤数据
        fields = []
        for i, d in enumerate(data.items):
            thumb_dict = d.get_thumb_path()
            thumb_url = ''
            is_cover = False
            if cover_id == str(d._id):
                is_cover = True
            if thumb_dict:
                thumb_url = thumb_dict['sm']
            field = {
                '_id': str(d._id),
                'name': d.name,
                'path': d.path,
                'img_url': d.img_url,
                'asset_type': d.asset_type,
                'domain': d.domain,
                'is_cover': is_cover,
            }
            if thumb_url:
                field['thumb_url'] = thumb_url
            elif d.img_url:
                field['thumb_url'] = d.img_url

            fields.append(field)

        meta['rows'] = fields
    except(Exception) as e:
        meta['rows'] = []
        total_count = 0

    meta['total_count'] = total_count
    meta['page'] = page
    meta['per_page'] = per_page

    return jsonify(code=0, message='success!', data=meta)


@main.route('/image/ajx_del')
def image_ajx_del():
    id = request.args.get('id', '')
    if not id:
        return jsonify(code=500, message='缺少请求参数！')

    try:
        asset = Image.objects(_id=ObjectId(id)).first()
        if not asset:
            return jsonify(code=500, message='内容不存在！')
        if not g.is_edit:
            return jsonify(code=500, message='没有权限！')

        ok = asset.mark_delete()
        return jsonify(code=0, message='success')
    except(Exception) as e:
        return jsonify(code=500, message=str(e))
