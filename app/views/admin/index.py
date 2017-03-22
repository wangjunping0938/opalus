from flask import render_template
from . import admin

@admin.route('/')
def index():
    meta = {
        'title': '控制台'
    }
    return render_template('admin/home/index.html', meta=meta)

@admin.route('/about')
def about():
    return render_template('admin/home/about.html', meta=meta)

