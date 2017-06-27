from flask import Flask

def create_app(object_name):
    app = Flask(__name__)
    app.config.from_object(object_name)

    db.init_app(app)

    return app

if __name__ == '__main__':
    app = create_app('project.config.ProdConfig')
    app.run()
