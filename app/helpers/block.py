# -*- coding:utf-8 -*-
from app.models.block import Block
from app.models.column import Column
from app.models.column_zone import ColumnZone
import time
from flask import current_app

# 获取配置信息
def get_block_content(mark, type=1): 
    content = ''
    if not mark:
        return content
    try : 
        query = {
            'mark': mark,
            'status': 1
        }
        item = Block.objects(**query).first()
        if not item:
            return content

        if type == 1:
            content = item.code
        else:
            content = item.content

        return content
    except(Exception) as e:
        return content


# 获取栏目信息
def get_column(mark, size=10, desc=False): 
    if not mark:
        return None
    try : 
        zone = ColumnZone.objects(name=mark, status=1, deleted=0).first()
        if not zone:
            return None

        query = {
            'column_zone_id': str(zone._id),
            'status': 1,
            'deleted': 0,
        }
        if desc:
            sortF = "-sort"
        else:
            sortF = "sort"
        items = Column.objects(**query).order_by(sortF)[:size]

        # 过滤数据
        rows = []
        for i, d in enumerate(items):
            row = {
                '_id': str(d._id),
                'title': d.title,
                'sub_title': d.sub_title,
                'cover': d.cover(),
                'target': d.target,
            }
            rows.append(row)

        return rows
    except(Exception) as e:
        return None

