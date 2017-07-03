# -*- coding: utf-8 -*-
# @Author: liuli
# @Date:   2017-03-15 23:28:39
# @Last Modified by:   XUEQUN
# @Last Modified time: 2017-07-01 17:49:20
import os
from os import path
import datetime,json
from sqlalchemy import func
from flask import (render_template,
                   Blueprint,
                   redirect,
                   url_for,
                   abort,
                   flash,
                   request)
from flask_login import login_required, current_user
from flask_principal import Permission, UserNeed

from webapp.models import db,User,Project,Charge_info
from webapp.forms import CommentForm, PostForm
cdn_blueprint = Blueprint(
    'cdn',
    __name__,
    template_folder=path.join(path.pardir,'templates','cdn'),
    url_prefix="/cdn"
    )

def get_current_user():
    try:
        cur_user = current_user.username
    except Exception as e:
        flash(u"请先登录!")
        return  redirect(url_for('main.login'))
    else:
        user = User.query.filter_by(
        username=cur_user
    ).one()
        return user

@cdn_blueprint.route('/')
def home():
    cur_user = get_current_user()
    return render_template('dashboard.html',login_user=cur_user.username)

@cdn_blueprint.route('/logout/')
def logout():
    return  redirect(url_for('main.logout'))

@cdn_blueprint.route('/custom/')
def custom():
    cur_user = get_current_user()
    return render_template('custom.html',login_user=cur_user.username)


@cdn_blueprint.route('/dashboard/')
def dashboard():
    cur_user = get_current_user()
    return render_template('dashboard.html',login_user=cur_user.username)

@cdn_blueprint.route('/tables/')
def tables():
    cur_user = get_current_user()
    os.chdir('/usr/local/src/myproject/cdnadmin/webapp/utils')
    with open('fastwebstaticsresult.txt') as f:
        rt=f.readlines()
        _rt_statics,total_money = eval(rt[0])
    return render_template('table.html',login_user=cur_user.username,statics=_rt_statics)

@cdn_blueprint.route('/domainadmin/')
def domainadmin():
    cur_user = get_current_user()
    return render_template('domainadmin.html',login_user=cur_user.username)

@cdn_blueprint.route('/projectamdin/')
def projectadmin():
    cur_user = get_current_user()
    projects = Project.query.all()
    return render_template('projectadmin.html',login_user=cur_user.username,projects=projects)

@cdn_blueprint.route('/priceinfo/')
def priceinfo():
    cur_user = get_current_user()
    prices = Charge_info.query.all()
    return render_template('priceinfo.html',login_user=cur_user.username,prices=prices)

def check_projectname(projectname):
    if len(projectname)<30:
        return (True,u'添加项目成功!')
'''
新建项目
'''
@cdn_blueprint.route('/project/add/', methods=['POST'])          #将url path=/user/add的post请求交由add_user处理
def add_project():
    projectname = request.form.get('projectname', '')
       #检查用户信息
    _is_ok, _error = check_projectname(projectname)

    if _is_ok:
        new_project = Project()
        new_project.project_name = projectname
        db.session.add(new_project)
        db.session.commit()
    return json.dumps({'is_ok':_is_ok, "error":_error})

'''
修改项目
'''
@cdn_blueprint.route('/project/update/', methods=['POST'])          #将url path=/user/add的post请求交由add_user处理
def update_project():
    projectid = request.form.get('id', '')
    #获取表单上的项目名称projectname
    projectname = request.form.get('projectname','')
    pro = Project.query.filter_by(id=projectid).one()
    #从数据库查询原始项目名称new_projectname
    new_projectname = pro.project_name
    check_projectname_isexists = Project.query.filter_by(project_name=projectname).all()
    #如果查询当前填入的项目名称存在数据库当中，且修改了项目名称，则提示项目名称已经存在。
    if check_projectname_isexists and not projectname == new_projectname :
        return json.dumps({'is_ok':False, "error":'修改的项目名已存在，操作失败!'})
    if projectname == new_projectname:
        return json.dumps({'is_ok':False, "error":'项目名称没有变化!'})
    else:
        Project.query.filter_by(id=projectid).update({'project_name':projectname})
        db.session.commit()
        return json.dumps({'is_ok':True, "error":'修改成功!'})

@cdn_blueprint.route('/project/delete/', methods=['GET'])
def delete_project():
    pid = request.args.get('id')
    pro = Project.query.filter_by(id=pid).first()
    print pro
    db.session.delete(pro)
    db.session.commit()
    flash('删除项目成功!',category='success')
    return redirect(url_for('cdn.projectadmin'))


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

