from . import main

from flask import render_template, jsonify, url_for, request, redirect, flash, current_app
from ...forms.user import SigninForm, SignupForm, ForgetPasswordForm, ResetPasswordForm
from ...helpers.auth import login_user, logout_user
from ...models.user import User
from ...helpers.email import send_mail

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


# 忘记密码
@main.route('/auth/forget_password',methods=['GET','POST'])
def forget_password():
    form=ForgetPasswordForm()
    if request.method == 'POST':
        if form.validate_on_submit():
            user=User.objects(email=request.form['email']).first()
            if user:
                token=user.generate_token()
                send_mail(user.email,'重置你的密码','auth/email/reset_password',user=user,token=token)
                tips = '重置密码邮件已发送至您的邮箱,请稍后查看.'
                flash(tips, 'success')
                return jsonify(success=True,message=tips, redirect_to=url_for('main.login'))
            else:
                tips = '请填写你注册时所用的邮箱地址!'
                return jsonify(success=False, message=tips)
    return render_template('auth/forget_password.html',form=form)


# 重置密码
@main.route('/auth/reset_password/<token>',methods=['POST','GET'])
def reset_password(token):
    form = ResetPasswordForm()
    if request.method == 'POST':
        if form.validate_on_submit():
            if User.reset_password(token, form.confirm_password.data):
                tips = '密码重置成功,请使用新密码进行登陆!'
                flash(tips, 'success')
                return jsonify(success=True, message=tips, redirect_to=url_for('main.login'))
            else:
                tips = '密码重置失败,请稍后重试!'
                return jsonify(success=False, message=tips)
    return render_template('auth/reset_password.html',form=form,token=token)
