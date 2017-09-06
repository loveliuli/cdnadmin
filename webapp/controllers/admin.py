from flask_admin import BaseView, expose
from flask_admin.contrib.sqla import ModelView
from flask_admin.contrib.fileadmin import FileAdmin
from flask_login import login_required, current_user

#from webapp.extensions import admin_permission
#from webapp.forms import CKTextAreaField


class CustomView(BaseView):
    @expose('/')
    @login_required
    #@admin_permission.require(http_exception=403)
    def index(self):
        return self.render('admin/custom.html')

    @expose('/second_page')
    @login_required
    #@admin_permission.require(http_exception=403)
    def second_page(self):
        return self.render('admin/second_page.html')


class CustomModelView(ModelView):
    def is_accessible(self):
        print current_user
        return current_user.is_authenticated()


class CustomFileAdmin(FileAdmin):
    def is_accessible(self):
        print current_user
        return current_user.is_authenticated()
