from sqlalchemy.orm import aliased

from QLHocSinh.models import *
from sqlalchemy import func, case, cast
from QLHocSinh import db



def check_login(username, password):
    query = TaiKhoan.query.filter(
        TaiKhoan.TenDangNhap == username.strip(),
        TaiKhoan.MatKhau == password
    )
    return query.first()

def get_user_by_id(user_id):
    return TaiKhoan.query.get(int(user_id))


def tinh_diem_TB_hocsinh(monhocid=None, hockyid=None, namhocid=None):
    Diem15pAlias = aliased(Diem15p)
    Diem1TietAlias = aliased(Diem1Tiet)
    DiemHocKyAlias = aliased(DiemHocKy)

    subquery = db.session.query(
        HocSinh.MaHocSinh,
        func.sum(Diem15pAlias.SoDiem15p * 1).label('total_diem15p'),
        func.count(Diem15pAlias.SoDiem15p).label('count_diem15p'),
        func.sum(Diem1TietAlias.SoDiem1Tiet * 2).label('total_diem1Tiet'),
        func.count(Diem1TietAlias.SoDiem1Tiet).label('count_diem1Tiet'),
        func.sum(DiemHocKyAlias.SoDiemHocKy * 3).label('total_diemHocKy'),
        func.count(DiemHocKyAlias.SoDiemHocKy).label('count_diemHocKy')
    ).join(Diem15pAlias, Diem15pAlias.MaHocSinh == HocSinh.MaHocSinh) \
        .join(Diem1TietAlias, Diem1TietAlias.MaHocSinh == HocSinh.MaHocSinh) \
        .join(DiemHocKyAlias, DiemHocKyAlias.MaHocSinh == HocSinh.MaHocSinh) \
        .filter(
            Diem15pAlias.MaMonHoc == monhocid,
            Diem1TietAlias.MaMonHoc == monhocid,
            DiemHocKyAlias.MaMonHoc == monhocid
        )


    if hockyid:
        subquery = subquery.filter(DiemHocKyAlias.MaHocKy == hockyid)


    if namhocid:
        subquery = subquery.join(HocKy, HocKy.MaHocKy == DiemHocKyAlias.MaHocKy) \
            .filter(HocKy.MaNamHoc == namhocid)


    subquery = subquery.group_by(HocSinh.MaHocSinh).subquery()

    return subquery



def tinh_so_hs_diem_TB_lon_hon_5(monhocid=None, hockyid=None, namhocid=None):

    subquery = tinh_diem_TB_hocsinh(monhocid, hockyid, namhocid)

    ChiTietLopHS_Alias_1 = aliased(ChiTietLopHS)
    ChiTietLopHS_Alias_2 = aliased(ChiTietLopHS)

    query = db.session.query(
        ChiTietLopHS_Alias_1.c.MaLop,
        func.count().label('so_hs_co_diem_TB_lon_hon_5')
    ).join(subquery, subquery.c.MaHocSinh == ChiTietLopHS_Alias_1.c.MaHocSinh) \
        .join(ChiTietLopHS_Alias_2, ChiTietLopHS_Alias_2.c.MaHocSinh == subquery.c.MaHocSinh)


    query = query.filter(
        (func.coalesce(subquery.c.total_diem15p, 0) / func.coalesce(subquery.c.count_diem15p, 1) +
         func.coalesce(subquery.c.total_diem1Tiet, 0) / func.coalesce(subquery.c.count_diem1Tiet, 1) +
         func.coalesce(subquery.c.total_diemHocKy, 0) / func.coalesce(subquery.c.count_diemHocKy, 1)) / 6.0 >= 5
    )

    results = query.group_by(ChiTietLopHS_Alias_1.c.MaLop).all()

    return results


def laydanhsachhocsinh():

    q = db.session.query(
        Lop.TenLop,
        HocSinh.HoTen
    ).join(
        ChiTietLopHS, Lop.MaLop == ChiTietLopHS.c.MaLop
    ).join(
        HocSinh, HocSinh.MaHocSinh == ChiTietLopHS.c.MaHocSinh
    ).all()

    return q

def laymonhoc(monhocid=None):
    return db.session.query(MonHoc.MaMonHoc,MonHoc.TenMonHoc).filter(MonHoc.MaMonHoc==monhocid).all()

