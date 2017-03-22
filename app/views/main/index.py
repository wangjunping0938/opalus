from flask import render_template
from . import main 

@main.route('/')
def index():
    return render_template('home/index.html')

@main.route('/about')
def about():
    return render_template('home/about.html')

@main.route('/contact')
def contact():
    return render_template('home/contact.html')

