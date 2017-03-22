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
