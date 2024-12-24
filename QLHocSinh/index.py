import math

from QLHocSinh import app
from flask import render_template, request, url_for, redirect, session
from QLHocSinh.admin import *
from QLHocSinh import utils,login
from flask_login import login_user, logout_user
from QLHocSinh.models import *
from QLHocSinh.utils import laythongtinnhanvien, laylopcuagiaovien, laymonhoccuagiaovientheolop, laynamhoccuagiaovien, \
    layhocky, laydanhsachhocsinh, laydanhsachdiemhocsinh, layhockys, laydiemtrungbinhhocky


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
    counter = 0
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

        elif 'update_scores' in request.form:

            # Lấy danh sách học sinh đã lọc

            danhsachhocsinh, counter = laydanhsachdiemhocsinh(malopdachon, namdachon)

            # Cập nhật điểm cho học sinh hoặc thêm mới nếu chưa có

            if danhsachhocsinh:

                for hocsinh in danhsachhocsinh:

                    # Cập nhật hoặc thêm mới điểm 15 phút

                    for i in range(5):

                        diem15p_value = request.form.get(f"diem15p_{hocsinh.MaHocSinh}_{i}")

                        if diem15p_value:

                            diem15p = Diem15p.query.filter_by(

                                MaHocSinh=hocsinh.MaHocSinh,

                                MaHocKy=hockydachon,

                                MaMonHoc=mondachon,

                                MaNamHoc=namdachon

                            ).all()

                            if len(diem15p) > i:  # Nếu điểm đã tồn tại, cập nhật

                                diem15p[i].SoDiem15p = diem15p_value

                            else:  # Nếu điểm chưa tồn tại, tạo mới

                                new_diem15p = Diem15p(

                                    MaHocSinh=hocsinh.MaHocSinh,

                                    MaHocKy=hockydachon,

                                    MaMonHoc=mondachon,

                                    MaNamHoc=namdachon,

                                    SoDiem15p=diem15p_value

                                )

                                db.session.add(new_diem15p)

                    # Cập nhật hoặc thêm mới điểm 1 tiết

                    for i in range(3):

                        diem1tiet_value = request.form.get(f"diem1tiet_{hocsinh.MaHocSinh}_{i}")

                        if diem1tiet_value:

                            diem1tiet = Diem1Tiet.query.filter_by(

                                MaHocSinh=hocsinh.MaHocSinh,

                                MaHocKy=hockydachon,

                                MaMonHoc=mondachon,

                                MaNamHoc=namdachon

                            ).all()

                            if len(diem1tiet) > i:  # Nếu điểm đã tồn tại, cập nhật

                                diem1tiet[i].SoDiem1Tiet = diem1tiet_value

                            else:  # Nếu điểm chưa tồn tại, tạo mới

                                new_diem1tiet = Diem1Tiet(

                                    MaHocSinh=hocsinh.MaHocSinh,

                                    MaHocKy=hockydachon,

                                    MaMonHoc=mondachon,

                                    MaNamHoc=namdachon,

                                    SoDiem1Tiet=diem1tiet_value

                                )

                                db.session.add(new_diem1tiet)

                    # Cập nhật hoặc thêm mới điểm học kỳ

                    diemhocky_value = request.form.get(f"diemhocky_{hocsinh.MaHocSinh}")

                    if diemhocky_value:

                        diemhocky = DiemHocKy.query.filter_by(

                            MaHocSinh=hocsinh.MaHocSinh,

                            MaHocKy=hockydachon,

                            MaMonHoc=mondachon,

                            MaNamHoc=namdachon

                        ).first()

                        if diemhocky:  # Nếu điểm học kỳ đã tồn tại, cập nhật

                            diemhocky.SoDiemHocKy = diemhocky_value

                        else:  # Nếu điểm học kỳ chưa tồn tại, tạo mới

                            new_diemhocky = DiemHocKy(

                                MaHocSinh=hocsinh.MaHocSinh,

                                MaHocKy=hockydachon,

                                MaMonHoc=mondachon,

                                MaNamHoc=namdachon,

                                SoDiemHocKy=diemhocky_value

                            )

                            db.session.add(new_diemhocky)

                # Commit sau khi thêm mới hoặc cập nhật xong tất cả điểm
                db.session.commit()
                # Sau khi cập nhật, chuyển hướng về lại trang nhập điểm
                # Cập nhật điểm cho học sinh
                for hocsinh in danhsachhocsinh:
                    diem15p = Diem15p.query.filter_by(MaHocSinh=hocsinh.MaHocSinh, MaHocKy=hockydachon,
                                                      MaMonHoc=mondachon,
                                                      MaNamHoc=namdachon).all()
                    hocsinh.diem15p_list = diem15p

                    diem1tiet = Diem1Tiet.query.filter_by(MaHocSinh=hocsinh.MaHocSinh, MaHocKy=hockydachon,
                                                          MaMonHoc=mondachon, MaNamHoc=namdachon).all()
                    hocsinh.diem1tiet_list = diem1tiet

                    diemhocky = DiemHocKy.query.filter_by(MaHocSinh=hocsinh.MaHocSinh, MaHocKy=hockydachon,
                                                          MaMonHoc=mondachon, MaNamHoc=namdachon).all()
                    hocsinh.diemhocky_list = diemhocky

    page = request.args.get('page', 1, type=int)
    page_size = app.config['PAGE_SIZE']

    danhsachhocsinh,counter = laydanhsachdiemhocsinh(malopdachon, namdachon)

    start = (page - 1) * page_size
    end = start + page_size
    danhsachhocsinh_paginated = danhsachhocsinh[start:end]

    for hocsinh in danhsachhocsinh:
        # lay diem 15p
        diem15p = Diem15p.query.filter_by(
            MaHocSinh=hocsinh.MaHocSinh,
            MaHocKy=hockydachon,
            MaMonHoc=mondachon,
            MaNamHoc=namdachon
        ).all()
        hocsinh.diem15p_list = diem15p

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


    return render_template('nhapdiem.html',
                           userif=userif, VaiTro=VaiTro, lop=lop,
                           malopdachon=malopdachon,  # Truyền lớp đã chọn vào template
                           mondangday=mondangday,
                           namdangday=namdangday,
                           danhsachhocsinh=danhsachhocsinh_paginated,
                           hocky=hocky,
                           namdachon=namdachon,
                           hockydachon=hockydachon,
                           mondachon=mondachon,
                           pages = math.ceil(counter/app.config['PAGE_SIZE'])
                           )


