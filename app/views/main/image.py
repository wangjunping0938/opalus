from flask import jsonify

from app.jobs.image import download, upload
from . import main
from app import redis_store

@main.route('/image')
def image_opera():
    download.delay()
    upload.delay()
    return jsonify(code=200, message='')

