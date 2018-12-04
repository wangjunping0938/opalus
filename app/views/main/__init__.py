# coding: utf-8

from flask import Blueprint, g
main = Blueprint('main', __name__, static_url_path='/static',
            static_folder='../../static', template_folder='../../templates/main')

from app import csrf
from . import index, auth, upload, image, asset
from app.helpers.auth import get_current_user

@main.before_request
def load_current_user():
    g.user = get_current_user()
    if g.user:
        g.is_admin = True if g.user.role_id in [5, 8] else False
        g.is_system = True if g.user.role_id in [8] else False

## 开启csrf验证
@main.before_request
def check_csrf():
    csrf.protect()

class Base():
    def __init__(self):
        pass
        #self._obj = kwargs.get('obj', None)
        #super(BaseForm, self).__init__(*args, **kwargs)
