from ensurepip import bootstrap
from pstats import Stats
from QLHocSinh import *
from flask_admin import Admin
from QLHocSinh.models import MonHoc, VaiTro, CauHinhLopHoc
from flask_admin.contrib.sqla import ModelView
from flask_login import current_user, logout_user
from flask_admin import BaseView,expose,AdminIndexView
from flask import redirect, url_for, flash
import utils
from QLHocSinh import db


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

    #Xử lý khi thay đổi môn học
    def on_model_change(self, form, model, is_created):

        if is_created:
            flash(f'Môn học "{model.TenMonHoc}" đã được tạo mới thành công!', 'success')
        else:
            flash(f'Môn học "{model.TenMonHoc}" đã được thay đổi thành công!', 'success')


    #Thông báo khi xóa xong
    def after_model_delete(self, model):
        flash(f'Môn học "{model.TenMonHoc}" đã bị xóa thành công!', 'danger')

class MyAdminIndexView(AdminIndexView):
    @expose('/')
    def index(self):
        return self.render('admin/index.html', stats=utils)


class StatsView(BaseView):
    @expose('/')
    def index(self):
        return self.render('admin/stats.html', stats=utils.tinh_so_hs_diem_TB_lon_hon_5(1,2,1))

    def is_accessible(self):
        return current_user.is_authenticated and current_user.LoaiTaiKhoan.__eq__(VaiTro.ADMIN)


class Regulations(AuthenticatedModelView):
    column_labels = {
        'SiSoToiDa': 'Sĩ số tối đa',
        'DoTuoiToiThieu': 'Độ tuổi tối thiểu',
        'DoTuoiToiDa':'Độ tuổi tối đa',
        'NgayCapNhat':'Ngày cập nhật'
    }
    can_delete = False
    can_create = False

admin = Admin(app, name ="Administration", template_mode = 'bootstrap4', index_view=MyAdminIndexView())
admin.add_view(MonHoc_Details(MonHoc, db.session,name ="Môn Học"))
admin.add_view(StatsView(name="Thống kê môn học"))
admin.add_view(Regulations(CauHinhLopHoc,db.session,name="Quy Định"))
admin.add_view(LogoutView(name='Đăng Xuất'))