@app.route('/xuatdiemtrungbinh', methods=["GET", "POST"])
def xuatdiemtb():
    userif = laythongtinnhanvien(current_user.MaTaiKhoan, current_user.LoaiTaiKhoan)
    lop = laylopcuagiaovien(userif.MaNhanVien)

    # Lọc dữ liệu
    malopdachontb = session.get('malopdachontb')
    namdachontb = session.get('namdachontb')
    mondachontb = session.get('mondachontb')

    mondangdaytb = session.get('mondangdaytb', [])
    namdangdaytb = session.get('namdangdaytb', [])


    danhsachhocsinh = []
    counter = 0
    hockys=[]

    if request.method == 'POST':
        if 'filter_classtb' in request.form:
            malopdaloctb = request.form.get('malopdaloctb')
            session['malopdachontb'] = malopdaloctb
            malopdachontb = session.get('malopdachontb')


            mondangdaytb = laymonhoccuagiaovientheolop(userif.MaNhanVien, malopdaloctb)
            namdangdaytb = laynamhoccuagiaovien(userif.MaNhanVien, malopdaloctb)

            session['mondangdaytb'] = [{"MaMonHoc": mon.MaMonHoc, "TenMonHoc": mon.TenMonHoc} for mon in mondangdaytb]
            session['namdangdaytb'] = [{"MaNamHoc": nam.MaNamHoc, "TenNamHoc": nam.TenNamHoc} for nam in namdangdaytb]

        elif 'filter_detailstb' in request.form:
            manamhoctb = request.form.get('namhoctb')
            session['namdachontb'] = manamhoctb
            namdachontb = session.get('namdachontb')

            mamonhoctb = request.form.get('monhoctb')
            session['mondachontb'] = mamonhoctb
            mondachontb = session.get('mondachontb')

            # Lấy danh sách học sinh

    danhsachhocsinh,counter = laydanhsachdiemhocsinh(malopdachontb, namdachontb)
    page = request.args.get('page', 1, type=int)
    page_size = app.config['PAGE_SIZE']

    start = (page - 1) * page_size
    end = start + page_size
    danhsachhocsinh_paginated = danhsachhocsinh[start:end]

    hockys = layhockys(namdachontb)

    for hocsinh in danhsachhocsinh:
        hocsinh.diemtb_list = []
        for hocky in hockys:
            hocsinh.diemtb_list.append(
                laydiemtrungbinhhocky(hocsinh.MaHocSinh, namdachontb, hocky.MaHocKy, mondachontb))


    return render_template('xuatdiemtb.html',
                           userif=userif,
                           VaiTro=VaiTro,
                           lop=lop,
                           malopdachontb=malopdachontb,  # Truyền lớp đã chọn vào template
                           mondangdaytb=mondangdaytb,
                           namdangdaytb=namdangdaytb,
                           danhsachhocsinh=danhsachhocsinh_paginated,
                           namdachontb=namdachontb,
                           mondachontb=mondachontb,
                           hockys=hockys,
                           pages=math.ceil(counter / app.config['PAGE_SIZE'])
                           )

if __name__ == '__main__':
    app.run(debug=True)