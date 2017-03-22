# -*- coding: UTF-8 -*- 
#  爬虫方法集
import datetime
from app.models.site import Site
from app.models.product import Product
from app.helpers.common import force_int, force_float_2

# 获取站点信息
def fetch_platform_site(mark=None):
    if not mark:
        return {'success':False, 'message':'缺少mark参数!'}
    site = Site.objects(mark=mark).first()
    if not site:
        return {'success':False, 'message':'网站不存在!'}

    site = site.to_mongo()
    # 格式过滤
    site['_id'] = str(site['_id'])
    site['created_at'] = site['created_at'].strftime("%Y-%m-%d %H:%M:%S")
    site['updated_at'] = site['updated_at'].strftime("%Y-%m-%d %H:%M:%S")

    return {'success':True, 'message':'success!', 'data':site}


# 更新抓取产品信息
def push_product(**kwargs):

    data = {}
    url = kwargs.get('url', None)
    if not url:
        return {'success':False, 'message': '抓取链接不存在!'}

    site_from = force_int(kwargs.get('site_from', 0))   # 站点来源(从站点配置获取) eg. 1.京东；2.淘宝；3.一条；
    site_type = force_int(kwargs.get('site_type', 0))   # 站点模式(从站点配置获取) eg. 1.销售；2.众筹；3.--
    title = kwargs.get('title', None)   # 名称

    if not site_from:
        return {'success':False, 'message':'站点来源不能为空!'}
    if not site_type:
        return {'success':False, 'message':'站点模式不能为空!'}
    if not title:
        return {'success':False, 'message':'产品名称不能为空!'}

    data['url'] = url
    data['site_from'] = site_from
    data['site_type'] = site_type
    data['title'] = title

    sub_title = kwargs.get('sub_title', None)   # 副名称
    if sub_title:
        data['sub_title'] = sub_title

    out_number = kwargs.get('out_number', None) # 站外编号(skuID)
    if out_number:
        data['out_number'] = out_number

    resume = kwargs.get('resume', None)
    if resume:
        data['resume'] = resume

    content = kwargs.get('content', None)
    if content:
        data['content'] = content

    tags = kwargs.get('tags', None) # 标签(多个用,分隔)
    if tags:
        data['tags'] = tags

    cover_url = kwargs.get('cover_url', None)   # 封面图
    if cover_url:
        data['cover_url'] = cover_url

    brand = {}
    brand_name = kwargs.get('brand_name', None) # 品牌名称
    if brand_name:
        brand['name'] = brand_name

    brand_contact = kwargs.get('brand_contact', None)   # 品牌联系方式

    if brand_contact:
        brand['contact'] = brand_contact

    brand_address = kwargs.get('brand_address', None)   # 品牌地址
    if brand_address:
        brand['address'] = brand_address

    if brand:
        data['brand'] = brand


    category_tags = kwargs.get('category_tags', None)   # 分类(多个用,分隔)
    if category_tags:
        data['category_tags'] = category_tags

    info = {}
    info_name = kwargs.get('info_name', None)   # 众筹发起人
    if info_name:
        info['name'] = info_name

    info_demand = kwargs.get('info_demand', None)   # 众筹标准
    if info_demand:
        info['demand'] = info_demand

    info_rate = force_float_2(kwargs.get('info_rate', 0))   # 众筹进度(百分比/100)
    if info_rate:
        info['rate'] = info_rate

    info_address = kwargs.get('info_address', None)   # 众筹公司地址
    if info_address:
        info['address'] = info_address

    info_contact = kwargs.get('info_contact', None)   # 众筹公司联系方式
    if info_contact:
        info['contact'] = info_contact

    info_time = kwargs.get('info_time', None)   # 众筹公司工作时间
    if info_time:
        info['time'] = info_time

    info_last_time = kwargs.get('info_last_time', None)   # 众筹公司工作时间
    if info_last_time:
        info['last_time'] = info_last_time

    if info:
        data['info'] = info

    rate = force_float_2(kwargs.get('rate', 0))   # 产品评分
    if rate:
        data['rate'] = rate

    cost_price = force_float_2(kwargs.get('cost_price', 0)) # 成本价
    if cost_price:
        data['cost_price'] = cost_price

    sale_price = force_float_2(kwargs.get('sale_price', 0))   # 品牌联系方式
    if sale_price:
        data['sale_price'] = sale_price

    total_price = force_float_2(kwargs.get('total_price', 0))   # 品牌地址
    if total_price:
        data['total_price'] = total_price

    love_count = force_int(kwargs.get('love_count', 0))   # 喜欢/点赞数
    if love_count:
        data['love_count'] = love_count

    favorite_count = force_int(kwargs.get('favorite_count', 0)) # 收藏/订阅数
    if favorite_count:
        data['favorite_count'] = favorite_count

    comment_count = force_int(kwargs.get('comment_count', 0))   # 评论数量
    if comment_count:
        data['comment_count'] = comment_count

    sale_count = force_int(kwargs.get('sale_count', 0))   # 销售数量
    if sale_count:
        data['sale_count'] = sale_count

    view_count = force_int(kwargs.get('view_count', 0))   # 浏览数量
    if view_count:
        data['view_count'] = view_count

    support_count = force_int(kwargs.get('support_count', 0))   # 支持数量
    if support_count:
        data['support_count'] = support_count

    try:
        data['last_grab_at'] = datetime.datetime.now()

        product = Product.objects(url=url).first()
        if not product:
            product = Product(**data)
            ok = product.save()
            if not ok:
                return {'success':False, 'message':'保存失败!'}
        else:
            data['inc__grab_count'] = 1 # 自增
            ok = product.update(**data)
            if not ok:
                return {'success':False, 'message':'更新失败!'}

    except(Exception) as e:
        return {'success':False, 'message':str(e)}
    
    return {'success':True, 'message':'success!', 'data':''}
