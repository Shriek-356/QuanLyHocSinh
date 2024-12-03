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


