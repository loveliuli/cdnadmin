# -*- coding: utf-8 -*-
# @Author: liuli
# @Date:   2017-03-15 23:27:56
# @Last Modified by:   XUEQUN
# @Last Modified time: 2017-06-29 17:24:50
#表单工具

from flask_wtf import FlaskForm, RecaptchaField
from wtforms import StringField, TextAreaField, PasswordField, BooleanField
from wtforms.validators import DataRequired, Length, EqualTo, URL

from webapp.models import User

class CommentForm(FlaskForm):
    name = StringField(
        'Name',
        validators=[DataRequired(), Length(max=255)]
    )
    text = TextAreaField(u'Comment', validators=[DataRequired()])

class LoginForm(FlaskForm):
    username = StringField('Username', [DataRequired(), Length(max=255)])
    password = PasswordField('Password', [DataRequired()])
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
    username = StringField('Username', [DataRequired(), Length(max=255)])
    password = PasswordField('Password', [DataRequired(), Length(min=8)])
    confirm = PasswordField('Confirm Password', [
        DataRequired(),
        EqualTo('password')
    ])
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