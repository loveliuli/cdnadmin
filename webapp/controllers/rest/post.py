# -*- coding: utf-8 -*-
# @Author: liuli
# @Date:   2017-04-05 16:17:42
# @Last Modified by:   XUEQUN
# @Last Modified time: 2017-08-11 22:37:05
#所有API实现

import sys
reload(sys)
sys.setdefaultencoding('utf-8')
import datetime,json
from flask import abort
from flask_login import current_user
from flask_restful import Resource, fields, marshal_with
from webapp.controllers.rest.fields import HTMLField

from webapp.models import db, User, Project, Domain
from webapp.controllers.rest.parsers import (
    project_get_parser,
    project_post_parser,
    project_put_parser,
    project_delete_parser,
    domain_put_parser,
    domain_get_parser,
    domain_delete_parser,
    domain_post_parser
)

nested_user_fields = {
    'username': fields.String()
}

nested_domain_fields = {
    'domain_name': fields.String()
}

project_fields = {
    'id': fields.Integer(),
    'project_name': fields.String(),
    'users': fields.List(fields.Nested(nested_user_fields)),
    'domains': fields.List(fields.Nested(nested_domain_fields))
}

domain_fields = {
    'domain_name': fields.String(),
    'id': fields.Integer(),
    'cname': fields.String(),
    'start_date': fields.DateTime(dt_format='iso8601'),
    'end_date': fields.DateTime(dt_format='iso8601'),
    'purpose': fields.String(),
    'status': fields.Integer(),
}


class UserApi(Resource):
    pass
class DomainApi(Resource):
    @marshal_with(domain_fields)
    #获取域名信息，如果指定id，则返回指定id的域名，否则返回所有域名，分页显示。
    def get(self, domain_id=None):
        if domain_id:
            domain = Domain.query.get(domain_id)
            if not domain:
                abort(404)
            return domain
        else:
            args = domain_get_parser.parse_args()
            page = args['page'] or 1
            print 'args is %s' %(args)
            domains = Domain.query.order_by(Domain.id).paginate(page, 10)
            return domains.items

    def post(self,domain_id=None):
        if domain_id:
            abort(400)
        else:
            args = domain_post_parser.parse_args(strict=True)
            user = User.verify_auth_token(args['token'])
            domain_name = args['domain_name']
            domain = Domain.query.filter_by(domain_name=domain_name).all()
            if not user:
                abort(401)
            if domain:
                abort(401)
            else:
                new_domain = Domain()
                new_domain.domain_name = args['domain_name']
                new_domain.cname = args['cname']
                new_domain.purpose = ''
                new_domain.project_id = 61
                new_domain.end_date = datetime.datetime.now()+datetime.timedelta(1000)
                new_domain.start_date = datetime.datetime.now()-datetime.timedelta(1500)

            db.session.add(new_domain)
            db.session.commit()
            return new_domain.id, 201


    def put(self, domain_id=None):
        if not domain_id:
            abort(400)

        domain = Domain.query.get(domain_id)

        if not domain:
            abort(404)

        args = domain_put_parser.parse_args(strict=True)
        user = User.verify_auth_token(args['token'])
        if not user:
            abort(401)


        domain.cname = args['cname']
        domain.domain_name = args['domain_name']


        db.session.add(domain)
        db.session.commit()
        return domain.id, 201

    def delete(self, domain_id=None):
        if not domain_id:
            abort(400)

        domain = Domain.query.get(domain_id)
        if not domain:
            abort(404)

        args = domain_delete_parser.parse_args(strict=True)
        user = User.verify_auth_token(args['token'])

        db.session.delete(domain)
        db.session.commit()
        return "", 204

class ProjectApi(Resource):
    @marshal_with(project_fields)
    def get(self, project_id=None):
        if project_id:
            project = Project.query.get(project_id)
            if not project:
                abort(404)
            return project
        else:
            args = project_get_parser.parse_args()
            page = args['page'] or 1
            print 'args is %s page is %s' %(args,page)
            if args['user']:
                user = User.query.filter_by(username=args['user']).first()
                #如果user存在，就根据user查询；否则就通过page参数查询。
                if not user:
                    abort(404)
                #使用desc一般用于日期，取最新的数据
                projects = user.projects.order_by(Project.project_name.desc()).paginate(page, 10)
            elif args['project_name']:
                project = Project.query.filter_by(project_name=args['project_name']).first()
                if not project:
                    abort(404)
                return project
            else:
                projects = Project.query.order_by(Project.id).paginate(page, 10)

            return projects.items

    def post(self, project_id=None):
        if project_id:
            abort(400)
        else:
            args = project_post_parser.parse_args(strict=True)

            user = User.verify_auth_token(args['token'])
            if not user:
                abort(401)

            new_post = Project()
            new_post.project_name = args['project_name']

            if args['users']:
                print args['users']
                for item in args['users']:
                    user = User.query.filter_by(username=item).first()

                    # Add the tag if it exists. If not, make a new tag
                    if user:
                        new_post.users.append(user)
                    else:
                        new_user = User()
                        new_user.username = item
                        new_post.users.append(new_user)


            db.session.add(new_post)
            db.session.commit()
            return new_post.id, 201

    def put(self, project_id=None):
        #无指定修改id，则退出
        if not project_id:
            abort(400)
        #根据id没有查询到项目，则退出
        project = Project.query.get(project_id)
        if not project:
            abort(404)
        #用户验证不通过，退出
        args = project_post_parser.parse_args(strict=True)
        user = User.verify_auth_token(args['token'])
        if not user:
            abort(401)
        #if user not in project.users:
        #    abort(403)

        if args['project_name']:
            project.project_name = args['project_name']


        #如果有users参数，先判断是否已存在用户表中，再判断用户是否已经关联项目，若已关联，则忽略；若没关联，则添加用户
        if args['users']:
            flag = True
            print args['users']
            print type(args['users'])
            for item in args['users']:
                user = User.query.filter_by(username=item).first()
                #如果新增的用户不存在数据库当中，则退出。
                if not user:
                    flag=False
                    abort(400)

            #如果修改的用户已经在本项目中，则忽略；如果没在本项目中，则添加。(用户要求是已经存在。)
            if flag:
                for item in args['users']:
                    if item in project.users:
                        continue
                    else:
                        user = User.query.filter_by(username=item).first()
                        project.users.append(user)

        #如果有domains参数，先判断域名是否已经关联到了项目，若已关联，则忽略；若没关联，则添加域名。(域名不要求已存在的)
        if args['domains']:
            print args['domains']
            print type(args['domains'])
            for item in args['domains']:
                if item in  project.domains:
                    continue
                else:
                    new_domain = Domain()
                    new_domain.domain_name = item
                    new_domain.cname = ''
                    new_domain.status = 1
                    new_domain.purpose = ''
                    new_domain.end_date = datetime.datetime.now()+datetime.timedelta(1000)
                    new_domain.start_date = datetime.datetime.now()-datetime.timedelta(1500)
                    project.domains.append(new_domain)

        db.session.add(project)
        db.session.commit()
        return project.id, 201

    def delete(self, project_id=None):
        if not project_id:
            abort(400)

        project = Project.query.get(project_id)
        if not project:
            abort(404)

        args = project_delete_parser.parse_args(strict=True)
        user = User.verify_auth_token(args['token'])
        if user not in  project.users:
            abort(401)

        db.session.delete(project)
        db.session.commit()
        return "success", 204