def laythongtinnhanvien(MaTaiKhoan, VaiTro):

    if VaiTro==VaiTro.STAFF:
        return NhanVienTruong.query.filter(MaTaiKhoan==NhanVienTruong.MaTaiKhoan).first()
    elif VaiTro==VaiTro.TEACHER:
        return GiaoVien.query.filter(MaTaiKhoan==GiaoVien.MaTaiKhoan).first()


def laylopcuagiaovien(MaNhanVien):
    query = db.session.query(Lop)\
             .join(ChiTietLopGV, Lop.MaLop == ChiTietLopGV.c.MaLop)\
             .filter(MaNhanVien == ChiTietLopGV.c.MaGV).all()
    return query

def laymonhoccuagiaovientheolop(MaNhanVien, MaLop):
    query = db.session.query(MonHoc) \
            .join(ChiTietLopGV, MonHoc.MaMonHoc == ChiTietLopGV.c.MaMonHoc) \
            .filter(MaNhanVien == ChiTietLopGV.c.MaGV,
                    MaLop == ChiTietLopGV.c.MaLop).all()
    return query

def laynamhoccuagiaovien(MaNhanVien, MaLop):
    query= db.session.query(NamHoc)\
           .join(ChiTietLopGV, NamHoc.MaNamHoc == ChiTietLopGV.c.MaNamHoc) \
           .filter(MaNhanVien == ChiTietLopGV.c.MaGV,
            MaLop == ChiTietLopGV.c.MaLop,
            ).all()

    return query

def layhocky(MaNhanVien, MaLop):
    query = db.session.query(HocKy) \
        .join(NamHoc, HocKy.MaNamHoc == NamHoc.MaNamHoc)\
        .join(ChiTietLopGV, NamHoc.MaNamHoc == ChiTietLopGV.c.MaNamHoc) \
        .filter(MaNhanVien == ChiTietLopGV.c.MaGV,
                MaLop == ChiTietLopGV.c.MaLop,
                ).all()
    return query

def laydanhsachdiemhocsinh(MaLop,MaNamHoc):

    query = db.session.query(HocSinh)\
    .join(ChiTietLopHS, HocSinh.MaHocSinh == ChiTietLopHS.c.MaHocSinh)\
    .filter(ChiTietLopHS.c.MaLop == MaLop,
            ChiTietLopHS.c.MaNamHoc == MaNamHoc
            )

    result = query.count()

    return query.all(),result

