# coding: utf-8
from app.extensions import celery

# test
@celery.task()
def job(a, b):
    with open('/Users/tian/test.txt', 'a+') as f:
        f.write("Hello, world!\n")
    return a + b
