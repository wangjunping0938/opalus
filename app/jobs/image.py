import time
import os
import sys
sys.path.append(os.path.abspath(os.path.dirname("__file__")))
from app.models.image import Image
from qiniu import Auth, put_data
from app.extensions import celery
from app.env import cf
import requests
from app.helpers.common import gen_mongo_id
import imghdr


class ImageOperation:
    def __init__(self, opera):
        self.local_name = gen_mongo_id()
        self.bucket_name = cf.get('qiniu', 'bucket_name')
        self.accessKey = cf.get('qiniu', 'access_key')
        self.secretKey = cf.get('qiniu', 'secret_key')
        self.opera = opera
        self.page = 1
        self.per_page = 100
        self.is_end = False
        self.total = 0

    def save_image(self, response, image, ext):
        if image:
            prefix = cf.get('base', 'upload_folder')  # 本地地址前缀
            # 本地文件夹
            local_dir = "%s/%s/%s/%s" % (prefix, self.bucket_name, 'image', time.strftime("%y%m%d"))
            # 本地地址
            local_path = "%s/%s/%s/%s/%s%s" % (
                prefix, self.bucket_name, 'image', time.strftime("%y%m%d"), self.local_name, "." + ext)
            if not os.path.exists(local_dir):  # 如果没有文件夹，创建文件夹
                os.makedirs(local_dir)
            with open(local_path, 'wb') as f:  # 保存图片
                f.write(response.content)
            # 保存数据
            # print(Image.size(local_path)) # 图片尺寸
            image.update(ext=ext, local_path=local_path)

    def operation(self):

        while not self.is_end:
            data = Image.objects.paginate(page=self.page, per_page=self.per_page)
            if not data:
                print("get data is empty! \n")
                break
            for i, image in enumerate(data.items):
                if self.opera == 'upload':
                    if not image.path:
                        key = "%s/%s/%s/%s" % (self.bucket_name, 'image', time.strftime("%y%m%d"), self.local_name)
                        try:
                            # 构建鉴权对象
                            q = Auth(self.accessKey, self.secretKey)
                            # 生成上传 Token，可以指定过期时间等
                            token = q.upload_token(self.bucket_name, key, 600)
                            ret, info = put_data(token, key, image.local_path)
                            if not info.status_code == 200:
                                return info.error
                            image.update(path=key)
                            self.total += 1
                        except Exception as e:
                            print('上传七牛云失败，错误图片_id ', str(image._id))
                elif self.opera == 'download':
                    if not image.local_path:
                        try:
                            response = requests.get(image.img_url)
                            ext = imghdr.what('', response.content)  # 扩展名
                            if ext is None:
                                ext = 'jpeg'
                            self.save_image(response, image, ext)
                            self.total += 1
                        except Exception as e:
                            print('下载图片失败,错误图片_id', str(image._id))
            print("current page %s: \n" % self.page)
            self.page += 1
            if len(data.items) < self.per_page:
                self.is_end = True
        print("is over execute count %s\n" % self.total)


@celery.task()
def upload():
    u = ImageOperation('upload')
    u.operation()


@celery.task()
def download():
    d = ImageOperation('download')
    d.operation()

