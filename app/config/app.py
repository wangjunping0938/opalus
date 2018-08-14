import os
import configparser
from app.env import cf


DEBUG = True if cf.getint('base', 'debug') == 1 else False

# 基础配置
SECRET_KEY = cf.get('base', 'secret_key')
#SQLALCHEMY_COMMIT_ON_TEARDOWN = True
#FLASKY_MAIL_SUBJECT_PREFIX = ''
#FLASKY_MAIL_SENDER = '' 
#FLASKY_ADMIN = os.environ.get('FLASKY_ADMIN')
PROJECT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
CONFDIR = os.path.join(PROJECT_DIR, 'config')

# 队列
CELERY_IMPORTS = ('app.jobs.base.job', )
CELERY_BROKER_URL = cf.get('redis', 'url')
CELERY_RESULT_BACKEND = cf.get('redis', 'url')

# MongoDB配置
MONGODB_SETTINGS = {
    'db': cf.get('mongo', 'db'),
    'host': cf.get('mongo', 'host'), 
    'port': cf.getint('mongo', 'port'),
    'username': cf.get('mongo', 'username'),
    'password': cf.get('mongo', 'password'),
    'authentication_source': cf.get('mongo', 'authentication_source')
}

# 邮件系统
MAIL_SERVER = cf.get('mail','server')
MAIL_PORT = cf.get('mail','port')
MAIL_USE_TLS = True
MAIL_USERNAME = cf.get('mail', 'username')
MAIL_PASSWORD = cf.get('mail', 'password')
FLASKY_MAIL_SUBJECT_PREFIX='[Opalus-TaiHuoNiao]'
FLASKY_MAIL_SENDER=cf.get('mail','sender')
FLASKY_ADMIN=cf.get('mail','admin')

#Redis 配置
REDIS_URL = cf.get('redis', 'url')

WTF_CSRF_ENABLED = False
SECRET_KEY = cf.get('base', 'secret_key')
WTF_CSRF_SECRET_KEY = cf.get('base', 'wtf_csrf_secret')

D3INGO_URL = cf.get('api', 'd3ingo_url')

PASSWORD_SECRET = cf.get('base', 'password_secret')

