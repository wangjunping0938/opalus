# -*- coding:utf-8 -*-
from app.models.block import Block
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

        if (type == 1):
            content = item.code
        else:
            content = item.content

        return content
    except(Exception) as e:
        return content
    else: 
        pass

