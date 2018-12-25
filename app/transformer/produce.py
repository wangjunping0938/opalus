# encoding: utf-8
from app.helpers.constant import prize_options
from app.models.category import Category
from app.models.brand import Brand
from app.models.color import Color

from bson import ObjectId


def t_produce_view(d):
    if not d:
        return {}
    return {
        '_id': str(d._id),
        'title': d.title,
        'name': d.name,
        'category_id': d.category_id,
        'category': fetch_category(d.category_id),
        'url': d.url,
        'img_url': d.cover.img_url,
        'thumb': d.cover.path,
        'company': d.company,
        'designer': d.designer,
        'kind': d.kind,
        'cover': d.cover(),
        # 'prize_id': d.prize_id,
        # 'prize': fetch_prize(d.prize_id, d.prize),
        # 'prize_level': d.prize_level,
        # 'prize_time': d.prize_time,
        'brand_id': d.brand_id,
        'brand': fetch_brand(d.brand_id),
        'remark': d.remark,
        'tags': d.tags,
        'material_tags': d.material_tags,
        'technique_tags': d.technique_tags,
        'style_tags': d.style_tags,
        'other_tags': d.other_tags,
        'total_tags': d.total_tags,
        'currency_type': d.currency_type,
        'price': d.price,
    }


def t_produce_list(data):
    if not data:
        return []
    rows = []
    # 过滤数据
    for i, d in enumerate(data.items):
        row = {
            '_id': str(d._id),
            'title': d.title,
            'category_id': d.category_id,
            'category': fetch_category(d.category_id),
            'url': d.url,
            'company': d.company,
            'designer': d.designer,
            'kind': d.kind,
            'prize_names': get_prize(d.prize),
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
            'total_tags_s': ','.join(d.total_tags),
            'editor_id': d.editor_id,
            'user_id': d.user_id,
            'channel': d.channel,
            'stick': d.stick,
            'deleted': d.deleted,
            'status': d.status,
            'currency_type': d.currency_type,
            'price': d.price,
            'created_at': d.created_at,
            'updated_at': d.updated_at,
            'cover': d.cover(),
        }
        if row['cover']:
            row.update({'thumb': d.cover().get_thumb_path()})
        rows.append(row)
    return rows

def t_admin_produce_list(data):
    if not data:
        return []
    rows = []
    # 过滤数据
    for i, d in enumerate(data.items):
        row = {
            '_id': str(d._id),
            'title': d.title,
            'category_id': d.category_id,
            'category': fetch_category(d.category_id),
            'url': d.url,
            'company': d.company,
            'designer': d.designer,
            'kind': d.kind,
            'prize_names': get_prize(d.prize),
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
            'total_tags_s': ','.join(d.total_tags),
            'editor_id': d.editor_id,
            'user_id': d.user_id,
            'channel': d.channel,
            'stick': d.stick,
            'deleted': d.deleted,
            'status': d.status,
            'currency_type': d.currency_type,
            'price': d.price,
            'created_at': d.created_at,
            'updated_at': d.updated_at,
            'cover': d.cover(),
        }
        if row['cover']:
            row.update({'thumb': d.cover().get_thumb_path()})
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
def get_prize(prize):
    prize_names = []
    for i in prize:
        prize_names.append(i['name'])
    prize_names = ','.join(prize_names)
    return prize_names

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


