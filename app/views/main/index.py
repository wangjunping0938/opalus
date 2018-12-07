from flask import render_template, current_app, request, jsonify
from . import main
from app import cache
from app.helpers.block import get_column

metaInit = {
    'title': '首页',
    'css_nav_index': 'active',
}

@main.route('/')
def index():
    meta = metaInit.copy()
    meta['index_home_slide'] = get_column('index_home_slide', 10)
    meta['web_home_right_slide'] = get_column('web_home_right_slide', 2)
    return render_template('home/index.html', meta=meta)

@main.route('/about')
def about():
    meta = metaInit.copy()
    return render_template('home/about.html', meta=meta)


@main.route('/contact')
def contact():
    meta = metaInit.copy()
    return render_template('home/contact.html', meta=meta)


@main.route('/test')
def test():
    meta = metaInit.copy()
    a = 'abc'
    cache.set('aa', a)
    b = cache.get('aa')
    # job.delay(1, 2)
    # c = current_app.config['TEST']
    return str(c)



