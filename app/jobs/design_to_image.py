import time
import os
import sys

sys.path.append(os.path.abspath(os.path.dirname("__file__")))
from app.models.image import Image
from app.models.design_case import DesignCase
from app.models.design_company import DesignCompany
from bson import ObjectId
from app.helpers.constant import prize_id
from app.extensions import celery
from app.env import cf
from manage import create_app

app = create_app()


def decorate(func):
    def loop(*args, **kwargs):
        page = 1
        per_page = 100
        is_end = False
        total = 0
        while not is_end:
            data = DesignCase.objects.paginate(page=page, per_page=per_page)
            if not len(data.items):
                print("get data is empty! \n")
                break
            for i, design_case in enumerate(data.items):
                func(design_case)
            print("current page %s: \n" % page)
            page += 1
            if len(data.items) < per_page:
                is_end = True
        print("is over execute count %s\n" % total)

    return loop


@celery.task()
@decorate
def save_data(design_case):
    image = Image()
    image.title = design_case.title  # 标题
    image.tags = design_case.tags  # 标签
    image.designer = design_case.designer_name  # 设计者姓名
    company = DesignCompany.objects(_id=ObjectId(design_case.target_id)).first()  # 公司
    image.company = company.name  # 公司姓名
    image.user_id = company.user_id  # 用户id
    # image.kind =   #类型
    # image.brand_id =  #品牌id
    image.prize_id = prize_id(design_case.prize_label)['id']  # 奖项ID
    image.prize = prize_id(design_case.prize_label)['name']  # 奖项名称
    image.prize_level = design_case.prize_level  # 奖项级别
    image.prize_time = design_case.award_time  # 奖项时间
    # image.category_id = #分类

    # 保存数据到素材库
    image.save()


save_data()
