import os
import sys

sys.path.append(os.path.abspath(os.path.dirname("__file__")))
from app.models.image import Image
from app.models.produce import Produce
from app.extensions import celery
import functools
from bson import ObjectId



def decorate(func):
    @functools.wraps(func)
    def loop(*args, **kwargs):
        page = 1
        per_page = 100
        is_end = False
        total = 0
        query = {}
        while not is_end:
            data = Image.objects(**query).paginate(page=page, per_page=per_page)
            if not len(data.items):
                print("get data is empty! \n")
                break
            for i, image in enumerate(data.items):
                if image.target_id:
                    continue
                func(image)
            print("current page %s: \n" % page)
            page += 1
            total += 1
            if len(data.items) < per_page:
                is_end = True
        print("is over execute count %s\n" % total)

    return loop



@decorate
def save_data(image):
    # 根据标题 和 渠道 判断 是否重复产品
    produce = Produce.objects(title=image.title,channel=image.channel).first()
    if produce:
        print('此素材已存在产品库', str(produce._id))
    else:
        print('新创建产品库')
        produce = Produce()
        produce.title = image.title  # 标题
        produce.img_url = image.url  # 原文地址
        produce.channel = image.channel  # 渠道
        produce.tags = image.tags  # 标签
        produce.brand_tags = image.brand_tags
        produce.color_tags = image.color_tags
        produce.material_tags = image.material_tags
        produce.other_tags = image.other_tags
        produce.style_tags = image.style_tags
        produce.technique_tags = image.technique_tags
        produce.total_tags = image.total_tags
        produce.designer = image.designer  # 设计者姓名
        produce.company = image.company  # 公司
        produce.price = image.price  # 价格
        produce.currency_type = image.currency_type  # 币种
        produce.kind = image.kind  # 类型
        produce.brand_id = image.brand_id  # 品牌id
        produce.category_id = image.category_id
        produce.remark = image.remark  # 备注
        produce.info = image.info  # 信息
        produce.evt = image.evt  # 来源
        if image.prize_id:
            prize_list = []
            prize_dict = {}
            prize_dict['id'] = image.prize_id
            prize_dict['name'] = image.prize
            prize_dict['time'] = image.prize_time
            prize_dict['level'] = image.prize_level
            prize_list.append(prize_dict)
            produce.prize = prize_list
        ok = produce.save()
        if ok:
            print('保存成功,产品库ID：', str(produce._id))
        else:
            print('导入失败,失败素材ID', str(image._id))
    # 保存素材target
    ok = image.update(target_id=str(produce._id))

    if ok:
        print('保存素材target成功,成功素材ID', str(image._id))
    else:
        print('保存素材target失败,失败素材ID', str(image._id))



