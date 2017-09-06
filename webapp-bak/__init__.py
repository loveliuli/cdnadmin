import os
from flask import Flask
from webapp.models import db
from controllers.cdn import cdn_blueprint
from controllers.main import main_blueprint
from webapp.extensions import bcrypt,login_manager,admin
from webapp.models import User,Project,Domain,Charge_info,Charge_statics
from webapp.controllers.admin import (
        CustomView,
        CustomModelView,
        CustomFileAdmin

    )

def datetimeformat(value, format="%Y-%m"):
    return value.strftime(format)

def create_app(object_name):
    app = Flask(__name__)
    app.config.from_object(object_name)

    db.init_app(app)
    bcrypt.init_app(app)
    admin.init_app(app)
    login_manager.init_app(app)

    admin.add_view(CustomView(name='Custom'))

    models = [User,Project,Domain,Charge_info,Charge_statics]
    for model in models:
        admin.add_view(
            CustomModelView(
                model,db.session,category='models'
                )
            )
    admin.add_view(
        CustomFileAdmin(
            os.path.join(os.path.dirname(__file__), 'static'),
            '/static/',
            name='Static Files'
        )
    )



    app.register_blueprint(cdn_blueprint)
    app.register_blueprint(main_blueprint)

    app.jinja_env.filters['datetimeformat'] = datetimeformat

    return app

if __name__ == '__main__':
    app = create_app('project.config.ProdConfig')
    app.run()
