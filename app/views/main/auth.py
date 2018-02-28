from . import main

from flask import render_template, jsonify, url_for, request, redirect, flash, current_app
from ...forms.user import SigninForm, SignupForm
from ...helpers import login_user, logout_user

## 登录
@main.route('/auth/login', methods=['POST', 'GET'])
def login():

    form = SigninForm()
    if request.method == 'POST':

        if form.validate_on_submit():
            login_user(form.user)
            return jsonify(success=True, message='OK', redirect_to=url_for('main.index'))
        else:
            return jsonify(success=False, message=str(form.errors))

        next_url = request.args.get('next', '/')
        #account = request.form['account']
        #password = request.form['password']

        return jsonify(success=False, message='创建失败!')

    return render_template('auth/login.html', form=form)


## 注册
@main.route('/auth/register', methods=['POST', 'GET'])
def register():
    form = SignupForm()
    if request.method == 'POST':
        if form.validate_on_submit():
            user = form.save();
            if user:
                login_user(user)
                flash('注册成功!', 'success')
                return jsonify(success=True, message='注册成功!', redirect_to=url_for('main.index'))
            else:
                return jsonify(success=False, message='注册失败!')
        else:
            return jsonify(success=False, message=str(form.errors))

    return render_template('auth/register.html', form=form)

@main.route('/auth/logout')
def logout():
    logout_user()
    flash('退出成功!', 'success')
    return redirect(url_for('main.index'))
    

