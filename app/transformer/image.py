#encoding: utf-8
from app.helpers.constant import prize_options
from app.models.category import Category
from app.models.brand import Brand

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
        'company': d.company,
        'designer': d.designer,
        'prize_id': d.prize_id,
        'prize': fetch_prize(d.prize_id, d.prize),
        'prize_level': d.prize_level,
        'prize_time': d.prize_time,
        'brand_id': d.brand_id,
        'brand': fetch_brand(d.brand_id),
        'tags': d.tags,
        'material_tags': d.material_tags,
        'technique_tags': d.technique_tags,
        'style_tags': d.style_tags,
        'other_tags': d.other_tags,
    }

# 分类
def fetch_category(category_id):
    category = None
    if category_id:
        category = Category.objects(_id=category_id).first()
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
