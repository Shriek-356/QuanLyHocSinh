from ensurepip import bootstrap
from pstats import Stats

from QLHocSinh import app,db
from flask_admin import Admin
from QLHocSinh.models import MonHoc, VaiTro
from flask_admin.contrib.sqla import ModelView
from flask_login import current_user, logout_user
from flask_admin import BaseView,expose,AdminIndexView
from flask import redirect, url_for
import utils

class AuthenticatedModelView(ModelView):
    def is_accessible(self):
        return current_user.is_authenticated and current_user.LoaiTaiKhoan.__eq__(VaiTro.ADMIN)

class LogoutView(BaseView):
    @expose('/')
    def index(self):
        logout_user()
        return redirect(url_for('admin.index'))
    def is_accessible(self):
        return current_user.is_authenticated

class MonHoc_Details(AuthenticatedModelView):
    column_labels = {
        'TenMonHoc':'Tên Môn Học',
        'ThoiLuongHoc': 'Thời lượng môn học (phút)',
    }
    column_searchable_list = ['TenMonHoc']

class MyAdminIndexView(AdminIndexView):
    @expose('/')
    def index(self):
        return self.render('admin/index.html', stats=utils)

class StatsView(BaseView):
    @expose('/')
    def index(self):
        return self.render('admin/stats.html', stats=utils.tinh_diem_TB())

    def is_accessible(self):
        return current_user.is_authenticated and current_user.LoaiTaiKhoan.__eq__(VaiTro.ADMIN)

admin = Admin(app, name ="Administration", template_mode = 'bootstrap4', index_view=MyAdminIndexView())
admin.add_view(MonHoc_Details(MonHoc, db.session))
admin.add_view(StatsView(name="Thống kê môn học"))
admin.add_view(LogoutView(name='Đăng Xuất'))




