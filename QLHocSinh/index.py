
from QLHocSinh import app
from flask import render_template, request, url_for, redirect, session
from QLHocSinh.admin import *
from QLHocSinh import utils,login
from flask_login import login_user, logout_user
from QLHocSinh.models import *
from QLHocSinh.utils import laythongtinnhanvien, laylopcuagiaovien, laymonhoccuagiaovientheolop, laynamhoccuagiaovien, \
    layhocky, laydanhsachhocsinh, laydanhsachdiemhocsinh


@app.route('/')
def welcome():
    return render_template('index.html')


@app.route('/home')
def home():
    userif = laythongtinnhanvien(current_user.MaTaiKhoan,current_user.LoaiTaiKhoan)

    return render_template('home.html',VaiTro=VaiTro,userif=userif)

@login.user_loader
def user_load(userid):
    return utils.get_user_by_id(userid)

@app.route('/login', methods=['GET', 'POST'])
def login():
    msg=''
    if request.method.__eq__('POST'):
        username = request.form['username']
        password = request.form['password']
        user = utils.check_login(username, password)
        if user:
            login_user(user)
            if(user.LoaiTaiKhoan==VaiTro.STAFF or user.LoaiTaiKhoan==VaiTro.TEACHER):
             return redirect(url_for('home'))
            else:
                return redirect(url_for('admin.index'))
        else:
            msg="Tai khoan hoac mat khau khong dung"

    return render_template('login.html', msg=msg)

@app.route('/logout')
def signout():
    logout_user()
    return redirect(url_for('login'))

@app.route('/admin-login', methods=['POST'])
def login_admin():
    username = request.form['username']
    password = request.form['password']
    user = utils.check_login(username, password , role=VaiTro.ADMIN)
    if user:
        login_user(user)
        return redirect(url_for('admin.index'))


@app.route('/nhapdiem', methods=["GET", "POST"])
def nhapdiem():
    userif = laythongtinnhanvien(current_user.MaTaiKhoan, current_user.LoaiTaiKhoan)
    lop = laylopcuagiaovien(userif.MaNhanVien)

    mondangday = session.get('mondangday', [])
    namdangday = session.get('namdangday', [])
    hocky = session.get('hocky', [])

    danhsachhocsinh = []

    #loc du lieu
    malopdachon=session.get('malopdachon')
    namdachon=session.get('namdachon')
    mondachon=session.get('mondachon')
    hockydachon=session.get('hockydachon')

    if request.method == 'POST':
        if 'filter_class' in request.form:  # Xử lý lọc lớp
            malopdaloc = request.form.get('malopdaloc')
            session['malopdachon'] = malopdaloc  # Lưu lớp vào session
            malopdachon = session['malopdachon']

            mondangday = laymonhoccuagiaovientheolop(userif.MaNhanVien, malopdaloc)
            namdangday = laynamhoccuagiaovien(userif.MaNhanVien, malopdaloc)
            hocky = layhocky(userif.MaNhanVien, malopdaloc)

            #lưu vào session khi nào cần thì dùng
            session['mondangday'] = [{"MaMonHoc": mon.MaMonHoc, "TenMonHoc": mon.TenMonHoc} for mon in mondangday]
            session['namdangday'] = [{"MaNamHoc": nam.MaNamHoc, "TenNamHoc": nam.TenNamHoc} for nam in namdangday]
            session['hocky'] = [{"MaHocKy": hk.MaHocKy, "TenHocKy": hk.TenHocKy} for hk in hocky]

        elif 'filter_details' in request.form:  # Xử lý lọc chi tiết
            #lay nam
            manamhoc = request.form.get('namhoc')
            session['namdachon']=manamhoc
            namdachon=session['namdachon']

            #lay mon
            mamonhoc = request.form.get('monhoc')
            session['mondachon']=mamonhoc
            mondachon=session['mondachon']

            #lay hoc ki
            mahocky=request.form.get('hocky')
            session['hockydachon']=mahocky
            hockydachon=session['hockydachon']

            print(namdachon)
            print(mondachon)
            print(hockydachon)

            danhsachhocsinh = laydanhsachdiemhocsinh(malopdachon, namdachon)

            for hocsinh in danhsachhocsinh:
                # lay diem 15p
                diem15p = Diem15p.query.filter_by(
                    MaHocSinh = hocsinh.MaHocSinh,
                    MaHocKy = hockydachon,
                    MaMonHoc = mondachon,
                    MaNamHoc = namdachon
                ).all()
                hocsinh.diem15p_list=diem15p

                # lay diem 1 tiet
                diem1tiet = Diem1Tiet.query.filter_by(
                    MaHocSinh=hocsinh.MaHocSinh,
                    MaHocKy=hockydachon,
                    MaMonHoc=mondachon,
                    MaNamHoc=namdachon
                ).all()
                hocsinh.diem1tiet_list = diem1tiet

                # lay diem hoc ky
                diemhocky = DiemHocKy.query.filter_by(
                    MaHocSinh=hocsinh.MaHocSinh,
                    MaHocKy=hockydachon,
                    MaMonHoc=mondachon,
                    MaNamHoc=namdachon
                ).all()
                hocsinh.diemhocky_list = diemhocky


            print(danhsachhocsinh)

    return render_template('nhapdiem.html',
                           userif=userif, VaiTro=VaiTro, lop=lop,
                           malopdachon=malopdachon,  # Truyền lớp đã chọn vào template
                           mondangday=mondangday,
                           namdangday=namdangday,
                           hocky=hocky,
                           danhsachhocsinh=danhsachhocsinh,
                           namdachon=namdachon,
                           hockydachon=hockydachon,
                           mondachon=mondachon,
                           )


@app.route('/test2')
def test2():
    userif = laythongtinnhanvien(current_user.MaTaiKhoan, current_user.LoaiTaiKhoan)
    return render_template('test2.html',userif=userif,VaiTro=VaiTro)

if __name__ == '__main__':
    app.run(debug=True)