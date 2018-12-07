#encoding: utf-8
from flask import Flask
import datetime
import os
from flask_mongoengine import MongoEngine, MongoEngineSessionInterface
from flask_wtf.csrf import CSRFProtect
from jinja2 import filters
# redis
from flask_caching import Cache
# 定时任务
from .extensions import celery
# 加载装饰器
from .helpers.filters import format_datatime
from flask_mail import Mail

PROJDIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '.'))
CONFDIR = os.path.join(PROJDIR, 'config')

db = MongoEngine()
cache = Cache(config={'CACHE_TYPE': 'simple'})
csrf = CSRFProtect()
mail=Mail()


def create_app(config=None):
    app = Flask(__name__,
            static_url_path = '/_static',
            static_folder = os.path.join(PROJDIR, '../static'),
            template_folder = 'templates')

    app.config.from_pyfile(os.path.join(CONFDIR, 'app.py'))
    app.config.from_pyfile(os.path.join(CONFDIR, 'qiniu.py'))

    if isinstance(config, dict):
        app.config.update(config)
    elif config:
        app.config.from_pyfile(config)

    app.config.update({'SITE_TIME': datetime.datetime.utcnow()})

    db.init_app(app)
    cache.init_app(app)
    csrf.init_app(app)
    mail.init_app(app)
    #app.session_interface = MongoEngineSessionInterface(db)

    celery.init_app(app)

    from .views import main
    app.register_blueprint(main, url_prefix='')
    from .views import admin
    app.register_blueprint(admin, url_prefix='/admin')
    from .views import api
    app.register_blueprint(api, url_prefix='/api')

    # 加载装饰器
    app.jinja_env.filters['date'] = format_datatime

    return app

