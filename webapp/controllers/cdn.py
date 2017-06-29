# -*- coding: utf-8 -*-
# @Author: liuli
# @Date:   2017-03-15 23:28:39
# @Last Modified by:   liuli
# @Last Modified time: 2017-06-28 23:10:54
from os import path
import datetime
from sqlalchemy import func
from flask import (render_template,
                   Blueprint,
                   redirect,
                   url_for,
                   abort)
from flask_login import login_required, current_user
from flask_principal import Permission, UserNeed

from webapp.models import db
from webapp.forms import CommentForm, PostForm
cdn_blueprint = Blueprint(
    'cdn',
    __name__,
    template_folder=path.join(path.pardir,'templates','cdn'),
    url_prefix="/cdn"
    )

@cdn_blueprint.route('/')
def home():
    return render_template('custom.html')

@cdn_blueprint.route('/logout')
def logout():
    return  redirect(url_for('main.login'))

@cdn_blueprint.route('/custom/')
def custom():
    return render_template('custom.html')


@cdn_blueprint.route('/dashboard/')
def dashboard():
    return render_template('dashboard.html')

@cdn_blueprint.route('/tables/')
def tables():
    return render_template('tables.html')

@cdn_blueprint.route('/post/<int:post_id>', methods=('GET', 'POST'))
def post(post_id):
    form = CommentForm()
    if form.validate_on_submit():
        new_comment = Comment()
        new_comment.name = form.name.data
        new_comment.text = form.text.data
        new_comment.post_id = post_id
        new_comment.date = datetime.datetime.now()

        db.session.add(new_comment)
        db.session.commit()

    post = Post.query.get_or_404(post_id)
    tags = post.tags
    comments = post.comments.order_by(Comment.date.desc()).all()
    recent, top_tags = sidebar_data()

    return render_template(
        'post.html',
        post=post,
        tags=tags,
        comments=comments,
        recent=recent,
        top_tags=top_tags,
        form=form
    )

@cdn_blueprint.route('/new', methods=['GET', 'POST'])
@login_required
def new_post():
    form = PostForm()
    print current_user

    if form.validate_on_submit():
        new_post = Post(form.title.data)
        new_post.text = form.text.data
        new_post.publish_date = datetime.datetime.now()
        new_post.user = User.query.filter_by(
            username=current_user.username
        ).one()

        db.session.add(new_post)
        db.session.commit()


    return render_template('new.html', form=form)


@cdn_blueprint.route('/edit/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_post(id):
    post = Post.query.get_or_404(id)

    permission = Permission(UserNeed(post.user.id))
    print permission.can()

    # We want admins to be able to edit any post
    if permission.can() or admin_permission.can():
        form = PostForm()

        if form.validate_on_submit():
            post.title = form.title.data
            post.text = form.text.data
            post.publish_date = datetime.datetime.now()

            db.session.add(post)
            db.session.commit()

            return redirect(url_for('.post', post_id=post.id))

        form.text.data = post.text

        return render_template('edit.html', form=form, post=post)

    abort(403)

