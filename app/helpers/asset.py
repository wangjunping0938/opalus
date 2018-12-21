# -*- coding:utf-8 -*-
import os
import time
from flask import current_app

from qiniu import Auth, put_file, put_data, put_stream, etag, BucketManager
import qiniu.config
from app.helpers.common import gen_mongo_id
from app.models.asset import Asset
from app.helpers.common import force_int

# 处理图片
from app.models.image import Image


def handle_file(f, **param):
    result = {'success': 0, 'message': ''}
    if not f:
        result['message'] = '文件不存在！'
        return result

    bucket_name = current_app.config['QN_BUCKET_NAME']
    # 文件名
    fname = f.filename
    # 获取文件后缀
    ext = fname.rsplit('.',1)[1]

    mime = f.mimetype

    size = f.content_length

    blob = f.read()
    size = len(blob)

    user_id = force_int(param['user_id'], 0)
    target_id = param['target_id']
    asset_type = force_int(param['asset_type'], 1)
    evt = param['evt']
    #上传到七牛后保存的文件名
    asset_name = gen_asset_name(asset_type)

    # 文件路径
    path = "%s/%s/%s/%s" % (bucket_name, asset_name, time.strftime("%y%m%d"), gen_mongo_id())

    # 上传至七牛
    qnResult = up_qiniu(blob, path)

    if not qnResult['success']:
        result['message'] = qnResult['message']
        return result

    row = {
        'name': fname,
        'mime': mime,
        'ext': ext,
        'size': size,
        'path': path,
        'asset_type': asset_type,
        'domain': asset_name,
        'target_id': target_id,
        'user_id': user_id
    }

    if evt == 1:
        # 保存至素材表
        if asset_type == 2:
            try:
                row.pop('mime')
                row.pop('domain')
                image = Image(**row)
                ok = image.save()
                if not ok:
                    result['message'] = '保存素材失败'
                    return result

                row['_id'] = str(image._id)

            except(Exception) as e:
                result['message'] = str(e)
                return result
        else:
        # 保存至asset表
            try:
                asset = Asset(**row)
                ok = asset.save()
                if not ok:
                    result['message'] = '保存附件失败'
                    return result

                row['_id'] = str(asset._id)

            except(Exception) as e:
                result['message'] = str(e)
                return result

    result['success'] = 1
    result['data'] = row
    return result


# 七牛上传附件
def up_qiniu(blob, key):
    result = {'success': 0, 'message': ''}
    accessKey = current_app.config['QN_ACCESS_KEY']
    secretKey = current_app.config['QN_SECRET_KEY']
    bucketName = current_app.config['QN_BUCKET_NAME']

    try:
        #构建鉴权对象
        q = Auth(accessKey, secretKey)
        #生成上传 Token，可以指定过期时间等
        token = q.upload_token(bucketName, key, 600)
        ret, info = put_data(token, key, blob)
        if not info.status_code == 200:
            result['message'] = info.error
            return result

        result['success'] = 1
        return result
    except(Exception) as e:
        result['message'] = str(e)
        return result

# 删除源文件
def remove_qiniu(key):
    access_key = current_app.config['QN_ACCESS_KEY']
    secret_key = current_app.config['QN_SECRET_KEY']
    bucket_name = current_app.config['QN_BUCKET_NAME']
    result = {'success': 0, 'message': ''}
    try:
        #构建鉴权对象
        q = Auth(access_key, secret_key)
        #初始化BucketManager
        bucket = BucketManager(q)

        #删除bucket_name 中的文件 key
        ret, info = bucket.delete(bucket_name, key)
        if not info.status_code == 200:
            result['message'] = info.error
            return result

        result['success'] = 1
        return result
    except(Exception) as e:
        result['message'] = str(e)
        return result
    

# 获取assetType所对应路径
def gen_asset_name(asset_type):
    name = 'custom'
    if asset_type == 1:
        name = 'custom'
    elif asset_type == 2:
        name = 'image'
    elif asset_type == 5:
        name = 'brand'
    elif asset_type == 7:
        name = 'column'

    return name
