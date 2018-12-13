import time
import os
import sys

sys.path.append(os.path.abspath(os.path.dirname("__file__")))
from flask import current_app
from app.models.image import Image
from qiniu import Auth, put_data, put_file
from app.helpers.common import gen_mongo_id
from app.extensions import celery
from app.env import cf
import requests
import imghdr


def decorate(func):
    def loop(self, *args, **kwargs):
        query = {}
        query['path'] = ''
        query['deleted'] = 0
        while not self.is_end:
            # 倒序 
            data = Image.objects(**query).order_by('created_at').paginate(page=self.page, per_page=self.per_page)
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
        self.per_page = 10
        self.is_end = False
        self.total = 0
        self.prefix = cf.get('base', 'upload_folder')  # 本地地址前缀

    @decorate
    def download(self, image):
        if not image.local_path:
            response = ''
            try:
                print('开始下载,图片: %s' % str(image._id))
                if image.path:
                    response = requests.get(os.path.join(current_app.config['ASSET_URL'], image.path))
                elif image.img_url:
                    response = requests.get(image.img_url)

                ext = imghdr.what('', response.content)  # 扩展名
                if ext is None:
                    ext = 'jpeg'

                local_name = str(image._id) + '.' + ext

                # mongo存储路径
                mongo_dir = os.path.join('image', time.strftime("%y%m%d"))
                # 本地文件夹
                local_dir = os.path.join(self.prefix, mongo_dir)
                # 本地地址
                if not os.path.exists(local_dir):  # 如果没有文件夹，创建文件夹
                    os.makedirs(local_dir)

                with open(os.path.join(local_dir, local_name), 'wb') as f:  # 保存图片
                    w_long = f.write(response.content)
                with open(os.path.join(local_dir, local_name), 'rb') as f:  # 查看图片
                    r_long = len(f.read())

                if w_long == r_long:  # 保证图片保存成功
                    # 保存数据
                    # print(Image.size(local_path)) # 图片尺寸
                    image.update(ext=ext, local_path=mongo_dir, local_name=local_name)
                    self.total += 1
                    print('下载图片成功: %s' % str(image._id))
                    return
                print('保存图片失败: %s' % str(image._id))

            except Exception as e:
                print('下载图片异常:', str(e))

    @decorate
    def upload(self, image):
        if not image.path:
            key = os.path.join(self.bucket_name, 'image', time.strftime("%y%m%d"), gen_mongo_id())
            try:
                print('开始上传,图片ID: %s' % str(image._id))
                # 构建鉴权对象
                q = Auth(self.accessKey, self.secretKey)
                # 生成上传 Token，可以指定过期时间等
                token = q.upload_token(self.bucket_name, key, 600)
                if image.local_path:
                    url = os.path.join(self.prefix, image.local_path, image.local_name)
                    ret, info = put_file(token, key, url)
                elif image.img_url:
                    response = requests.get(image.img_url)
                    if response.status_code == 200:
                        ret, info = put_data(token, key, response.content)
                    else:
                        print('获取图片错误: %s' % response.status_code)
                        return False
                else:
                    print('图片地址不存在ID: %s' % str(image._id))
                    return False

                if not info.status_code == 200:
                    print('上传七牛失败: %s' % info.error)
                    return False

                if not info.status_code == 200:
                    return info.error
                image.update(path=key)
                self.total += 1
                print('上传七牛云成功: %s' % str(image._id))
            except Exception as e:
                print('上传七牛云失败: %s' % str(e))
        else:
            print('图片已处理:%s' % str(image._id))


@celery.task()
def upload():
    u = ImageOperation()
    u.upload()


@celery.task()
def download():
    d = ImageOperation()
    d.download()


# 批量修改
@celery.task()
def image_update():

    page = 1
    perPage = 100
    isEnd = False
    successStatCount = 0
    failStatCount = 0
    query = {}
    query['deleted'] = 0
    #query['status'] = 1
    #query['channel'] = 'g_mark'

    while not isEnd:
        data = Image.objects(**query).order_by('-created_at').paginate(page=page, per_page=perPage)
        if not data:
            print("get data is empty! \n")
            continue

        # 过滤数据
        for i, d in enumerate(data.items):
            #img_url = d.img_url.strip()
            if d.channel == 'g_mark':
                #ok = d.update(prize_id=8)
                ok = True
                if ok:
                    successStatCount += 1
                else:
                    failStatCount += 1

        print("current page %s: \n" % page)
        page += 1
        if len(data.items) < perPage:
            isEnd = True

    print("is over execute SuccessCount %d ---- failCount: %d\n" % (successStatCount, failStatCount))

