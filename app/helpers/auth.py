# coding: utf-8

import functools
from flask import g, request, session, redirect, url_for, flash

def get_current_user():

    from ..models.user import User 
    if 'uid' in session and 'token' in session:
        user = User.objects(_id=int(session['uid'])).first()
        if not user:
            return None
        if user.token != session['token']:
            return None
        return user
    return None


def login_user(user, permanent=False):
    if not user:
        return None
    session['uid'] = user.id
    session['token'] = user.token
    if permanent:
        session.permanent = True
    return user


def logout_user():
    if 'uid' not in session:
        return
    session.pop('uid')
    session.pop('token')

class require_role(object):
    def __init__(self, role):
        self.role = role

    def __call__(self, method):
        @functools.wraps(method)
        def wrapper(*args, **kwargs):
            if not g.user:
                url = url_for('main.login')
                flash('请先登录!', 'warn')
                return redirect(url)
            if self.role is None:
                return method(*args, **kwargs)
            if self.role == 'user':
                return method(*args, **kwargs)

            if self.role == 'staff':
                if g.user.role_id in [2,3,4,5,6,7,8,9]:
                    return method(*args, **kwargs)
                else:
                    flash('没有权限', 'warn')
                    return redirect(url_for('main.index'))
            if self.role == 'admin':
                if g.user.role_id in [5,9]:
                    return method(*args, **kwargs)
                else:
                    flash('没有权限.', 'warn')
                    return redirect(url_for('main.index'))

        return wrapper


require_user = require_role('user')
require_staff = require_role('staff')
require_admin = require_role('admin')
