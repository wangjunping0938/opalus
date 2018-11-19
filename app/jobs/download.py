import time
from app.models.image import Image
import os
import requests
from app.helpers.common import gen_mongo_id

from app import create_app

app = create_app()

# 保存图片到本地
def save_image(response, image):
    if image:
        local_name = image.name
        bucket_name = 'opalus'
        local_path = "%s/%s/%s/%s" % (bucket_name, 'image', time.strftime("%y%m%d"), gen_mongo_id())
        if not os._exists(local_path):
            os.makedirs(local_path)
        with open(local_path + '/' + local_name, 'wb') as f:
            f.write(response.content)
        image.local_path = local_path
        image.local_name = image.name
        image.save()

# 下载图片
def download():
    image_all = Image.objects.all()
    if image_all:
        for image in image_all:
            image_id = image._id
            if image.local_path:
                image = Image.objects(_id=image_id).first()
                if image:
                    try:
                        response = requests.get(image.img_url)
                        save_image(response, image)
                    except Exception as e:
                        print('下载图片失败', str(image_id))
    else:
        print('无图片')


download()
