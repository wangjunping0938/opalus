from flask import request, jsonify
from . import api
from app.models.product import Product
from app.helpers.pager import Pager
from app.helpers.common import force_int, force_float_2
from app.forms.product import SaveForm
from app.lib.grab import push_product
from app.helpers.common import force_int

## 更新商品信息
@api.route('/product/update', methods=['POST'])
def product_update():

    data = request.values.to_dict()

    result = push_product(**data)
    if result['success']:
        return jsonify(code=0, message='success!', data=result['data'])
    else:
        return jsonify(code=3002, message=result['message'])

## 查询抓取数量
@api.route('/product/fetch_count', methods=['POST'])
def product_fetch_count():

    query = {}
    site_from = request.values.get('site_from', 0)
    if site_from != 0:
        query['site_from'] = force_int(site_from)

    count = Product.objects(**query).count()
    return jsonify(code=0, message='success!', data={ 'count': count })

## 查询某个地址抓取次数
@api.route('/product/fetch_url', methods=['POST'])
def product_fetch_url():
    url = request.values.get('url', '')
    count = 0
    product = Product.objects(url=url).first()
    if product:
        count = product['grab_count']
    return jsonify(code=0, message='success!', data={ 'count': count })

