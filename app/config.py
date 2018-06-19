import os
import configparser
from .env import cf
basedir = os.path.abspath(os.path.dirname(__file__))

class Config:
    SECRET_KEY = cf.get('base', 'secret_key')
    SQLALCHEMY_COMMIT_ON_TEARDOWN = True
    FLASKY_MAIL_SUBJECT_PREFIX = ''
    FLASKY_MAIL_SENDER = '' 
    FLASKY_ADMIN = os.environ.get('FLASKY_ADMIN')
    PROJECT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
    CONFDIR = os.path.join(PROJECT_DIR, 'etc')

    CELERY_IMPORTS = ('app.jobs.base.job', )
    CELERY_BROKER_URL = cf.get('redis', 'url')
    CELERY_RESULT_BACKEND = cf.get('redis', 'url')


    @staticmethod
    def init_app(app): 
        pass

class DevelopmentConfig(Config): 
    DEBUG = True
    MAIL_SERVER = 'smtp.googlemail.com'
    MAIL_PORT = 587
    MAIL_USE_TLS = True
    MAIL_USERNAME = cf.get('mail', 'username')
    MAIL_PASSWORD = cf.get('mail', 'password')

    # MongoDB配置
    MONGODB_SETTINGS = {
        'db': cf.get('mongo', 'db'),
        'host': cf.get('mongo', 'host'), 
        'port': cf.getint('mongo', 'port'),
        'username': cf.get('mongo', 'username'),
        'password': cf.get('mongo', 'password'),
        'authentication_source': cf.get('mongo', 'authentication_source')
    }

    #Redis 配置
    REDIS_URL = cf.get('redis', 'url')

    WTF_CSRF_ENABLED = False
    SECRET_KEY = cf.get('base', 'secret_key')
    WTF_CSRF_SECRET_KEY = cf.get('base', 'wtf_csrf_secret')

    PASSWORD_SECRET = cf.get('base', 'password_secret')

    D3INGO_URL = cf.get('api', 'd3ingo_url')


class TestingConfig(Config): 
    DEBUG = True
    TESTING = True
    # MongoDB配置
    MONGODB_SETTINGS = {
        'db': cf.get('mongo', 'db'),
        'host': cf.get('mongo', 'host'), 
        'port': cf.getint('mongo', 'port'),
        'username': cf.get('mongo', 'username'),
        'password': cf.get('mongo', 'password'),
        'authentication_source': cf.get('mongo', 'authentication_source')
    }

    #Redis 配置
    REDIS_URL = cf.get('redis', 'url')

    WTF_CSRF_ENABLED = False
    SECRET_KEY = cf.get('base', 'secret_key')
    WTF_CSRF_SECRET_KEY = cf.get('base', 'wtf_csrf_secret')

    PASSWORD_SECRET = cf.get('base', 'password_secret')

    D3INGO_URL = cf.get('api', 'd3ingo_url')

class ProductionConfig(Config):
    DEBUG = False
    # MongoDB配置
    MONGODB_SETTINGS = {
        'db': cf.get('mongo', 'db'),
        'host': cf.get('mongo', 'host'), 
        'port': cf.getint('mongo', 'port'),
        'username': cf.get('mongo', 'username'),
        'password': cf.get('mongo', 'password'),
        'authentication_source': cf.get('mongo', 'authentication_source')
    }

    #Redis 配置
    REDIS_URL = cf.get('redis', 'url')

    WTF_CSRF_ENABLED = False
    SECRET_KEY = cf.get('base', 'secret_key')
    WTF_CSRF_SECRET_KEY = cf.get('base', 'wtf_csrf_secret')

    D3INGO_URL = cf.get('api', 'd3ingo_url')

    PASSWORD_SECRET = cf.get('base', 'password_secret')

config = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'production': ProductionConfig,
    'default': DevelopmentConfig
}
