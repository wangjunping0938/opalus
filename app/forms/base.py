# coding: utf-8

from flask_wtf import FlaskForm

class BaseForm(FlaskForm):
    def __init__(self, *args, **kwargs):
        self._obj = kwargs.get('obj', None)
        super(BaseForm, self).__init__(*args, **kwargs)
