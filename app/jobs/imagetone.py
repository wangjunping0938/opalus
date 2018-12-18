import os
import sys
from io import BytesIO
from flask import g, current_app
sys.path.append(os.path.abspath(os.path.dirname("__file__")))
from app.models.image import Image
from app.extensions import celery
from app.env import cf
import requests
import PIL
import numpy as np
import scipy.cluster
from app.models.color import Color
from bson import ObjectId


#  读取图片并返回ImageExtractor 实例化对象
def read_file(response):
    # if not os.path.exists(image_path):
    #     raise ValueError('Image path {} not exist.'.format(image_path))
    img = ImageExtractor()
    img.raw_image = PIL.Image.open(BytesIO(response.content))
    img.initialized = True
    return img


# 图片处理
class ImageExtractor(object):
    def __init__(self):
        # 加工图
        self.image = None
        # 原图
        self.raw_image = None
        self.image_array = None
        # 颜色
        self.tones = None  # rgb
        self.tones_str = []
        self.hex = None  # hex
        self.initialized = False
        self.tone_image = None

    # 获取加工图
    def reduce_size(self, max_width):
        # 原图尺寸
        h, w = self.raw_image.size[0], self.raw_image.size[1]
        if w <= max_width:
            self.image = self.raw_image
            return self
        new_w = int(max_width)
        new_h = int(new_w / w * h)
        # 加工图
        self.image = self.raw_image.resize((new_h, new_w), Image.ANTIALIAS)

    # 像素
    def unstack_pixel(self):
        image_array = np.asarray(self.image)
        shape = image_array.shape
        self.image_array = image_array.reshape(scipy.product(shape[:2]), shape[2]).astype(float)

    # 获取颜色 获取最主要的num种
    def extract_tones(self, num):
        image_array = self.image_array
        codes, dist = scipy.cluster.vq.kmeans(image_array, num)
        codes = [[int(_) for _ in code] for code in codes]
        self.tones = codes
        for i in self.tones:
            j = ",".join('%s' % z for z in i)
            self.tones_str.append(j)
        self.rgb2hex()

    #  打印顔色
    def get_str_tones(self):
        for ind, each_tone in enumerate(self.tones, 1):
            print(f'Tone {ind}: {each_tone}')

    # 获取 hex值
    def rgb2hex(self):
        self.hex = []
        for rgb in self.tones:
            strs = "#"
            for j in range(0, 3):
                s = hex(rgb[j])[2:]
                if len(s) < 2:
                    s += '0'
                strs += s
            self.hex.append(strs)

    def rgb_to_cmyk(self):
        pass

    def rgb_to_pantone(self):
        pass


@celery.task()
def get_tones():
    query = {}
    query['deleted'] = 0
    #query['color_ids'] = []
    page = 1
    per_page = 100
    is_end = False
    total = 1
    asset_url = current_app.config['ASSET_URL']
    while not is_end:
        # 倒序
        data = Image.objects(**query).order_by('-created_at').paginate(page=page, per_page=per_page)
        if not len(data.items):
            print("get data is empty! \n")
            break
        for i, image in enumerate(data.items):
            if image.color_ids:
                print('色值已存在，跳过...')
                continue
            img_url = ''
            if image.path:
                img_url = os.path.join(asset_url, image.path)
            else:
                print('没有上传图片，跳过..')
                continue
                img_url = image.img_url

            try:
                response = requests.get(img_url)
            except:
                print('网络超时访问图片地址失败',str(image._id))
                continue
            try:
                if response.status_code == 200:
                    img = read_file(response)
                else:
                    print('读取图片失败：%s', response.status_code)
                    continue
            except:
                print('读取文件失败: %s',str(image._id))
                continue
            try:
                img.reduce_size(img.raw_image.size[1])
                img.unstack_pixel()
                img.extract_tones(4)
                color_ids = []
                for j in range(len(img.tones_str)):
                    color = Color.objects(rgb=img.tones_str[j]).first()
                    if color:
                        color_ids.append(str(color._id))
                    else:
                        color = Color(rgb=img.tones_str[j], hex=img.hex[j])
                        ok = color.save()
                        color_ids.append(str(ok._id))
                ok = image.update(color_ids=color_ids)
                if ok:
                    print('更新成功: %s' % str(image._id))
                else:
                    print('更新失败：%s' % str(image._id))
            except:
                print('解析图片失败：%s',str(image._id))
                continue
        total += 1
        print("current page %s: \n" % page)
        page += 1
        if len(data.items) < per_page:
            is_end = True
    print("is over execute count %s\n" % total)

