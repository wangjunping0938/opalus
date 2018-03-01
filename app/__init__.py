#encoding: utf-8
from flask import Flask
from .config import config
import os
from flask_mongoengine import MongoEngine, MongoEngineSessionInterface
from flask_wtf.csrf import CSRFProtect
from jinja2 import filters
# 加载装饰器
from .helpers.filters import format_datatime

db = MongoEngine()
csrf = CSRFProtect()

def create_app(config_name):
    app = Flask(__name__,
            static_url_path = '/_static',
            static_folder = config[config_name].PROJECT_DIR + '/static',
            template_folder = 'templates')

    app.config.from_object(config[config_name]) #  这里config.py是文件
    config[config_name].init_app(app)

    db.init_app(app)
    csrf.init_app(app)
    #app.session_interface = MongoEngineSessionInterface(db)

    from .views import main
    app.register_blueprint(main, url_prefix='')
    from .views import admin
    app.register_blueprint(admin, url_prefix='/admin')
    from .views import api
    app.register_blueprint(api, url_prefix='/api')

    # 加载装饰器
    app.jinja_env.filters['date'] = format_datatime

    return app

