from flask import render_template, current_app, request
from . import main 
from app import redis_store
from app.jobs.base import job


@main.route('/')
def index():
    return render_template('home/index.html')

@main.route('/about')
def about():
    return render_template('home/about.html')

@main.route('/contact')
def contact():
    return render_template('home/contact.html')


@main.route('/test')
def test():
    a = 'abc'
    redis_store.set('aa', a)
    b = redis_store.get('aa')
    #job.delay(1, 2)
    #c = current_app.config['TEST']
    return str(c)

