from flask import request, jsonify
from . import api
from app.models.product import Product
from app.helpers.pager import Pager
from app.helpers.common import force_int, force_float_2
from app.forms.product import SaveForm
from app.lib.grab import push_product

## 更新商品信息
@api.route('/product/update', methods=['POST'])
def product_update():

    data = request.values.to_dict()

    result = push_product(**data)
    if result['success']:
        return jsonify(code=0, message='success!', data=result['data'])
    else:
        return jsonify(code=3002, message=result['message'])

