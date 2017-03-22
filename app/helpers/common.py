# -*- coding:utf-8 -*-

import time
import base64
# 加密
import hashlib

def force_int(value, default=0):
    try:
        return int(value)
    except:
        return default

def force_float_2(value, default=0):
    try:
        return "%.2f" % value
    except:
        return default

# md5
def gen_md5(str):
    m = hashlib.md5()
    m.update(str.encode('utf8'))
    return m.hexdigest()

# sha1
def gen_sha1(str):
    m = hashlib.sha1()
    m.update(str.encode('utf8'))
    return m.hexdigest()
