# coding: utf-8

from wtforms import TextAreaField, StringField, IntegerField, PasswordField, FormField
from wtforms.validators import DataRequired, Length, EqualTo, NumberRange, Email
from flask_wtf import FlaskForm, RecaptchaField
from flask import current_app

#from .base import BaseForm
from ..models.user import User
#from ..helpers import *

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

# 用户基础信息
class ProfileForm(FlaskForm):
    realname = StringField('真实姓名')
    address = StringField('地址')
    sex = IntegerField('姓别')
    position = StringField('职位')

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
            if user.status == 1:
                raise ValueError('账号未通过审核!')
            if user.status == 0:
                raise ValueError('账号已禁用!')

            # 通过
            if user.status == 5:
                self.user = user
                return user
        raise ValueError('账号或密码不正确!')


class SignupForm(FlaskForm):
    account = StringField('用户名', validators=[DataRequired(message="账户不能为空"), Length(min=4, max=30, message="长度大于4小于30")])
    password = PasswordField('密码', validators=[DataRequired(), Length(min=6, max=20, message="长度大于6小于20")])
    password_confirm = PasswordField('确认密码', validators=[DataRequired(message="确认密码"), EqualTo('password', message='密码不一致')])
    phone=StringField("电话",validators=[DataRequired(),Length(max=20)])
    email=StringField('邮箱',validators=[DataRequired(),Length(max=30,message="长度小于30")])
    #profile = FormField(ProfileForm)
    #profile_realname = StringField('真实姓名',validators=[DataRequired(message="姓名不能为空!"),Length(max=30,message="姓名长度不要超过15个汉字!")])

    def validate_account(self, field):
        account = self.account.data
        phone=self.phone.data
        email=self.email.data
        data = field.data.lower()
        if data in RESERVED_WORDS:
            raise ValueError('不允许使用此用户名')
        if User.objects(account=account).first():
            raise ValueError('账号已存在')
        if User.objects(phone=phone).first():
            raise ValueError("该手机号已被注册!")
        if User.objects(email=email).first():
            raise ValueError('该email已存在!')

    def save(self, **param):
        data = self.data;
        current_app.logger.debug(data)
        data.pop('password_confirm')
        user = User(**data)
        user.save()
        return user

class SaveForm(FlaskForm):
    #account = StringField('用户名', validators=[DataRequired(message="账户不能为空"), Length(min=4, max=16, message="长度大于4小于16")])
    id = IntegerField('ID', validators=[DataRequired(message="ID不能为空")])
    phone = StringField('手机', validators=[Length(max=20, message="手机格式不正确")])
    email = StringField('邮箱', validators=[Length(max=30, message="邮箱格式不正确")])
    role_id = IntegerField('权限', validators=[NumberRange(min=1, max=8, message="权限设置不正确")])
    status = IntegerField('状态', validators=[NumberRange(min=0, max=5, message="状态设置不正确")])
    profile = FormField(ProfileForm)
    # 个人信息
    profile_realname = StringField('真实姓名')
    profile_address = StringField('地址')
    profile_sex = IntegerField('姓别')
    profile_position = StringField('职位')


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
        data['phone'] = self.data['phone']
        data['email'] = self.data['email']

        profile_data = {}
        if self.data['profile_realname']:
            profile_data['realname'] = self.data['profile_realname']
        if self.data['profile_address']:
            profile_data['address'] = self.data['profile_address']
        if self.data['profile_sex']:
            profile_data['sex'] = self.data['profile_sex']
        if self.data['profile_position']:
            profile_data['position'] = self.data['profile_position']

        data['profile'] = profile_data

        ok = user.update(**data)
        return ok

    def save(self):
        data = self.data;
        user = User(**data)
        user.save()
        return user

