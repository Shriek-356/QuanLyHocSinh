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
    if current_user.is_authenticated:
       userif = laythongtinnhanvien(current_user.MaTaiKhoan,current_user.LoaiTaiKhoan)
       return render_template('home.html',VaiTro=VaiTro,userif=userif)
    else:
        return redirect(url_for('login'))

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
            msg="Tài khoản hoặc mật khẩu không đúng"

    return render_template('login.html', msg=msg)

@app.route('/logout')
def signout():
    logout_user()
    return redirect(url_for('login'))

@app.route('/admin-login', methods=['POST'])
def login_admin():
    username = request.form['username']
    password = request.form['password']
    user = utils.check_login(username, password, role= VaiTro.ADMIN)
    if user:
        login_user(user)
        return redirect(url_for('admin.index'))
    else:
        flash('Tên đăng nhập hoặc mật khẩu không đúng!', 'error')
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



@app.route('/danhsach_lop', methods=['GET', 'POST'])
def danhsach_lop():
    search_name = request.args.get('search_name', '')

    # Truy vấn các học sinh chưa có trong bảng ChiTietLopHS
    danhsach_lop_hocsinh = HocSinh.query.outerjoin(ChiTietLopHS).filter(ChiTietLopHS.c.MaHocSinh == None)

    # Nếu có tên tìm kiếm, lọc theo tên học sinh
    if search_name:
        danhsach_lop_hocsinh = danhsach_lop_hocsinh.filter(HocSinh.HoTen.ilike(f"%{search_name}%"))

    # Lấy thông tin người dùng
    userif = laythongtinnhanvien(current_user.MaTaiKhoan, current_user.LoaiTaiKhoan)

    return render_template('danhsach.html',
                           danhsach_lop_hocsinh=danhsach_lop_hocsinh,
                           userif=userif,
                           VaiTro=VaiTro,
                           search_name=search_name)


@app.route('/xoa_hocsinh/<int:hoc_sinh_id>', methods=['GET', 'POST'])
def xoa_hocsinh(hoc_sinh_id):
    # Tìm học sinh theo MaHocSinh
    hoc_sinh = HocSinh.query.get_or_404(hoc_sinh_id)

    # Xóa học sinh khỏi cơ sở dữ liệu
    db.session.delete(hoc_sinh)
    db.session.commit()

    # Chuyển hướng về trang danh sách học sinh sau khi xóa
    return redirect(url_for('danhsach_lop'))


@app.route('/them_hocsinh', methods=['GET', 'POST'])
def them_hocsinh():
    if request.method == 'POST':
        ten_hoc_sinh = request.form['ten_hoc_sinh']
        gioi_tinh = request.form['gioi_tinh']
        ngay_sinh = request.form['ngay_sinh']
        dia_chi = request.form['dia_chi']
        so_dien_thoai = request.form['so_dien_thoai']
        email = request.form['email']

        # Kiểm tra ngày sinh hợp lệ
        try:
            ngay_sinh_date = datetime.strptime(ngay_sinh, '%Y-%m-%d')
            today = datetime.today()
            tuoi = (today - ngay_sinh_date).days // 365
        except ValueError:
            return render_template('them.html', error="Ngày sinh không hợp lệ!")

        # Lấy cấu hình lớp học từ bảng CauHinhLopHoc
        cau_hinh = CauHinhLopHoc.query.order_by(CauHinhLopHoc.NgayCapNhat.desc()).first()
        if not cau_hinh:
            return render_template('them.html', error="Không tìm thấy cấu hình lớp học!")

        tuoi_toi_thieu = cau_hinh.DoTuoiToiThieu
        tuoi_toi_da = cau_hinh.DoTuoiToiDa

        # Kiểm tra độ tuổi hợp lệ
        if tuoi < tuoi_toi_thieu or tuoi > tuoi_toi_da:
            return render_template(
                'them.html',
                error=f"Tuổi của học sinh phải nằm trong khoảng {tuoi_toi_thieu} đến {tuoi_toi_da} tuổi!"
            )

        # Kiểm tra trùng số điện thoại hoặc email
        if HocSinh.query.filter_by(SoDienThoai=so_dien_thoai).first():
            return render_template('them.html', error="Số điện thoại đã tồn tại!")

        if HocSinh.query.filter_by(Email=email).first():
            return render_template('them.html', error="Email đã tồn tại!")

        # Thêm học sinh vào cơ sở dữ liệu
        try:
            new_hoc_sinh = HocSinh(
                HoTen=ten_hoc_sinh,
                GioiTinh=gioi_tinh,
                NgaySinh=ngay_sinh,
                DiaChi=dia_chi,
                SoDienThoai=so_dien_thoai,
                Email=email
            )
            db.session.add(new_hoc_sinh)
            db.session.commit()

            return render_template('them.html', success="Thêm học sinh thành công!")
        except Exception as e:
            db.session.rollback()
            return render_template('them.html', error=f"Lỗi: {str(e)}")

    return render_template('them.html')

