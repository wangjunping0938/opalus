from flask import request, jsonify
from . import api
from app.models.site import Site
from app.helpers.pager import Pager
from app.helpers.filters import format_datatime
from app.forms.site import SaveForm

## 更新商品信息
@api.route('/site/view')
def site_view():

    mark = request.values.get('mark', '')
    if not mark:
        return jsonify(code=3001, message='缺少请求参数！')

    site = Site.objects(mark=mark).first().to_mongo()
    if not site:
        return jsonify(code=3002, message='站点不存在！')

    # 格式过滤
    site['_id'] = str(site['_id'])
    site['created_at'] = site['created_at'].strftime("%Y-%m-%d %H:%M:%S")
    site['updated_at'] = site['updated_at'].strftime("%Y-%m-%d %H:%M:%S")

    return jsonify(code=0, message='success!', data=site)


