from flask import Flask
from webapp.models import db
from controllers.cdn import cdn_blueprint
from controllers.main import main_blueprint
from webapp.extensions import bcrypt,login_manager

def create_app(object_name):
    app = Flask(__name__)
    app.config.from_object(object_name)

    db.init_app(app)
    bcrypt.init_app(app)
    login_manager.init_app(app)
    app.register_blueprint(cdn_blueprint)
    app.register_blueprint(main_blueprint)

    return app

if __name__ == '__main__':
    app = create_app('project.config.ProdConfig')
    app.run()