@app.route('/hienthi_danhsach_lop_hocsinh', methods=['GET', 'POST'])
def hienthi_danhsach_lop_hocsinh():
    # Lấy danh sách năm học
    danh_sach_nam_hoc = db.session.query(NamHoc).all()

    # Lấy giá trị từ URL query parameters
    search_name = request.args.get('search_name', '')
    filter_class = request.args.get('filter_class', '')
    filter_year = request.args.get('nam_hoc', '')  # Thêm lọc theo năm học

    # Truy vấn danh sách lớp học
    classes = db.session.query(Lop).all()

    # Truy vấn danh sách học sinh với tham số lọc và tìm kiếm
    query = db.session.query(
        Lop.TenLop.label('lop'),
        HocSinh.HoTen.label('hoc_sinh'),
        HocSinh.GioiTinh.label('gioi_tinh'),
        HocSinh.NgaySinh.label('ngay_sinh'),
        HocSinh.DiaChi.label('dia_chi'),
        HocSinh.SoDienThoai.label('so_dien_thoai'),
        HocSinh.Email.label('email')
    ).join(
        ChiTietLopHS, ChiTietLopHS.c.MaHocSinh == HocSinh.MaHocSinh
    ).join(
        Lop, ChiTietLopHS.c.MaLop == Lop.MaLop
    )

    # Áp dụng lọc theo năm học nếu có
    if filter_year:
        query = query.filter(ChiTietLopHS.c.MaNamHoc == filter_year)

    # Áp dụng lọc theo lớp nếu có
    if filter_class:
        query = query.filter(Lop.MaLop == filter_class)

    # Áp dụng tìm kiếm theo tên học sinh nếu có
    if search_name:
        query = query.filter(HocSinh.HoTen.ilike(f"%{search_name}%"))

    print(filter_year)
    print(filter_class)
    # Lấy danh sách học sinh sau khi áp dụng các bộ lọc
    danhsach_lop_hocsinh = query.all()

    # Lấy thông tin người dùng hiện tại
    userif = laythongtinnhanvien(current_user.MaTaiKhoan, current_user.LoaiTaiKhoan)

    return render_template(
        'danhsachlop.html',
        danhsach_lop_hocsinh=danhsach_lop_hocsinh,
        userif=userif,
        VaiTro=VaiTro,
        classes=classes,
        search_name=search_name,  # Truyền giá trị search_name vào template
        filter_class=filter_class,
        filter_year=filter_year,  # Truyền giá trị filter_year vào template
        danh_sach_nam_hoc=danh_sach_nam_hoc
    )



@app.route('/lap_lop', methods=['GET', 'POST'])
def lap_lop():
    danh_sach_nam_hoc = db.session.query(NamHoc.MaNamHoc, NamHoc.TenNamHoc).all()

    # Truy vấn danh sách lớp
    danh_sach_lop = db.session.query(Lop.MaLop, Lop.TenLop).all()

    # Truy vấn danh sách học sinh chưa có trong bảng ChiTietLopHS
    subquery = db.session.query(ChiTietLopHS.c.MaHocSinh)  # Truy vấn cột MaHocSinh trong bảng ChiTietLopHS
    hoc_sinh_chua_xep_lop = db.session.query(
        HocSinh.MaHocSinh,
        HocSinh.HoTen,
        HocSinh.NgaySinh,
        HocSinh.GioiTinh,
        HocSinh.Email,
        HocSinh.DiaChi
    ).filter(~HocSinh.MaHocSinh.in_(subquery)).all()

    if request.method == 'POST':
        # Lấy giá trị năm học và lớp được chọn từ form
        ma_nam_hoc = request.form.get('nam_hoc')
        ma_lop = request.form.get('ma_lop')
        hoc_sinh_chon = request.form.getlist('hoc_sinh_da_chon')  # Lấy danh sách các học sinh đã chọn

        if ma_nam_hoc and ma_lop and hoc_sinh_chon:
            try:
                # Lấy cấu hình sĩ số tối đa từ bảng CauHinhLopHoc
                cau_hinh = db.session.query(CauHinhLopHoc).first()
                if not cau_hinh:
                    flash("Chưa có cấu hình lớp học. Vui lòng cấu hình trước!", "danger")
                    return redirect(url_for('lap_lop'))

                si_so_toi_da = cau_hinh.SiSoToiDa

                # Kiểm tra số lượng học sinh trong lớp hiện tại
                so_luong_hoc_sinh = db.session.query(ChiTietLopHS).filter(
                    ChiTietLopHS.c.MaLop == ma_lop,
                    ChiTietLopHS.c.MaNamHoc == ma_nam_hoc
                ).count()

                if so_luong_hoc_sinh + len(hoc_sinh_chon) > si_so_toi_da:
                    # Nếu số học sinh trong lớp + học sinh mới vượt quá sĩ số tối đa
                    flash(f"Lớp đã đầy (tối đa {si_so_toi_da} học sinh).", "danger")
                    return redirect(url_for('lap_lop'))

                # Thêm học sinh vào lớp
                for ma_hoc_sinh in hoc_sinh_chon:
                    # Thêm bản ghi vào bảng ChiTietLopHS
                    db.session.execute(
                        ChiTietLopHS.insert().values(
                            MaHocSinh=ma_hoc_sinh,
                            MaLop=ma_lop,
                            MaNamHoc=ma_nam_hoc  # Thêm MaNamHoc được chọn
                        )
                    )

                # Commit thay đổi vào cơ sở dữ liệu
                db.session.commit()

                # Thông báo thành công và tải lại trang
                flash("Thêm học sinh vào lớp thành công!", "success")
                return redirect(url_for('lap_lop'))

            except Exception as e:
                db.session.rollback()
                flash(f"Lỗi: {str(e)}", "danger")
                return redirect(url_for('lap_lop'))

        else:
            flash("Vui lòng chọn năm học, lớp và học sinh!", "warning")
            return redirect(url_for('lap_lop'))

    return render_template(
        'laplop.html',
        hoc_sinh_chua_xep_lop=hoc_sinh_chua_xep_lop,
        danh_sach_lop=danh_sach_lop,
        danh_sach_nam_hoc=danh_sach_nam_hoc
    )

if __name__ == '__main__':
    app.run(debug=True)