from flask import request, jsonify, current_app
from . import api
from app.models.produce import Produce
from bson import ObjectId
from app.forms.produce import SaveApi
from app.models.image import Image


## 保存/更新
@api.route('/produce/submit', methods=['POST'])
def produce_submit():
    ok = False
    form = SaveApi(request.values)
    if not form.validate_on_submit():
        return jsonify(code=3004, message=str(form.errors))
    data = request.values.to_dict()
    if not data:
        return jsonify(code=3003, message='至少传入一个参数!')
    try:
        if not (data['title'] and data['channel']):
            return jsonify(code=3003, message='标题和渠道为必填')
        if not data['img_urls']:
            return jsonify(code=3003, message='img_urls为空')
        produce = Produce.objects(title=data['title'], channel=data['channel']).first()
        if not produce:
            produce_data = data.copy()
            produce_data.pop('img_urls')
            produce = Produce(**produce_data)
            produce.save()
        img_urls = data['img_urls'].split(',')

        for i in img_urls:
            img_data = {}
            img_data['title'] = data['title']
            img_data['img_url'] = i
            img_data['channel'] = data['channel']
            img_data['url'] = data['url']
            img_data['target_id'] = str(produce._id)
            img = Image.objects(img_url=i).first()
            if not img:
                img = Image(**img_data)
                img.save()
            else:
                img.update(target_id=str(produce._id))
            ok = produce.update(cover_id=str(img._id))

        if ok:
            return jsonify(code=0, message='success!', data=produce)
        else:
            return jsonify(code=3010, message='操作失败！')

    except(Exception) as e:
        return jsonify(code=3011, message=str(e))
