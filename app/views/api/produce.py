from flask import request, jsonify, current_app
from . import api
import datetime
from app.models.produce import Produce
from app.helpers.pager import Pager
from bson import ObjectId
from app.forms.produce import SaveApi



## 保存/更新
@api.route('/produce/submit', methods=['POST'])
def produce_submit():

    form = SaveApi(request.values)
    if not form.validate_on_submit():
        return jsonify(code=3004, message=str(form.errors))

    data = request.values.to_dict()

    if not data:
        return jsonify(code=3003, message='至少传入一个参数!')

    try:
        item = Produce(**data)
        ok = item.save()

        if ok:
            return jsonify(code=0, message='success!', data=item)
        else:
            return jsonify(code=3010, message='操作失败！')

    except(Exception) as e:
        return jsonify(code=3011, message=str(e))

