from flask import request, jsonify
from . import api
from app.lib.grab import fetch_platform_site, push_product

## TEST
@api.route('/test/view')
def test_view():

    mark = request.values.get('mark', '')
    if not mark:
        return jsonify(code=3001, message='缺少请求参数！')

    result = fetch_platform_site(mark)

    return jsonify(code=0, message='缺少请求参数！', data=result)

@api.route('/test/product')
def test_push_product():

    data = {
            'url': 'http://www.baidu.com',
            'title': '百度',
            'site_from': 3,
            'site_type': 2,
            'brand_name': '太火鸟1',
            'brand_address': '北京yjmhj1',
            'info_name': '新浪',
            'tags': '希望,美好,喜欢,test',
            'out_number': "232342342",
            'love_count': 3,
            'sale_count': 8,
            'category_tags': "智能家具,数码"

        }


    result = push_product(**data)

    return jsonify(code=0, message='缺少请求参数！', data=result)
