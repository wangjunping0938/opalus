from flask import request, jsonify
from . import api
from app.models.site import Site
from app.helpers.pager import Pager
from app.helpers.filters import format_datatime
from app.forms.site import SaveForm
from app.lib.grab import fetch_platform_site

## 更新商品信息
@api.route('/site/view', methods=['POST'])
def site_view():

    mark = request.values.get('mark', '')
    if not mark:
        return jsonify(code=3001, message='缺少请求参数！')

    result = fetch_platform_site(mark)
    if result['success']:
        return jsonify(code=0, message='success!', data=result['data'])
    else:
        return jsonify(code=3002, message=result['message'])

