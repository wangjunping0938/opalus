import time
import sys
import os

from app.helpers.common import gen_mongo_id
sys.path.append(os.path.abspath(os.path.dirname("__file__")))

from app.models.image import Image
from qiniu import Auth, put_data
from app.extensions import celery
from app import create_app
from app.env import cf
app = create_app()


def upload():
    page = 1
    per_page = 100
    is_end = False
    total = 0
    while not is_end:
        data = Image.objects.paginate(page=page, per_page=per_page)
        if not data:
            print("get data is empty! \n")
            break

        for i, image in enumerate(data.items):
            if not image.path:
                result = {'success': 0, 'message': ''}
                accessKey = cf.get('qiniu', 'access_key')
                secretKey = cf.get('qiniu', 'secret_key')
                bucket_name = cf.get('qiniu', 'bucket_name')
                key = "%s/%s/%s/%s" % (bucket_name, 'image', time.strftime("%y%m%d"), gen_mongo_id())
                try:
                    # 构建鉴权对象
                    q = Auth(accessKey, secretKey)
                    # 生成上传 Token，可以指定过期时间等
                    token = q.upload_token(bucket_name, key, 600)
                    ret, info = put_data(token, key, image.local_path)
                    if not info.status_code == 200:
                        print(info)
                        result['message'] = info.error
                        return result
                    result['success'] = 1
                    image.update(path=key)
                    total += 1
                except Exception as e:
                    print('上传七牛云失败，错误图片_id ', str(image._id))

        print("current page %s: \n" % page)
        page += 1
        if len(data.items) < per_page:
            is_end = True

    print("is over execute count %s\n" % total)


upload()