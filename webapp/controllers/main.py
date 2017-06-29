# -*- coding: utf-8 -*-
# @Author: XUEQUN
# @Date:   2017-03-17 11:16:27
# @Last Modified by:   XUEQUN
# @Last Modified time: 2017-06-29 17:30:00

from flask import (render_template,
                   current_app,
                   Blueprint,
                   redirect,
                   url_for,
                   request,
                   flash,
                   session)
from flask_principal import (
    Identity,
    AnonymousIdentity,
    identity_changed
)
from webapp.forms import LoginForm, RegisterForm
from os import path
from webapp.models import User,db
from flask_login import login_user, logout_user

main_blueprint = Blueprint(
    'main',
    __name__,
    template_folder=path.join(path.pardir,'templates','main'),
    )
@main_blueprint.route('/')
def index():
    return redirect(url_for('main.login'))

@main_blueprint.route('/login', methods=['GET', 'POST'])
#@oid.loginhandler
def login():
    form = LoginForm()
    #openid_form = OpenIDForm()

    # if openid_form.validate_on_submit():
    #     return oid.try_login(
    #         openid_form.openid.data,
    #         ask_for=['nickname', 'email'],
    #         ask_for_optional=['fullname']
    #     )

    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).one()
        login_user(user, remember=form.remember.data)

        identity_changed.send(
            current_app._get_current_object(),
            identity=Identity(user.id)
        )

        #flash("You have been logged in.", category="success")
        return redirect(url_for('cdn.home'))

    # openid_errors = oid.fetch_error()
    # if openid_errors:
    #     flash(openid_errors, category="danger")

    #return render_template('login.html', form=form, openid_form=openid_form)
    return render_template('login.html', form=form)


@main_blueprint.route('/logout', methods=['GET', 'POST'])
def logout():
    logout_user()

    identity_changed.send(
        current_app._get_current_object(),
        identity=AnonymousIdentity()
    )

    flash(u"成功退出!", category="success")
    return redirect(url_for('.login'))


@main_blueprint.route('/register', methods=['GET', 'POST'])
#@oid.loginhandler
def register():
    form = RegisterForm()
    # openid_form = OpenIDForm()

    # if openid_form.validate_on_submit():
    #     return oid.try_login(
    #         openid_form.openid.data,
    #         ask_for=['nickname', 'email'],
    #         ask_for_optional=['fullname']
    #     )

    if form.validate_on_submit():
        new_user = User(form.username.data)
        new_user.set_password(form.password.data)

        db.session.add(new_user)
        db.session.commit()

        flash(u"用户创建成功，请登陆.", category="success")

        return redirect(url_for('.login'))

    # openid_errors = oid.fetch_error()
    # if openid_errors:
    #     flash(openid_errors, category="danger")

    #return render_template('register.html', form=form, openid_form=openid_form)
    return render_template('register.html', form=form)

