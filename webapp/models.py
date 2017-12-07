# -*- coding: utf-8 -*-
# @Author: liuli
# @Date:   2017-03-15 23:27:56
# @Last Modified by:   XUEQUN
# @Last Modified time: 2017-09-06 16:32:03
import sys
reload(sys)
sys.setdefaultencoding('utf-8')
from flask_sqlalchemy import SQLAlchemy
from flask_login import AnonymousUserMixin
from flask import current_app
from webapp.extensions import bcrypt
from sqlalchemy import func
import datetime
from itsdangerous import (
    TimedJSONWebSignatureSerializer as Serializer,
    BadSignature,
    SignatureExpired
)

db = SQLAlchemy()

#1、用户和项目为多对多关系，一个用户可以管理多个项目，一个项目可以有多个使用人
#2、项目和域名为1对多关系，一个项目有多个域名

#用户和项目1对多关系
users = db.Table(
    'user_projects',
    db.Column('user_id', db.Integer, db.ForeignKey('user.id')),
    db.Column('project_id', db.Integer, db.ForeignKey('project.id'))
)

#用户和角色为1对多的关系，一个用户可能多个角色(admin、supper、default)
roles = db.Table(
    'role_users',
    db.Column('user_id', db.Integer, db.ForeignKey('user.id')),
    db.Column('role_id', db.Integer, db.ForeignKey('role.id'))
)


#项目表。字段为：项目ID、项目名称、域名列表、用户列表
class Project(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    project_name = db.Column(db.String(255))
    remark = db.Column(db.String(255))
    domains = db.relationship('Domain', backref='project', lazy='dynamic')
    users = db.relationship(
        'User',
        secondary=users,
        backref=db.backref('projects', lazy='dynamic')
)
#域名表。域名ID、所属CDN厂商、开始使用日期、结束日期、状态、用途，对应的项目ID
class Domain(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    domain_name =  db.Column(db.String(255))
    cname =  db.Column(db.String(255))
    start_date = db.Column(db.DateTime(),default=datetime.datetime.now)
    end_date = db.Column(db.DateTime(),default=datetime.datetime.now)
    status = db.Column(db.Integer())
    purpose = db.Column(db.String(255))
    project_id = db.Column(db.Integer(), db.ForeignKey('project.id'))


    #def __init__(self, cname):
   #     self.cname = cname

    #def __repr__(self):
    #    return "<cname u'{0}'>".format(self.cname)

#用户表。用户ID、用户名、密码、状态、邮件、电话
class User(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    username = db.Column(db.String(255))
    password = db.Column(db.String(255))
    status = db.Column(db.Integer())
    email = db.Column(db.String(255))
    tel = db.Column(db.String(255))
    roles = db.relationship(
        'Role',
        secondary=roles,
        backref=db.backref('users', lazy='dynamic')
    )


    def __init__(self,username):
        self.username = username
        #self.password = self.set_password(password)

    #def __repr__(self):
    #    return '<User u{0}>'.format(self.password)
    def is_authenticated(self):
        if isinstance(self, AnonymousUserMixin):
            return False
        else:
            return True

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

class Role(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(80), unique=True)
    description = db.Column(db.String(255))

    def __init__(self, name):
        self.name = name

    def __repr__(self):
        return '<Role {0}>'.format(self.name)


#计费信息表。计费ID、计费厂商、计费区域、简称、计费类型、计费价格
class Charge_info(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    charge_cname = db.Column(db.String(255))
    charge_area = db.Column(db.String(255))
    nick_name = db.Column(db.String(255))
    charge_type = db.Column(db.String(255))
    charge_price = db.Column(db.Float())


    #def __init__(self, charge_cname):
     #   self.charge_cname = charge_cname

    #def __repr__(self):
    #    return "<charge_cname '{0}'>".format(self.charge_cname)


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

    @staticmethod
    def get_charge_statics(charge_date,charge_cname):
        project_client_wangsu = ['剑一','剑二','剑三','剑世','月影','猎魔','春秋','封神一','反恐行动','自由禁区','麻辣江湖']
        project_client_fastweb = ['剑一','剑三','剑世','月影','反恐行动']

        project_legend_wangsu = []
        project_legend_fastweb = []
        status_data_fastweb = []
        status_data_wangsu = []

        project_legend_client_wangsu = []
        project_legend_phone_wangsu = []
        status_data_wangsu_phone = []
        status_data_wangsu_client = []

        charge_statics = db.session.query(Charge_statics.charge_date.label('charge_date'),Charge_statics.charge_cname.label('charge_cname'),Charge_statics.charge_project.label('charge_project'),func.sum(Charge_statics.charge_total)).filter_by(charge_date=charge_date).filter_by(charge_cname=charge_cname).group_by(Charge_statics.charge_project).all()

        if charge_cname == '快网':
            for f in charge_statics:
                for j in project_client_fastweb:
                    if f[2] == j:
                        project_legend_fastweb.append(f[2])
                        status_data_fastweb.append(f[3])
            return project_legend_fastweb,status_data_fastweb

        elif charge_cname == '网宿':
            #网宿5月所有项目的数据列表
            for p in charge_statics:
                if p[3]==0:continue
                project_legend_wangsu.append(p[2])
                status_data_wangsu.append(p[3])

            #网宿5月客户端和手机端各自项目和数据列表
            for k in charge_statics:
                for x in project_client_wangsu:
                    if k[2] == x:
                        project_legend_client_wangsu.append(k[2])
                        status_data_wangsu_client.append(k[3])
                if k[2] in project_client_wangsu:
                    continue
                else:
                    project_legend_phone_wangsu.append(k[2])
                    status_data_wangsu_phone.append(k[3])
            return project_legend_wangsu,status_data_wangsu,project_legend_client_wangsu,status_data_wangsu_client,project_legend_phone_wangsu,status_data_wangsu_phone

