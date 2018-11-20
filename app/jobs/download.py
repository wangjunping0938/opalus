import time
import sys
import os
sys.path.append(os.path.abspath(os.path.dirname("__file__")))

from app.models.image import Image

import requests
from app.helpers.common import gen_mongo_id
import imghdr

from app.extensions import celery
from app import create_app
from app.env import cf

app = create_app()


# 保存图片到本地
def save_image(response, image, ext):
    if image:
        local_name = gen_mongo_id()  # 本地文件名
        prefix = cf.get('base', 'upload_folder')  # 本地地址前缀
        bucket_name = 'opalus'
        prefix = 'D:/img'
        # 本地文件夹
        local_dir = "%s/%s/%s/%s" % (prefix, bucket_name, 'image', time.strftime("%y%m%d"))
        # 本地地址
        local_path = "%s/%s/%s/%s/%s" % (prefix, bucket_name, 'image', time.strftime("%y%m%d"),local_name)
        if not os.path.exists(local_dir):  # 如果没有文件夹，创建文件夹
            os.makedirs(local_dir)
        with open(local_path+"."+ext, 'wb') as f:  # 保存图片
            f.write(response.content)
        # 保存数据
        # print(Image.size(local_path)) # 图片尺寸
        image.local_path = local_path
        # image.local_name = image.name
        image.ext = ext
        image.save()



# 下载图片
# @celery.task()
def download():
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
            if not image.local_path:
                try:
                    response = requests.get(image.img_url)
                    ext = imghdr.what('', response.content)  # 扩展名
                    if ext is None:
                        ext = 'jpeg'
                    save_image(response, image, ext)
                except Exception as e:
                    print('下载图片失败', str(image._id))

        print("current page %s: \n" % page)
        page += 1
        if len(data.items) < per_page:
            is_end = True

    print("is over execute count %s\n" % total)


download()
