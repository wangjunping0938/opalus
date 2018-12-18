import os
import sys

sys.path.append(os.path.abspath(os.path.dirname("__file__")))
from app.models.image import Image
from app.models.design_case import DesignCase
from app.models.design_company import DesignCompany
from bson import ObjectId
from app.helpers.constant import prize_options
from app.extensions import celery
import functools


def decorate(func):
    @functools.wraps(func)
    def loop(*args, **kwargs):
        page = 1
        per_page = 100
        is_end = False
        total = 0
        query = {}
        query['prize_label'] = '红星奖'
        while not is_end:
            data = DesignCase.objects(**query).paginate(page=page, per_page=per_page)
            if not len(data.items):
                print("get data is empty! \n")
                break
            for i, design_case in enumerate(data.items):
                func(design_case)
            print("current page %s: \n" % page)
            page += 1
            total += 1
            if len(data.items) < per_page:
                is_end = True
        print("is over execute count %s\n" % total)

    return loop


@celery.task()
@decorate
def save_data(design_case):
    image = Image.objects(img_url=design_case.cover_url).first()
    if image:
        print('此作品已存在素材库，添加失败，失败作品_id', str(design_case._id))
    elif design_case.prize_label == '红星奖':
        image = Image()
        image.title = design_case.title  # 标题
        image.tags = design_case.tags  # 标签
        image.img_url = design_case.cover_url  # 图片地址
        image.designer = design_case.designer_name  # 设计者姓名
        # company = DesignCompany.objects(number=design_case.target_id).first()  # 公司
        if design_case.company_name:
            image.company = design_case.company_name  # 公司姓名
        elif design_case.en_company_name:
            image.company = design_case.en_company_name  # 公司姓名
        image.kind = 1  #类型
        # image.brand_id =  #品牌id
        #d = prize_options(design_case.prize_label)  # 获取奖项id和名称的字典映射
        image.prize_id = 4  # 奖项ID
        image.prize = design_case.prize_label  # 奖项名称
        image.prize_level = design_case.prize_level  # 奖项级别
        image.prize_time = design_case.award_time  # 奖项时间
        image.channel = 'opalus_design_case'
        image.evt = 1
        # 保存数据到素材库
        ok = True
        #ok = image.save()
        if not ok:
            print("保存成功: %s" % design_case.prize_label)
        else:
            print("保存失败: %s" % str(design_case._id))

        print('作品以成功转入素材库,成功作品_id', str(design_case._id))
    else:
        print("作品奖项不匹配: %s" % str(design_case._id))

# 1.python manage.py shell
# 2.celery worker -A celery_runner --loglevel=info
# 3. from app.jobs.design_to_image import save_data
#    save_data.delay()
