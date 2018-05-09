# coding: utf-8

from flask import Blueprint
api = Blueprint('api', __name__, static_url_path='/static',
            static_folder='../../static')

from . import test, product, site, design_company, design_case, design_record

@api.before_request
def load_current_user():
    pass


class Base():
    def __init__(self):
        pass
        #self._obj = kwargs.get('obj', None)
        #super(BaseForm, self).__init__(*args, **kwargs)
