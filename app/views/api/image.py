from flask import request, jsonify, current_app
from . import api
import datetime
from app.models.image import Image
from app.helpers.pager import Pager
from bson import ObjectId
from app.forms.image import SaveApi

## 列表
@api.route('/image/list')
def image_list():

    query = {}
    meta = {}
    page = int(request.args.get('page', 1))
    per_page = int(request.args.get('per_page', 100))
    status = int(request.args.get('status', 0))
    deleted = int(request.args.get('deleted', 0))
    name = request.args.get('name', '')

    if name:
        query['name'] = name

    if in_grap:
        if in_grap == -1:
            query['in_grap'] = 0
        else:
            query['in_grap'] = in_grap

    if out_grap:
        if out_grap == -1:
            query['out_grap'] = 0
        else:
            query['out_grap'] = out_grap


    if status == -1:
        query['status'] = 0
    if status == 1:
        query['status'] = 1
    else:
        pass

    query['deleted'] = deleted

    try:
        data = Image.objects(**query).order_by('-created_at').paginate(page=page, per_page=per_page)
        total_count = Image.objects(**query).count()

        # 过滤数据
        for i, d in enumerate(data.items):
            data.items[i]._id = str(d._id)

        meta['rows'] = data.items
    except(Exception) as e:
        meta['rows'] = []
        total_count = 0

    meta['total_count'] = total_count
    meta['page'] = page
    meta['per_page'] = per_page

    return jsonify(code=0, message='success!', data=meta)


## 保存/更新
@api.route('/image/submit', methods=['POST'])
def image_submit():

    form = SaveApi(request.values)
    if not form.validate_on_submit():
        return jsonify(code=3004, message=str(form.errors))

    data = request.values.to_dict()

    if not data:
        return jsonify(code=3003, message='至少传入一个参数!')

    try:
        item = Image(**data)
        ok = item.save()

        if ok:
            return jsonify(code=0, message='success!', data=item)
        else:
            return jsonify(code=3010, message='操作失败！')

    except(Exception) as e:
        return jsonify(code=3011, message=str(e))

