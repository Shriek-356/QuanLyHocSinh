from ensurepip import bootstrap
from QLHocSinh import app,db
from flask_admin import Admin
from QLHocSinh.models import MonHoc
from flask_admin.contrib.sqla import ModelView

admin = Admin(app, name ="Administration", template_mode = 'bootstrap4')

class MonHoc_Details(ModelView):
    column_labels = {
        'TenMonHoc':'Tên Môn Học',
        'ThoiLuongHoc': 'Thời lượng môn học (phút)',
    }
    column_searchable_list = ['TenMonHoc']

admin.add_view(MonHoc_Details(MonHoc, db.session))




