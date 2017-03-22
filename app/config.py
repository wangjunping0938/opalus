import os
basedir = os.path.abspath(os.path.dirname(__file__))

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'tian' 
    SQLALCHEMY_COMMIT_ON_TEARDOWN = True
    FLASKY_MAIL_SUBJECT_PREFIX = ''
    FLASKY_MAIL_SENDER = '' 
    FLASKY_ADMIN = os.environ.get('FLASKY_ADMIN')
    PROJECT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
    CONFDIR = os.path.join(PROJECT_DIR, 'etc')

    @staticmethod
    def init_app(app): 
        pass

class DevelopmentConfig(Config): 
    DEBUG = True
    MAIL_SERVER = 'smtp.googlemail.com'
    MAIL_PORT = 587
    MAIL_USE_TLS = True
    MAIL_USERNAME = os.environ.get('MAIL_USERNAME')
    MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD') 

    # MongoDB配置
    MONGODB_SETTINGS = {
        'db': 'opalus',
        'host': '127.0.0.1', 
        'port': 27017,
        'username':'root',
        'password':''
    }

    CSRF_ENABLED = True
    SECRET_KEY = 'opalus'
    WTF_CSRF_SECRET_KEY = 'opalus'

    PASSWORD_SECRET = 'opalus'


class TestingConfig(Config): 
    TESTING = True
    # MongoDB配置
    MONGODB_SETTINGS = {
        'db': 'opalus',
        'host': '127.0.0.1', 
        'port': 27017,
        'username':'root',
        'password':''
    }

    CSRF_ENABLED = True
    SECRET_KEY = 'opalus'
    WTF_CSRF_SECRET_KEY = 'opalus'

    PASSWORD_SECRET = 'opalus'

class ProductionConfig(Config):
    # MongoDB配置
    MONGODB_SETTINGS = {
        'db': 'opalus',
        'host': '127.0.0.1', 
        'port': 27017,
        'username':'root',
        'password':''
    }

    CSRF_ENABLED = True
    SECRET_KEY = 'opalus'
    WTF_CSRF_SECRET_KEY = 'opalus'

    PASSWORD_SECRET = 'opalus'

config = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'production': ProductionConfig,
    'default': DevelopmentConfig
}
