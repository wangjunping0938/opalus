import os
import re
import sys

import requests

sys.path.append(os.path.abspath(os.path.dirname("__file__")))
from app.models.color import Color
from app.extensions import celery
from manage import create_app

app = create_app()



def get_cmyk(color):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36',
    }
    rgb = ','.join(color.rgb)
    data = {'RGB_R': rgb[0], 'RGB_G': rgb[1], 'RGB_B': rgb[2], 'rgb_iccprofile': '0', 'cmyk_iccprofile': '9',
            'intent': '3'}
    cmyk_host = 'https://www.colortell.com/rgb2cmyk'
    response = requests.post(cmyk_host, data=data,headers=headers)
    rex = re.compile(r'<td><code>(\d*?).</code></td>', re.M)
    result = rex.findall(response.text)
    result = [str(i / 100) for i in result]
    cmyk = ','.join(result)
    return cmyk


def get_pantone(color):
    headers = {
        'X-Requested-With': 'XMLHttpRequest',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36',
        'Host': 'www.qtccolor.com',
        'Content-Type': 'application/x-www-form-urlencoded'
    }

    pantone_host = 'https://www.qtccolor.com/findColor.aspx'
    params = {'render': '1', 'subbrand': '4', 'take': '30', 'word': color.hex}
    response = requests.get(pantone_host, params=params, headers=headers)
    rex = re.compile(r'<div class="ColorCode">(.+?)</div></a>', re.M)
    result = rex.findall(response.text)
    pantone = result[0]
    return pantone



@celery.task()
def cmyk():
    page = 1
    per_page = 100
    is_end = False
    total = 1
    while not is_end:
        # 倒序
        data = Color.objects(cmyk='').order_by('created_at').paginate(page=page, per_page=per_page)
        if not len(data.items):
            print("get data is empty! \n")
            break

        for i, color in enumerate(data.items):
            if color.cmyk:
                continue
            cmyk = get_cmyk(color)
            color.update(cmyk=cmyk)

        total += 1
        print("current page %s: \n" % page)
        page += 1
        if len(data.items) < per_page:
            is_end = True
    print("is over execute count %s\n" % total)



@celery.task()
def pantone():
    page = 1
    per_page = 100
    is_end = False
    total = 1
    while not is_end:
        # 倒序
        data = Color.objects(pantone='').order_by('created_at').paginate(page=page, per_page=per_page)
        if not len(data.items):
            print("get data is empty! \n")
            break

        for i, color in enumerate(data.items):
            if color.pantone:
                continue
            pantone = get_pantone(color)
            color.update(pantone=pantone)

        total += 1
        print("current page %s: \n" % page)
        page += 1
        if len(data.items) < per_page:
            is_end = True
    print("is over execute count %s\n" % total)

