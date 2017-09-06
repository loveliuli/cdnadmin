# -*- coding: utf-8 -*-
# @Author: liuli
# @Date:   2017-04-05 22:14:45
# @Last Modified by:   XUEQUN
# @Last Modified time: 2017-08-08 21:41:23
from flask import abort, current_app
from flask_restful import Resource

from webapp.models import User
from webapp.controllers.rest.parsers import user_post_parser

from itsdangerous import TimedJSONWebSignatureSerializer as Serializer


class AuthApi(Resource):
    def post(self):
        args = user_post_parser.parse_args()
        user = User.query.filter_by(username=args['username']).one()

        if user.check_password(args['password']):
            s = Serializer(current_app.config['SECRET_KEY'], expires_in=604800)
            return {"token": s.dumps({'id': user.id})}
        else:
            abort(401)
