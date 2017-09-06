# -*- coding: utf-8 -*-
# @Author: liuli
# @Date:   2017-04-05 17:59:00
# @Last Modified by:   XUEQUN
# @Last Modified time: 2017-08-11 21:25:02
#获取url中的参数

from flask_restful import reqparse

#user的POST方法可带参数，用于生产token
user_post_parser = reqparse.RequestParser()
user_post_parser.add_argument('username', type=str, required=True)
user_post_parser.add_argument('password', type=str, required=True)

#project的GET方法可带参数.指定页数、用户、项目名获取项目相关的信息
project_get_parser = reqparse.RequestParser()
project_get_parser.add_argument('page', type=int, location=['args', 'headers'])
project_get_parser.add_argument('user', type=str, location=['args', 'headers'])
project_get_parser.add_argument('project_name', type=str, location=['args', 'headers'])

#project的POST方法可带-d参数，可传入项目名称、用户、域名，project_name和token是必须的。
project_post_parser = reqparse.RequestParser()
project_post_parser.add_argument(
    'token',
    type=str,
    required=True,
    help="Auth Token is required to edit posts"
)
project_post_parser.add_argument(
    'project_name',
    type=str,
    required=True,
    help="Project_name is required"
)

project_post_parser.add_argument(
    'users',
    type=str,
    action='append'
)

project_post_parser.add_argument(
    'domains',
    type=str,
    action='append'
)

#project的PUT方法可带-d参数，可传入项目名称、用户、域名，project_name和token是必须的。
project_put_parser = reqparse.RequestParser()
project_put_parser.add_argument(
    'token',
    type=str,
    required=True,
    help="Auth Token is required to create posts"
)
project_put_parser.add_argument(
    'project_name',
    type=str,
    required=True,
    help="Project_name is required"
)
project_put_parser.add_argument(
    'users',
    type=str
)
project_put_parser.add_argument(
    'domains',
    type=str
)

#project的DELETE方法可带-d参数，token是必须的。
project_delete_parser = reqparse.RequestParser()
project_delete_parser.add_argument(
    'token',
    type=str,
    required=True,
    help="Auth Token is required to delete posts"
)


domain_get_parser = reqparse.RequestParser()
domain_get_parser.add_argument('page', type=int, location=['args', 'headers'])
domain_get_parser.add_argument('domain_id', type=int, location=['args', 'headers'])

domain_post_parser = reqparse.RequestParser()
domain_post_parser.add_argument(
    'token',
    type=str,
    required=True,
    help="Auth Token is required to create posts"
)
domain_post_parser.add_argument(
    'cname',
    type=str
)
domain_post_parser.add_argument(
    'domain_name',
    type=str
)


domain_put_parser = reqparse.RequestParser()
domain_put_parser.add_argument(
    'token',
    type=str,
    required=True,
    help="Auth Token is required to create posts"
)
domain_put_parser.add_argument(
    'cname',
    type=str
)
domain_put_parser.add_argument(
    'domain_name',
    type=str
)

domain_delete_parser = reqparse.RequestParser()
domain_delete_parser.add_argument(
    'token',
    type=str,
    required=True,
    help="Auth Token is required to delete posts"
)

