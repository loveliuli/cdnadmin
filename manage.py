import os
from flask_script import Manager, Server
from flask_script.commands import ShowUrls,Clean
from flask_migrate import Migrate, MigrateCommand

from webapp import create_app
from webapp.models import db, User,Role,Project, Domain, Charge_info, Charge_statics

# default to dev config
env = os.environ.get('WEBAPP_ENV', 'dev')
app = create_app('webapp.config.%sConfig' % env.capitalize())

migrate = Migrate(app, db)

manager = Manager(app)
manager.add_command("server", Server())
manager.add_command("show-urls", ShowUrls())
manager.add_command('db', MigrateCommand)
manager.add_command('clean',Clean())

@manager.shell
def make_shell_context():
    return dict(
        app=app,
        db=db,
        User=User,
        Role=Role,
        Domain=Domain,
        Project=Project,
        Charge_info=Charge_info,
        Charge_statics=Charge_statics
    )

if __name__ == "__main__":
    manager.run()
