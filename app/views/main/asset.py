from flask import render_template, current_app, request, jsonify, g
from . import main 
from app.models.asset import Asset
from bson import ObjectId

@main.route('/asset/ajx_list')
def asset_ajx_list():
    page = int(request.args.get('page', 1))
    per_page = int(request.args.get('per_page', 20))
    target_id = request.args.get('target_id', '')
    asset_type = int(request.args.get('asset_type', 1))
    cover_id = request.args.get('cover_id', '')

    meta = {}
    query = {}
    if target_id:
        query['target_id'] = target_id
    query['asset_type'] = asset_type
    query['deleted'] = 0

    try:
        data = Asset.objects(**query).order_by('-created_at').paginate(page=page, per_page=per_page)
        total_count = Asset.objects(**query).count()

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
                'asset_type': d.asset_type,
                'domain': d.domain,
                'thumb_url': thumb_url,
                'is_cover': is_cover
            }
            fields.append(field)

        meta['rows'] = fields
    except(Exception) as e:
        meta['rows'] = []
        total_count = 0

    meta['total_count'] = total_count
    meta['page'] = page
    meta['per_page'] = per_page

    return jsonify(code=0, message='success!', data=meta)

@main.route('/asset/ajx_del')
def asset_ajx_del():
    id = request.args.get('id', '')
    if not id:
        return jsonify(code=500, message='缺少请求参数！')

    try:
        asset = Asset.objects(_id=ObjectId(id)).first()
        if not asset:
            return jsonify(code=500, message='内容不存在！')
        if g.user._id != asset.user_id:
            return jsonify(code=500, message='没有权限！')

        ok = asset.mark_delete()
        return jsonify(code=0, message='success')
    except(Exception) as e:
        return jsonify(code=500, message=str(e))
