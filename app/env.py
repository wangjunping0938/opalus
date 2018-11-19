import configparser
import os
basedir = os.path.abspath(os.path.dirname(__file__))

cf = configparser.ConfigParser()
cf.read(os.path.abspath(os.path.join(basedir, '..', '.env_example')))
