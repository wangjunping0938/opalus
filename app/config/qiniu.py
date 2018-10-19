import os
import configparser
from app.env import cf

QN_ACCESS_KEY = cf.get('qiniu', 'access_key')
QN_SECRET_KEY = cf.get('qiniu', 'secret_key')
QN_BUCKET_NAME = cf.get('qiniu', 'bucket_name')