def laydiemtrungbinhhocky(ma_hoc_sinh, ma_nam_hoc, ma_hoc_ky, ma_mon_hoc):
    # Lấy tổng điểm 15 phút trong học kỳ và theo môn học
    diem15p = db.session.query(func.sum(Diem15p.SoDiem15p).label('diem15p_total')) \
        .filter(Diem15p.MaHocSinh == ma_hoc_sinh) \
        .filter(Diem15p.MaNamHoc == ma_nam_hoc) \
        .filter(Diem15p.MaHocKy == ma_hoc_ky) \
        .filter(Diem15p.MaMonHoc == ma_mon_hoc) \
        .scalar()  # Tổng điểm 15 phút

    # Lấy tổng điểm 1 tiết trong học kỳ và theo môn học
    diem1tiet = db.session.query(func.sum(Diem1Tiet.SoDiem1Tiet).label('diem1tiet_total')) \
        .filter(Diem1Tiet.MaHocSinh == ma_hoc_sinh) \
        .filter(Diem1Tiet.MaNamHoc == ma_nam_hoc) \
        .filter(Diem1Tiet.MaHocKy == ma_hoc_ky) \
        .filter(Diem1Tiet.MaMonHoc == ma_mon_hoc) \
        .scalar()  # Tổng điểm 1 tiết

    # Lấy tổng điểm học kỳ trong học kỳ và theo môn học
    diemhocky = db.session.query(func.sum(DiemHocKy.SoDiemHocKy).label('diemhocky_total')) \
        .filter(DiemHocKy.MaHocSinh == ma_hoc_sinh) \
        .filter(DiemHocKy.MaNamHoc == ma_nam_hoc) \
        .filter(DiemHocKy.MaHocKy == ma_hoc_ky) \
        .filter(DiemHocKy.MaMonHoc == ma_mon_hoc) \
        .scalar()  # Tổng điểm học kỳ

    # Đếm số lượng điểm 15 phút
    count_diem15p = db.session.query(Diem15p).filter(Diem15p.MaHocSinh == ma_hoc_sinh) \
        .filter(Diem15p.MaNamHoc == ma_nam_hoc) \
        .filter(Diem15p.MaHocKy == ma_hoc_ky) \
        .filter(Diem15p.MaMonHoc == ma_mon_hoc).count()

    # Đếm số lượng điểm 1 tiết
    count_diem1tiet = db.session.query(Diem1Tiet).filter(Diem1Tiet.MaHocSinh == ma_hoc_sinh) \
        .filter(Diem1Tiet.MaNamHoc == ma_nam_hoc) \
        .filter(Diem1Tiet.MaHocKy == ma_hoc_ky) \
        .filter(Diem1Tiet.MaMonHoc == ma_mon_hoc).count()

    # Đếm số lượng điểm học kỳ
    count_diemhocky = db.session.query(DiemHocKy).filter(DiemHocKy.MaHocSinh == ma_hoc_sinh) \
        .filter(DiemHocKy.MaNamHoc == ma_nam_hoc) \
        .filter(DiemHocKy.MaHocKy == ma_hoc_ky) \
        .filter(DiemHocKy.MaMonHoc == ma_mon_hoc).count()

    # Tính tổng điểm cho từng loại (với hệ số)
    total_points_15p = (diem15p or 0)
    total_points_1tiet = (diem1tiet or 0) * 2
    total_points_hocky = (diemhocky or 0) * 3

    # Tính tổng điểm
    total_points = total_points_15p + total_points_1tiet + total_points_hocky

    # Tính tổng số "con điểm" (với hệ số)
    total_weight = count_diem15p + (count_diem1tiet * 2) + (count_diemhocky * 3)

    # Trả về điểm trung bình học kỳ
    if total_weight == 0:
        return 0  # Trường hợp không có điểm nào
    return round(total_points / total_weight, 2)


def layhockys(MaNamHoc):
    return HocKy.query.filter(HocKy.MaNamHoc == MaNamHoc).all()


def dem_hocsinh_tutrungbinh_theolop(ma_nam_hoc, ma_hoc_ky, ma_mon_hoc):
    # Lấy danh sách lớp học theo năm học
    lop_hoc_list = db.session.query(Lop).join(ChiTietLopHS).filter(ChiTietLopHS.c.MaNamHoc == ma_nam_hoc).all()

    # Biến lưu kết quả
    result = {}

    # Duyệt qua từng lớp
    for lop_hoc in lop_hoc_list:
        # Lấy danh sách học sinh của lớp (qua bảng ChiTietLopHS)
        hoc_sinh_list = db.session.query(HocSinh).join(ChiTietLopHS).filter(
            ChiTietLopHS.c.MaLop == lop_hoc.MaLop,
            ChiTietLopHS.c.MaNamHoc == ma_nam_hoc
        ).all()

        # Biến đếm số học sinh đạt điểm trung bình >= 5 trong lớp
        count = 0
        total_hoc_sinh = len(hoc_sinh_list)  # Tổng số học sinh trong lớp

        # Duyệt qua từng học sinh trong lớp
        for hoc_sinh in hoc_sinh_list:
            # Tính điểm trung bình của từng học sinh
            diem_trung_binh = laydiemtrungbinhhocky(hoc_sinh.MaHocSinh, ma_nam_hoc, ma_hoc_ky, ma_mon_hoc)

            # Nếu điểm trung bình >= 5 thì tăng biến đếm
            if diem_trung_binh >= 5:
                count += 1

        # Tính tỷ lệ đạt >= 5
        if total_hoc_sinh > 0:
            ty_le = round((count / total_hoc_sinh) * 100, 2)
        else:
            ty_le = 0

        # Lưu kết quả cho lớp này, thêm thông tin tổng số học sinh
        result[lop_hoc.TenLop] = {
            'so_hocsinh_dat': count,
            'ty_le': ty_le,
            'tong_hocsinh': total_hoc_sinh  # Tổng số học sinh trong lớp
        }

    return result

