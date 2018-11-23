from flask import render_template, current_app, request, jsonify
from . import main

from app.jobs.image import download, upload
from . import main
from app import redis_store

metaInit = {
    'title': '素材库',
    'css_nav_image': 'active',
}

@main.route('/image')
def image_index():
    meta = metaInit.copy()
    return render_template('image/index.html', meta=meta)

@main.route('/imagea')
def image_opera():
    download.delay()
    upload.delay()
    return jsonify(code=200, message='')

