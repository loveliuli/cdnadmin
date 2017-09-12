# -*- coding: utf-8 -*-
# @Author: liuli
# @Date:   2017-03-18 22:39:53
# @Last Modified by:   XUEQUN
# @Last Modified time: 2017-09-06 10:31:52
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_admin import Admin
from flask_restful import Api
from flask_principal import Principal, Permission, RoleNeed


bcrypt = Bcrypt()
admin = Admin()
rest_api = Api()
principals = Principal()


admin_permission = Permission(RoleNeed('admin'))
poster_permission = Permission(RoleNeed('poster'))
default_permission = Permission(RoleNeed('default'))

login_manager = LoginManager()
login_manager.login_view = "main.login"
login_manager.session_protection = "strong"
login_manager.login_message = "Please login to access this page"
login_manager.login_message_category = "info"



@login_manager.user_loader
def load_user(userid):
    from models import User
    return User.query.get(userid)


#@oid.after_login
def create_or_login(resp):
    from models import db, User
    username = resp.fullname or resp.nickname or resp.email

    if not username:
        flash('Invalid login. Please try again.', 'danger')
        return redirect(url_for('main.login'))

    user = User.query.filter_by(username=username).first()
    if user is None:
        user = User(username)
        db.session.add(user)
        db.session.commit()

    session['username'] = username
    return redirect(url_for('cdn.home'))


