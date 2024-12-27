from ensurepip import bootstrap
from pstats import Stats
from urllib import request

from QLHocSinh import *
from flask_admin import Admin
from QLHocSinh.models import MonHoc, VaiTro, CauHinhLopHoc, NamHoc, Lop
from flask_admin.contrib.sqla import ModelView
from flask_login import current_user, logout_user
from flask_admin import BaseView,expose,AdminIndexView
from flask import redirect, url_for, flash, jsonify
import utils
from QLHocSinh import db
from flask import request

from QLHocSinh.utils import layhockys


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
        return self.render('admin/index.html', VaiTro=VaiTro)


from flask import session

from flask import session, request, jsonify, redirect, url_for

class StatsView(BaseView):
    @expose('/',methods=["GET","POST"])
    def index(self):
        # Lấy danh sách các năm học và môn học
        ds_nam_hoc = db.session.query(NamHoc).all()
        ds_mon = db.session.query(MonHoc).all()
        hockys=[]

        # Lấy các tham số từ session (nếu có)
        selected_year = session.get('selected_year')
        selected_subject = session.get('selected_subject')
        selected_hocky = session.get('selected_hocky')

        if request.method == 'POST':
            if 'filter_hocky' in request.form:
                selected_year = request.form['nam_hoc']
                session['selected_year'] = selected_year

                selected_subject = request.form['mon']
                session['selected_subject'] = selected_subject

                hockys = layhockys(selected_year)

            if 'thongke' in request.form:

                selected_hocky = request.form['hocky']
                session['selected_hocky'] = selected_hocky

        stats = utils.dem_hocsinh_tutrungbinh_theolop(1,1,1)
        if selected_year and selected_subject and selected_hocky:
            stats = utils.dem_hocsinh_tutrungbinh_theolop(selected_year, selected_hocky, selected_subject)

        # Trả về template với các tham số
        return self.render('admin/stats.html',
                           stats=stats,
                           years=ds_nam_hoc,
                           subjects=ds_mon,
                           hockys=hockys,
                           selected_year=selected_year,
                           selected_subject=selected_subject,
                           selected_hocky=selected_hocky)


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




