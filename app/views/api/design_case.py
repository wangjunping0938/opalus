from flask import request, jsonify, current_app
from . import api
import datetime
from app.models.design_case import DesignCase
from app.helpers.pager import Pager
from bson import ObjectId
from app.forms.design_case import SaveForm

## 列表
@api.route('/design_case/list')
def design_case_list():

    query = {}
    meta = {}
    page = int(request.args.get('page', 1))
    per_page = int(request.args.get('per_page', 20))
    status = int(request.args.get('status', 0))
    deleted = int(request.args.get('deleted', 0))
    title = request.args.get('title', '')
    if status == -1:
        query['status'] = 0
    if status == 1:
        query['status'] = 1
    else:
        pass

    if title:
        query['title'] = title

    query['deleted'] = deleted

    try:
        data = DesignCase.objects(**query).order_by('-created_at').paginate(page=page, per_page=per_page)
        total_count = DesignCase.objects(**query).count()

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

## 查看
@api.route('/design_case/view')
def design_case_view():
    id = request.args.get('id', None)
    if not id:
        return jsonify(code=3001, message='ID不存在!')

    item = DesignCase.objects(_id=ObjectId(id)).first()
    if not item:
        return jsonify(code=3002, message='公司不存在!')

    item._id = str(item._id)
    item.tags_label = ','.join(item.tags)
    
    return jsonify(code=0, message='success!', data=item)

## 保存/更新
@api.route('/design_case/submit', methods=['POST'])
def design_case_submit():
    form = SaveForm(request.values)
    if not form.validate_on_submit():
        return jsonify(code=3004, message=str(form.errors))

    id = request.values.get('id', '')
    title = request.values.get('title', '')
    data = request.values.to_dict()

    for key in request.values:
        data[key] = data[key].strip()
        if not request.values.get(key):
            data.pop(key)

    if not data:
        return jsonify(code=3003, message='至少传入一个参数!')

    try:
        if id:
            if id:
                item = DesignCase.objects(_id=ObjectId(id)).first()
                if not item:
                    return jsonify(code=3002, message='内容不存在!')
                if 'id' in data:
                    data.pop('id')

            if item:
                item.update(**data)

        elif title:
            item = DesignCase.objects(title=title, deleted=0).first()
            if item:
                item.update(**data)
            else:
                item = DesignCase(**data)
                item.save()

        else:
            return jsonify(code=3003, message='至少传入一个参数!')

        if item:
            return jsonify(code=0, message='success!', data=data)
        else:
            return jsonify(code=3010, message='操作失败！')

    except(Exception) as e:
        return jsonify(success=False, message=str(e))

