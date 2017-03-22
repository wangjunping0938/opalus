# -*- coding:utf-8 -*-
# 过滤器


# 时间
def format_datatime(value, format='%Y-%m-%d %H:%M'):
    return value.strftime(format)
