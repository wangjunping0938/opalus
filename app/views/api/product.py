from flask import request, jsonify
from . import api
from app.models.product import Product
from app.helpers.pager import Pager
from app.helpers.common import force_int, force_float_2
from app.forms.product import SaveForm

## 更新商品信息
@api.route('/product/update')
def product_update():

    url = request.values.get('url', '')
    out_number = request.values.get('out_number', '')
    title = request.values.get('title', '')
    sub_title = request.values.get('sub_title', '')

    resume = request.values.get('resume', '')   # 简述
    content = request.values.get('content', '')
    tags = request.values.get('tags', '')
    cover_url = request.values.get('cover_url', '')

    kind = force_int(request.values.get('kind', 0))
    category_id = force_int(request.values.get('category_id', 0))
    site_from = force_int(request.values.get('site_from', 0))
    remark = request.values.get('remark', '')   # 备注

    cost_price = force_float_2(request.values.get('cost_price', 0))
    sale_price = force_float_2(request.values.get('sale_price', 0))
    total_price = force_float_2(request.values.get('total_price', 0))

    love_count = force_int(request.values.get('love_count', 0))
    favorite_count = force_int(request.values.get('favorite_count', 0))
    comment_count = force_int(request.values.get('comment_count', 0))
    sale_count = force_int(request.values.get('sale_count', 0))
    view_count = force_int(request.values.get('view_count', 0))


    return jsonify(success=True, code=33, message='success!')


