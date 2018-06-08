# -*- coding:utf-8 -*-
import time
from flask import current_app, g

## 权限验证
def check_role(role):
    if g.user.role_id == 8:
        return True
    if role == 8:
        return False
    if g.user.role_id == 5:
        return True
    if role == 5:
        return False
    if g.user.role_id == 2:
        return True
    if role == 2:
        return False
    return True
