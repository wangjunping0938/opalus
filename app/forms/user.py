# coding: utf-8

from wtforms import TextAreaField, StringField, IntegerField, PasswordField
from wtforms.validators import DataRequired, Length, EqualTo, NumberRange
from flask_wtf import FlaskForm, RecaptchaField

#from .base import BaseForm
from ..models.user import User
from ..helpers import *

RESERVED_WORDS = [
    'root', 'admin', 'bot', 'robot', 'master', 'webmaster',
    'account', 'people', 'user', 'users', 'project', 'projects',
    'search', 'action', 'favorite', 'like', 'love', 'none',
    'team', 'teams', 'group', 'groups', 'organization',
    'organizations', 'package', 'packages', 'org', 'com', 'net',
    'help', 'doc', 'docs', 'document', 'documentation', 'blog',
    'bbs', 'forum', 'forums', 'static', 'assets', 'repository',

    'public', 'private',
    'mac', 'windows', 'ios', 'lab',
]


class SigninForm(FlaskForm):
    account = StringField('用户名', validators=[DataRequired(), Length(min=4, max=30, message="长度大于4小于30")],
            )
    password = PasswordField('密码', validators=[DataRequired()]
    )
    #permanent = BooleanField(_('Remember me for a month.'))

    def validate_password(self, field):
        account = self.account.data
        user = User.objects(account=account).first()

        if not user:
            raise ValueError('账号不存在!')
        if user.check_password(self.password.data, account):
            self.user = user
            return user
        raise ValueError('账号或密码不正确!')


class SignupForm(FlaskForm):
    account = StringField('用户名', validators=[DataRequired(message="账户不能为空"), Length(min=4, max=30, message="长度大于4小于30")])

    password = PasswordField('密码', validators=[DataRequired(), Length(min=6, max=20, message="长度大于6小于20")])
    password_confirm = PasswordField('确认密码', validators=[DataRequired(message="确认密码"), EqualTo('password', message='密码不一致')])

    def validate_account(self, field):
        account = self.account.data
        data = field.data.lower()
        if data in RESERVED_WORDS:
            raise ValueError('不允许使用此用户名')
        if User.objects(account=account).first():
            raise ValueError('账号已存在')

    def save(self):
        data = self.data;
        data.pop('password_confirm')
        #data.pop('csrf_token')
        user = User(**data)
        user.save()
        return user

class SaveForm(FlaskForm):
    #account = StringField('用户名', validators=[DataRequired(message="账户不能为空"), Length(min=4, max=16, message="长度大于4小于16")])
    id = IntegerField('ID', validators=[DataRequired(message="ID不能为空")])
    role_id = IntegerField('权限', validators=[NumberRange(min=1, max=8, message="权限设置不正确")])
    status = IntegerField('状态', validators=[NumberRange(min=0, max=5, message="状态设置不正确")])

    #csrf_token = StringField('auth', validators=[DataRequired(message="不能为空")])
    #password = PasswordField('密码', validators=[DataRequired(), Length(min=6, max=20, message="长度大于6小于20")])
    #password_confirm = PasswordField('确认密码', validators=[DataRequired(message="确认密码"), EqualTo('password', message='密码不一致')])

    def update_one(self):
        id = self.data['id']
        user = User.objects(_id=id).first()
        if not user:
            raise ValueError('用户不存在!')
        data = {}
        data['role_id'] = self.data['role_id']
        data['status'] = self.data['status']

        ok = user.update(**data)
        return ok

    def save(self):
        data = self.data;
        user = User(**data)
        user.save()
        return user
