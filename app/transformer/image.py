#encoding: utf-8
from app.helpers.constant import prize_options
from app.models.category import Category
from app.models.brand import Brand
from app.models.color import Color

from bson import ObjectId

def t_image_view(d):
    if not d:
        return {}
    return {
        '_id': str(d._id),
        'title': d.title,
        'name': d.name,
        'category_id': d.category_id,
        'category': fetch_category(d.category_id),
        'thumb': d.get_thumb_path(),
        'url': d.url,
        'img_url': d.img_url,
        'company': d.company,
        'designer': d.designer,
        'kind': d.kind,
        'prize_id': d.prize_id,
        'prize': fetch_prize(d.prize_id, d.prize),
        'prize_level': d.prize_level,
        'prize_time': d.prize_time,
        'brand_id': d.brand_id,
        'brand': fetch_brand(d.brand_id),
        'remark': d.remark,
        'tags': d.tags,
        'material_tags': d.material_tags,
        'technique_tags': d.technique_tags,
        'style_tags': d.style_tags,
        'other_tags': d.other_tags,
        'total_tags': d.total_tags,
        'color_ids': d.color_ids,
        'colors': color_tran(d.color_ids),
        'currency_type': d.currency_type,
        'price': d.price,
    }

def t_image_list(data):
    if not data:
        return []
    rows = []
    # 过滤数据
    for i, d in enumerate(data.items):
        row = {
            '_id': str(d._id),
            'title': d.title,
            'name': d.name,
            'category_id': d.category_id,
            'category': fetch_category(d.category_id),
            'thumb': d.get_thumb_path(),
            'url': d.url,
            'img_url': d.img_url,
            'company': d.company,
            'designer': d.designer,
            'kind': d.kind,
            'prize_id': d.prize_id,
            'prize': fetch_prize(d.prize_id, d.prize),
            'prize_level': d.prize_level,
            'prize_time': d.prize_time,
            'brand_id': d.brand_id,
            'brand': fetch_brand(d.brand_id),
            'tags': d.tags,
            'tags_s': ','.join(d.tags),
            'evt_label': evt_label(d.evt),
            'material_tags': d.material_tags,
            'technique_tags': d.technique_tags,
            'style_tags': d.style_tags,
            'other_tags': d.other_tags,
            'total_tags': d.total_tags,
            'total_tags_s':','.join(d.total_tags),
            'user_id': d.user_id,
            'channel': d.channel,
            'stick': d.stick,
            'deleted': d.deleted,
            'status': d.status,
            'color_ids': d.color_ids,
            'colors': color_tran(d.color_ids),
            'currency_type': d.currency_type,
            'price': d.price,
            'created_at': d.created_at,
            'updated_at': d.updated_at,
        }
        rows.append(row)
    return rows

# 分类
def fetch_category(category_id):
    category = None
    if category_id:
        category = Category.objects(_id=int(category_id)).first()
    return category

# 奖项
def fetch_prize(prize_id, prize):
    if prize_id:
        prize_label = prize_options(prize_id)['name']
    elif prize:
        prize_label = prize
    else:
        prize_label = ''

    return prize_label

# 品牌
def fetch_brand(brand_id):
    brand = None
    if brand_id:
        brand = Brand.objects(_id=brand_id).first()
    return brand

# 来源
def evt_label(evt):
    evt_label = ''
    if evt == 5:
        evt_label = 'WJP'
    elif evt == 3:
        evt_label = 'LZB'
    elif evt == 2:
        evt_label = 'TIAN'
    else:
        evt_label = '--'

    return evt_label

# 色值
def color_tran(color_ids):
    colors = []
    for i in color_ids:
        if len(i) == 24:
            color = Color.objects(_id=ObjectId(i)).first()
            if color:
                colors.append(color)
    return colors
