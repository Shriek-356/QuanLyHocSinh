from QLHocSinh.models import *
from sqlalchemy import func, db, case


def check_login(username, password, role = VaiTro.ADMIN):
    query = TaiKhoan.query.filter(
        TaiKhoan.TenDangNhap == username.strip(),
        TaiKhoan.MatKhau == password
    )
    if role:
        query = query.filter(TaiKhoan.LoaiTaiKhoan == role)

    return query.first()

def get_user_by_id(user_id):
    return TaiKhoan.query.get(int(user_id))

def tinh_diem_TB(MaMonHoc=None):
    q = db.session.query(
        Lop.TenLop,
        Lop.SiSo,
        func.count(HocSinh.MaHocSinh).label('tong_hoc_sinh'),
        func.sum(
            case(
                [(func.avg(
                    Diem15p.SoDiem15p * 1 + Diem1Tiet.SoDiem1Tiet * 2 + DiemHocKy.SoDiemHocKy * 3
                ) >= 5, 1)],
                else_=0
            )
        ).label('so_luong_dat'),
        HocKy.TenHocKy,
        NamHoc.TenNamHoc
    ).join(ChiTietLopHS, Lop.MaLop == ChiTietLopHS.MaLop).join(
        HocSinh, ChiTietLopHS.MaHocSinh == HocSinh.MaHocSinh
    ).join(Diem15p, HocSinh.MaHocSinh == Diem15p.MaHocSinh).join(
        Diem1Tiet, HocSinh.MaHocSinh == Diem1Tiet.MaHocSinh
    ).join(DiemHocKy, HocSinh.MaHocSinh == DiemHocKy.MaHocSinh).join(
        HocKy, DiemHocKy.MaHocKy == HocKy.MaHocKy
    ).join(NamHoc, HocKy.MaNamHoc == NamHoc.MaNamHoc).filter(
        Diem15p.MaMonHoc == MaMonHoc,
        Diem1Tiet.MaMonHoc == MaMonHoc,
        DiemHocKy.MaMonHoc == MaMonHoc
    ).group_by(Lop.MaLop, HocKy.MaHocKy, NamHoc.MaNamHoc).all()

    return q