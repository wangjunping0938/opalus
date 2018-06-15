from flask import request, jsonify, current_app
from . import api
import datetime
from app.models.company_queue import CompanyQueue
from app.helpers.pager import Pager
from bson import ObjectId
from app.forms.company_queue import SaveForm

## 列表
@api.route('/company_queue/list')
def company_queue_list():

    query = {}
    meta = {}
    page = int(request.args.get('page', 1))
    d3in_id = int(request.args.get('d3in_id', 0))
    number = int(request.args.get('number', 0))
    in_grap = int(request.args.get('in_grap', 0))
    out_grap = int(request.args.get('out_grap', 0))
    per_page = int(request.args.get('per_page', 20))
    status = int(request.args.get('status', 0))
    deleted = int(request.args.get('deleted', 0))
    name = request.args.get('name', '')

    if d3in_id:
        query['d3in_id'] = d3in_id

    if number:
        query['number'] = number

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
        data = CompanyQueue.objects(**query).order_by('-created_at').paginate(page=page, per_page=per_page)
        total_count = CompanyQueue.objects(**query).count()

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
@api.route('/company_queue/submit', methods=['POST'])
def company_queue_submit():

    form = SaveForm(request.values)
    if not form.validate_on_submit():
        return jsonify(code=3004, message=str(form.errors))

    id = request.values.get('id', '')
    name = request.values.get('name', '')
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
                item = CompanyQueue.objects(_id=ObjectId(id)).first()
                if not item:
                    return jsonify(code=3002, message='内容不存在!')
                if 'id' in data:
                    data.pop('id')
                if 'name' in data:
                    data.pop('name')
                if 'd3in_id' in data:
                    data.pop('d3in_id')

            if item:
                item.update(**data)

        elif name:
            item = CompanyQueue.objects(name=name, deleted=0).first()
            if item:
                data['in_grap'] = 0
                data['inc__grap_times'] = 1
                if 'd3in_id' in data:
                    data.pop('d3in_id')
                data['last_on'] = datetime.datetime.now()
                item.update(**data)
            else:
                data['last_on'] = datetime.datetime.now()
                data['status'] = 1
                item = CompanyQueue(**data)
                item.save()
        else:
            return jsonify(code=3003, message='至少传入一个参数!')

        if item:
            return jsonify(code=0, message='success!', data=data)
        else:
            return jsonify(code=3010, message='操作失败！')

    except(Exception) as e:
        return jsonify(code=3011, message=str(e))

