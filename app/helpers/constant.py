# -*- coding:utf-8 -*-

# 获取所含站点信息
def platform_options(id=0):
    data = [
                {'id':0, 'name': '--', 'type': 0},
                {'id':1, 'name': '京东众筹', 'type': 2},
                {'id':2, 'name': '淘宝众筹', 'type': 2},
                {'id':3, 'name': '米家', 'type': 2},
                {'id':4, 'name': '一条', 'type': 1},
                {'id':5, 'name': '二更', 'type': 1},
                {'id':6, 'name': '差评', 'type': 1},
                {'id':7, 'name': '其它', 'type': 0}
            ]

    if id==0:
        return data
    else:
        for d in data:
            if d['id']==id:
                return d
    return {'id': 0, 'name': ''}

# 获取网站模式
def platform_type(id=0):
    if id==1:
        return '正常销售'
    elif id==2:
        return '众筹'
    elif id==3:
        return '-'
    else:
        return '--'

# 企业规模
def company_scale_options(id=0):
    data = [
                {'id':0, 'name': '--'},
                {'id':1, 'name': '20人以下'},
                {'id':2, 'name': '20-50人'},
                {'id':3, 'name': '50-100人'},
                {'id':4, 'name': '100-300人'},
                {'id':5, 'name': '300人以上'},
                {'id':6, 'name': '其它'},
            ]

    if id==0:
        return data
    else:
        for d in data:
            if d['id']==id:
                return d
    return {'id': 0, 'name': ''}

# 企业性质
def company_nature_options(id=0):
    data = [
                {'id':0, 'name': '--'},
                {'id':1, 'name': '私企'},
                {'id':2, 'name': '国企'},
                {'id':3, 'name': '事业单位'},
                {'id':4, 'name': '外企'},
                {'id':5, 'name': '合资企业'},
                {'id':6, 'name': '其它'},
            ]

    if id==0:
        return data
    else:
        for d in data:
            if d['id']==id:
                return d
    return {'id': 0, 'name': ''}


# 企业注册资金
def company_registered_capital_format_options(id=0):
    data = [
                {'id':0, 'name': '--'},
                {'id':1, 'name': '1~100万'},
                {'id':2, 'name': '101~500万'},
                {'id':3, 'name': '501~1000万'},
                {'id':4, 'name': '1001~5000万'},
                {'id':5, 'name': '5000万以上'},
            ]

    if id==0:
        return data
    else:
        for d in data:
            if d['id']==id:
                return d
    return {'id': 0, 'name': ''}
