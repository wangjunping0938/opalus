# coding: utf-8
from flask import Blueprint, g
from flask import redirect, url_for, flash

admin = Blueprint('admin', __name__, static_url_path='/static',
            static_folder='../../../static', template_folder='app/templates/admin')

from app import csrf
from . import index, user, block, category, site, product, order, growth, article, design_company, design_case, design_conf, design_record, company_queue, brand, image, asset, tag, column,column_zone
from app.helpers.auth import get_current_user

@admin.before_request
def load_current_user():
    g.user = get_current_user()
    if g.user:
        g.is_edit = True if g.user.role_id in [2, 5, 8] else False
        g.is_admin = True if g.user.role_id in [5, 8] else False
        g.is_system = True if g.user.role_id in [8] else False

        if not g.is_edit:
            flash('没有权限!', 'warning')
            return redirect(url_for('main.index'))

    else:
        flash('请先登录!', 'warning')
        return redirect(url_for('main.login'))


## 开启csrf验证
@admin.before_request
def check_csrf():
    csrf.protect()


class Base():
    def __init__(self):
        pass
