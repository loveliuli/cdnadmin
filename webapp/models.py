# -*- coding: utf-8 -*-
# @Author: liuli
# @Date:   2017-03-15 23:27:56
# @Last Modified by:   liuli
# @Last Modified time: 2017-06-27 23:54:44
from flask.ext.sqlalchemy import SQLAlchemy
from flask.ext.login import AnonymousUserMixin
from flask import current_app

db = SQLAlchemy()

class User(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    username = db.Column(db.String(255))
    password = db.Column(db.String(255))
    status = db.Column(db.Integer())
    project = db.Column(db.String(255))
    email = db.Column(db.String(255))
    tel = db.Column(db.String(255))
    domains = db.relationship('Domains', backref='user', lazy='dynamic')

    def __init__(self, username):
        self.username = username

    def __repr__(self):
        return '<User {0}>'.format(self.username)

    #将密码字段进行加密
    def set_password(self,password):
        self.password = bcrypt.generate_password_hash(password)

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


class Domain(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    project = db.Column(db.String(255))
    cname =  db.Column(db.String(255))
    start_date = db.Column(db.DateTime())
    end_date = db.Column(db.DateTime())
    status = db.Column(db.Integer())
    purpose = db.Column(db.String(255))
    user_id = db.Column(db.Integer(), db.ForeignKey('user.id'))


    def __init__(self, cname):
        self.cname = cname

    def __repr__(self):
        return "<cname '{0}'>".format(self.cname)


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

