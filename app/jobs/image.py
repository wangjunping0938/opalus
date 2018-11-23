import time
import os
import sys

sys.path.append(os.path.abspath(os.path.dirname("__file__")))
from app.models.image import Image
from qiniu import Auth, put_data
from app.extensions import celery
from app.env import cf
import requests
import imghdr


def decorate(func):
    def loop(self, *args, **kwargs):
        while not self.is_end:
            data = Image.objects.paginate(page=self.page, per_page=self.per_page)
            if not len(data.items):
                print("get data is empty! \n")
                break
            for i, image in enumerate(data.items):
                func(self, image)
            print("current page %s: \n" % self.page)
            self.page += 1
            if len(data.items) < self.per_page:
                self.is_end = True
        print("is over execute count %s\n" % self.total)

    return loop


class ImageOperation:
    def __init__(self):
        self.bucket_name = cf.get('qiniu', 'bucket_name')
        self.accessKey = cf.get('qiniu', 'access_key')
        self.secretKey = cf.get('qiniu', 'secret_key')
        self.page = 1
        self.per_page = 100
        self.is_end = False
        self.total = 0
        self.prefix = cf.get('base', 'upload_folder')  # 本地地址前缀

    @decorate
    def download(self, image):
        if not image.local_path:
            local_name = str(image._id)
            response = ''
            try:
                print('开始下载,图片_id', str(image._id))
                if image.path:
                    response = requests.get("https://" + image.get_thumb_path()['sm'])
                elif image.img_url:
                    response = requests.get(image.img_url)

                ext = imghdr.what('', response.content)  # 扩展名
                if ext is None:
                    ext = 'jpeg'

                # 本地文件夹
                local_dir = os.path.join(self.prefix, 'image', time.strftime("%y%m%d"))
                # 本地地址
                if not os.path.exists(local_dir):  # 如果没有文件夹，创建文件夹
                    os.makedirs(local_dir)

                with open(local_dir + '/' + local_name + '.' + ext, 'wb') as f:  # 保存图片
                    w_long = f.write(response.content)
                with open(local_dir + '/' + local_name + '.' + ext, 'rb') as f:  # 查看图片
                    r_long = len(f.read())

                if w_long == r_long:  # 保证图片保存成功
                    # 保存数据
                    # print(Image.size(local_path)) # 图片尺寸
                    mogo_local_dir = os.path.join('image', time.strftime("%y%m%d"))
                    image.update(ext=ext, local_path=mogo_local_dir, local_name=local_name)
                    self.total += 1
                    print('下载图片成功,成功图片_id', str(image._id))
                    return
                print('保存图片失败,错误图片_id', str(image._id))

            except Exception as e:
                print('下载图片失败,错误图片_id', str(image._id))

    @decorate
    def upload(self, image):
        if not image.path:
            key = os.path.join(self.bucket_name, 'image', time.strftime("%y%m%d"), image.local_name)
            try:
                print('开始上传,图片_id', str(image._id))
                # 构建鉴权对象
                q = Auth(self.accessKey, self.secretKey)
                # 生成上传 Token，可以指定过期时间等
                token = q.upload_token(self.bucket_name, key, 600)
                ret, info = put_data(token, key, os.path.join(self.prefix, image.local_path))
                if not info.status_code == 200:
                    return info.error
                image.update(path=key)
                self.total += 1
                print('上传七牛云成功，成功图片_id', str(image._id))
            except Exception as e:
                print('上传七牛云失败，错误图片_id ', str(image._id))


@celery.task()
def upload():
    u = ImageOperation()
    u.upload()


@celery.task()
def download():
    d = ImageOperation()
    d.download()



