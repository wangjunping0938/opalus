# coding: utf-8
from . import create_app

def job1(a):
  app = create_app("development")
  app_ctx = app.app_context()
  app_ctx.push()
  print('aaaaaa')
