# -*- coding: utf-8 -*-
# @Author: liuli
# @Date:   2017-03-18 22:39:53
# @Last Modified by:   liuli
# @Last Modified time: 2017-06-27 23:16:58

from flask.ext.login import LoginManager


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
    return redirect(url_for('blog.home'))


