# -*- coding: utf-8 -*-
# @Author: liuli
# @Date:   2017-03-15 23:27:56
# @Last Modified by:   liuli
# @Last Modified time: 2017-06-28 19:22:06
from flask_sqlalchemy import SQLAlchemy
from flask_login import AnonymousUserMixin
from flask import current_app
from webapp.extensions import bcrypt

db = SQLAlchemy()

#1、用户和项目为多对多关系，一个用户可以管理多个项目，一个项目可以有多个使用人
#2、项目和域名为1对多关系，一个项目有多个域名

#用户和项目1对多关系
users = db.Table(
    'user_projects',
    db.Column('user_id', db.Integer, db.ForeignKey('user.id')),
    db.Column('project_id', db.Integer, db.ForeignKey('project.id'))
)

#项目表。字段为：项目ID、项目名称、域名列表、用户列表
class Project(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    project_name = db.Column(db.String(255))
    domains = db.relationship('Domain', backref='project', lazy='dynamic')
    users = db.relationship(
        'Project',
        secondary=users,
        backref=db.backref('projects', lazy='dynamic')
)
#域名表。域名ID、所属CDN厂商、开始使用日期、结束日期、状态、用途，对应的项目ID
class Domain(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    cname =  db.Column(db.String(255))
    start_date = db.Column(db.DateTime())
    end_date = db.Column(db.DateTime())
    status = db.Column(db.Integer())
    purpose = db.Column(db.String(255))
    project_id = db.Column(db.Integer(), db.ForeignKey('project.id'))


    def __init__(self, cname):
        self.cname = cname

    def __repr__(self):
        return "<cname '{0}'>".format(self.cname)

#用户表。用户ID、用户名、密码、状态、邮件、电话
class User(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    username = db.Column(db.String(255))
    password = db.Column(db.String(255))
    status = db.Column(db.Integer())
    email = db.Column(db.String(255))
    tel = db.Column(db.String(255))


    def __init__(self,username):
        self.username = username
        #self.password = self.set_password(password)

    def __repr__(self):
        return '<User {0}>'.format(self.password)

    #将密码字段进行加密
    def set_password(self,password):
        self.password =bcrypt.generate_password_hash(password)
        #return bcrypt.generate_password_hash(password) #初始化测试添加用户名和密码时使用。

    #检测当前对象的密码是否和传入的密码一致
    def check_password(self,password):
        return bcrypt.check_password_hash(self.password,password)

    def is_active(self):
        return True

    def get_id(self):
        return unicode(self.id)

    @staticmethod
    def verify_auth_token(token):
        s = Serializer(current_app.config['SECRET_KEY'])

        try:
            data = s.loads(token)
        except SignatureExpired:
            return None
        except BadSignature:
            return None

        user = User.query.get(data['id'])
        return user

#计费信息表。计费ID、计费厂商、计费区域、简称、计费类型、计费价格
class Charge_info(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    charge_cname = db.Column(db.String(255))
    charge_area = db.Column(db.String(255))
    nick_name = db.Column(db.String(255))
    charge_type = db.Column(db.String(255))
    charge_price = db.Column(db.Float())


    def __init__(self, charge_cname):
        self.charge_cname = charge_cname

    def __repr__(self):
        return "<charge_cname '{0}'>".format(self.charge_cname)

#计费统计表。计费ID、计费日期（2017-05）、计费厂商、计费类型、计费项目、计费区域、计费带宽、计费价格、费用、占比
class Charge_statics(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    charge_date =  db.Column(db.DateTime())
    charge_cname = db.Column(db.String(255))
    charge_type = db.Column(db.String(255))
    charge_project = db.Column(db.String(255))
    charge_area = db.Column(db.String(255))
    charge_traff = db.Column(db.Float())
    charge_price = db.Column(db.Float())
    charge_total = db.Column(db.Float())
    charge_percent = db.Column(db.Float())

