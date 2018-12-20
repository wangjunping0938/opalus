# -*- coding:utf-8 -*-

from flask import render_template, request, current_app, url_for, jsonify, g, flash
from . import admin
from app.models.image import Image
from app.models.brand import Brand
from app.models.site import Site
from app.models.category import Category
from app.helpers.pager import Pager
from app.helpers.common import force_int
from app.forms.image import SaveForm, setStatus
from bson import ObjectId
from app.helpers.block import get_block_content
from app.helpers.constant import prize_options
from app.jobs.image import download, upload
from app.jobs.imagetone import get_tones
from app.transformer.image import t_image_list
import re

metaInit = {
    'title': '图片管理',
    'css_nav_sub_image': 'active',
    'css_nav_image': 'active',
    'css_all': 'active'
}


## 列表
@admin.route('/image/list')
def image_list():
    meta = metaInit.copy()
    query = {}
    page = force_int(request.args.get('page', 1))
    per_page = force_int(request.args.get('per_page', 100))
    status = force_int(request.args.get('status', 0))
    deleted = force_int(request.args.get('deleted', 0))
    kind = force_int(request.args.get('kind', 0))
    prize_id = force_int(request.args.get('prize_id', 0))
    site_mark = request.args.get('site_mark','')

    t = force_int(request.args.get('t', 1), 1)
    q = request.args.get('q', '')

    if q:
        if t == 1:
            query['_id'] = ObjectId(q.strip())
        if t == 2:
            query['channel'] = q.strip()
        if t == 3:
            query['evt'] = force_int(q.strip())

    if prize_id:
        query['prize_id'] = prize_id

    if kind:
        if kind == 1:
            meta['css_design'] = 'active'
        elif kind == 5:
            meta['css_fashion'] = 'active'
        meta['css_all'] = ''
        query['kind'] = kind

    if status == -1:
        query['status'] = 0
    if status == 1:
        query['status'] = 1
    else:
        pass

    if deleted == 1:
        query['deleted'] = 1
        meta['css_deleted'] = 'active'
    else:
        query['deleted'] = 0
    if site_mark:
        query['channel'] = site_mark
    if not kind and not deleted:
        meta['css_all'] = 'active'
    else:
        meta['css_all'] = ''

    page_url = url_for('admin.image_list', page="#p#", q=q, t=t, prize_id=prize_id,site_mark=site_mark, kind=kind, status=status, deleted=deleted)

    data = Image.objects(**query).order_by('-created_at').paginate(page=page, per_page=per_page)
    total_count = Image.objects(**query).count()
    site_list = Site.objects.all()
    # 过滤数据
    rows = t_image_list(data)

    meta['data'] = rows
    meta['total_count'] = total_count
    meta['prize_options'] = prize_options()
    meta['site_list'] = site_list
    pager = Pager(page, per_page, total_count, page_url)
    meta['pager'] = pager.render_view()

    return render_template('admin/image/list.html', meta=meta)


## 编辑
@admin.route('/image/submit')
def image_submit():
    meta = metaInit.copy()
    id = request.args.get('id', None)
    meta['data'] = None
    if id:
        item = Image.objects(_id=ObjectId(id)).first()
        item._id = str(item._id)
        item.thumb = item.get_thumb_path()
        item.tags_s = ','.join(item.tags)
        item.color_tags_s = ','.join(item.color_tags)
        item.brand_tags_s = ','.join(item.brand_tags)
        item.material_tags_s = ','.join(item.material_tags)
        item.style_tags_s = ','.join(item.style_tags)
        item.technique_tags_s = ','.join(item.technique_tags)
        item.other_tags_s = ','.join(item.other_tags)
        item.color_ids_s = ','.join(item.color_ids)
        meta['data'] = item

    form = SaveForm()

    meta['default_tags'] = re.split('[,，]', get_block_content('default_tags'))
    meta['default_color_tags'] = re.split('[,，]', get_block_content('default_color_tags'))
    meta['default_brand_tags'] = re.split('[,，]', get_block_content('default_brand_tags'))
    meta['default_material_tags'] = re.split('[,，]', get_block_content('default_material_tags'))
    meta['default_style_tags'] = re.split('[,，]', get_block_content('default_style_tags'))
    meta['default_technique_tags'] = re.split('[,，]', get_block_content('default_technique_tags'))
    meta['default_other_tags'] = re.split('[,，]', get_block_content('default_other_tags'))

    meta['prize_options'] = prize_options()

    categories = Category.objects(kind=2, status=1, deleted=0)[:20]
    meta['categories'] = categories

    # 获取品牌列表
    brands = Brand.objects(status=1, deleted=0)[:1000]
    meta['brands'] = brands

    meta['referer_url'] = request.environ.get('HTTP_REFERER') if request.environ.get('HTTP_REFERER') else ''

    return render_template('admin/image/submit.html', meta=meta, form=form)


## 保存
@admin.route('/image/save', methods=['POST'])
def image_save():
    meta = metaInit.copy()

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
            redirect_to = request.form.get('referer_url') if request.form.get('referer_url') else url_for(
                'admin.image_list')
            return jsonify(success=True, message='操作成功!', redirect_to=redirect_to)
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

## 推荐
@admin.route('/image/set_stick', methods=['POST'])
def image_set_stick():
    meta = metaInit.copy()

    id = request.values.get('id', '')
    evt = request.values.get('evt', 1)
    if not id:
        return jsonify(success=False, message='缺少请求参数!')

    try:
        image = Image.objects(_id=ObjectId(id)).first()
        if not image:
            return jsonify(success=False, message='对象不存在!')           
        image.mark_stick(evt=evt) if image else None
    except(Exception) as e:
        return jsonify(success=False, message=str(e))

    return jsonify(success=True, message='操作成功!', data={'id': id, 'evt': evt},
                   redirect_to=url_for('admin.image_list'))


## 删除
@admin.route('/image/delete', methods=['POST'])
def image_delete():
    meta = metaInit.copy()

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

    return jsonify(success=True, message='操作成功!', data={'ids': ids, 'type': type},
                   redirect_to=url_for('admin.image_list'))


## 恢复
@admin.route('/image/recovery', methods=['POST'])
def image_recovery():
    meta = {}

    ids = request.values.get('ids', '')
    type = request.values.get('type', 1)
    if not ids:
        return jsonify(success=False, message='缺少请求参数!')

    try:
        arr = ids.split(',')
        for d in arr:
            item = Image.objects(_id=ObjectId(d)).first()
            item.mark_recovery() if item else None
    except(Exception) as e:
        return jsonify(success=False, message=str(e))

    return jsonify(success=True, message='操作成功!', data={'ids': ids, 'type': type},
                   redirect_to=url_for('admin.image_list'))


# 上传至七牛云
@admin.route('/image/qiniu', methods=['GET'])
def image_qiniu():
    try:
        upload.delay()
    except Exception as e:
        return jsonify(success=False, message=str(e))

    return jsonify(success=True, message='操作成功!celery正在后台上传')


# 下载到本地
@admin.route('/image/location', methods=['GET'])
def image_location():
    try:
        download.delay()
    except Exception as e:
        return jsonify(success=False, message=str(e))

    return jsonify(success=True, message='操作成功!celery正在后台下载')
