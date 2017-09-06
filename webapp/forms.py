# -*- coding: utf-8 -*-
# @Author: liuli
# @Date:   2017-03-15 23:27:56
# @Last Modified by:   XUEQUN
# @Last Modified time: 2017-08-29 10:24:53
#表单工具

from flask_wtf import FlaskForm, RecaptchaField
from wtforms import StringField, TextAreaField, PasswordField, BooleanField,TextField,IntegerField,SubmitField
from wtforms.validators import DataRequired, Length, EqualTo, URL,Email,NumberRange

from webapp.models import User

class CommentForm(FlaskForm):
    name = StringField(
        'Name',
        validators=[DataRequired(), Length(max=255)]
    )
    text = TextAreaField(u'Comment', validators=[DataRequired()])

class LoginForm(FlaskForm):
    username = StringField(u'用户名', validators=[DataRequired(), Length(max=255, message=u'填写用户名')])
    password = PasswordField(u'密码',validators=[DataRequired(), Length(max=255, message=u'填写密码')])
    verification_code = StringField(u'验证码', validators=[DataRequired(), Length(4, 4, message=u'填写4位验证码')])
    remember = BooleanField("Remember Me")

    def validate(self):
        check_validate = super(LoginForm, self).validate()

        # if our validators do not pass
        if not check_validate:
            return False

        # Does our the exist
        user = User.query.filter_by(username=self.username.data).first()
        if not user:
            self.username.errors.append(u'用户名或密码错误！')
            return False

        # Do the passwords match
        if not user.check_password(self.password.data):
            self.username.errors.append(u'用户名或密码错误！')
            return False

        return True

class PostForm(FlaskForm):
    title = StringField('Title', [DataRequired(), Length(max=255)])
    text = TextAreaField('Content', [DataRequired()])

class RegisterForm(FlaskForm):
    username = StringField(u'用户名', validators=[DataRequired(), Length(max=255, message=u'填写用户名')])
    email = TextField(u'邮箱',validators=[DataRequired(), Length(max=255, message=u'填写邮箱地址')])
    tel = IntegerField(u'手机号', validators=[DataRequired(), Length(min=13,message=u'填写手机号'),NumberRange(min=10000000000, max=20000000000)])
    password = PasswordField(u'密码', validators=[DataRequired(), Length(min=255, message=u'填写密码')])
    confirm = PasswordField(u'确认密码', validators=[DataRequired(),EqualTo('password')])
    submit = SubmitField('注册')

    #recaptcha = RecaptchaField()

    def validate(self):
        check_validate = super(RegisterForm, self).validate()

        # if our validators do not pass
        if not check_validate:
            return False

        user = User.query.filter_by(username=self.username.data).first()

        # Is the username already being used
        if user:
            self.username.errors.append(u"用户名已存在！")
            return False

        return True
