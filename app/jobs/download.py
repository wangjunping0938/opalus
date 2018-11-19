import time
from app.models.image import Image
import os
import requests
from app.helpers.common import gen_mongo_id
from app.extensions import celery
from app import create_app

app = create_app()


# 保存图片到本地
def save_image(response, image):
    if image:
        local_name = image.name  # 本地文件名
        prefix = 'C:\\Users\\aaa10\\Desktop'  # 本地地址前缀
        bucket_name = 'opalus'
        # 本地地址后缀
        local_path = "%s%s/%s/%s/%s" % (prefix, bucket_name, 'image', time.strftime("%y%m%d"), gen_mongo_id())
        if not os._exists(local_path):  # 如果没有文件夹，创建文件夹
            os.makedirs(local_path)
        with open(local_path + '/' + local_name, 'wb') as f:  # 保存图片
            f.write(response.content)
        # 保存数据
        image.local_path = local_path
        image.local_name = image.name
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
                    save_image(response, image)
                except Exception as e:
                    print('下载图片失败', str(image._id))

        print("current page %s: \n" % page)
        page += 1
        if len(data.items) < per_page:
            is_end = True

    print("is over execute count %s\n" % total)


download()
