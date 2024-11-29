from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Double, Date, UniqueConstraint
from QLHocSinh import db
from QLHocSinh import app
from datetime import datetime
from sqlalchemy.orm import relationship
from enum import Enum as PyEnum
from sqlalchemy import Enum
from flask_login import UserMixin

class GioiTinh(PyEnum):
    NAM = "Nam"
    NU = "Nữ"
    KHAC = "Khác"

class VaiTro(PyEnum):
    ADMIN="Admin"
    STAFF="Nhân viên trường"
    TEACHER ="Giáo Viên"


class TaiKhoan(db.Model, UserMixin):
    __tablename__ = 'TAIKHOAN'

    MaTaiKhoan = Column(Integer, primary_key=True, autoincrement=True)
    TenDangNhap = Column(String(20), nullable=False)
    MatKhau = Column(String(20), nullable=False)
    NgayTao = Column(DateTime, default=datetime.now)
    CCCD = Column(String(9), nullable=False)
    NgaySinh = Column(Date)
    LoaiTaiKhoan = Column(Enum(VaiTro), default=VaiTro.STAFF, nullable=False)

    admin = relationship('Admin',backref='taikhoan', lazy=True)
    nhanvientruong = relationship('NhanVienTruong',backref='taikhoan', lazy=True)
    teacher = relationship('GiaoVien',backref='taikhoan', lazy=True)

    def __str__(self):
        return self.TenDangNhap

    def get_id(self):
        return str(self.MaTaiKhoan)


class Admin (db.Model):
    __tablename__ = 'ADMIN'
    MaNhanVien = Column(Integer, primary_key=True, autoincrement=True)
    MaTaiKhoan = Column(Integer, ForeignKey(TaiKhoan.MaTaiKhoan), nullable=False)
    TenNhanVien = Column(String(20), nullable=False)
    GioiTinh = Column(Enum(GioiTinh), nullable=False)

    def __str__(self):
        return self.TenNhanVien

class NhanVienTruong(db.Model):
    __tablename__ = 'NHANVIENTRUONG'
    MaNhanVien = Column(Integer, primary_key=True, autoincrement=True)
    MaTaiKhoan = Column(Integer, ForeignKey(TaiKhoan.MaTaiKhoan), nullable=False)
    TenNhanVien = Column(String(20), nullable=False)

    def __str__(self):
        return self.TenNhanVien



class MonHoc(db.Model):
    __tablename__ = 'MONHOC'
    MaMonHoc = Column(Integer, primary_key=True, autoincrement=True)
    TenMonHoc = Column(String(20), nullable=False)
    ThoiLuongHoc = Column(Integer, nullable=False)

    giaoviens = relationship('GiaoVien', backref='monhoc', lazy=True)
    diem15p = relationship('Diem15p', backref='monhoc', lazy=True)
    diem1tiet = relationship('Diem1Tiet', backref='monhoc', lazy=True)
    diemhocky = relationship('DiemHocKy', backref='monhoc', lazy=True)

    def __str__(self):
        return self.TenMonHoc


class Lop(db.Model):
    __tablename__ = 'LOP'
    MaLop = Column(Integer, primary_key=True, autoincrement=True)
    TenLop = Column(String(20),nullable=False)
    SoHocSinh = Column(Integer, nullable=False)

    def __str__(self):
        return self.TenLop



class GiaoVien(db.Model):
    __tablename__ = 'GIAOVIEN'
    MaNhanVien = Column(Integer, primary_key=True, autoincrement=True)
    MaMonHoc = Column(Integer, ForeignKey(MonHoc.MaMonHoc) ,nullable=False)
    MaTaiKhoan = Column(Integer, ForeignKey(TaiKhoan.MaTaiKhoan), nullable=False)
    TenGV = Column(String(20), nullable=False)
    DiaChi = Column(String(50))
    SoDienThoai = Column(String(10),nullable=False)

    def __str__(self):
        return self.TenGV


class HocSinh(db.Model):
    __tablename__ = 'HOCSINH'
    MaHocSinh = Column(Integer, primary_key=True, autoincrement=True)
    HoTen = Column(String(20), nullable=False)
    GioiTinh = Column(Enum(GioiTinh), nullable=False)
    NgaySinh = Column(DateTime, default=datetime.now)
    DiaChi = Column(String(50),nullable=False)
    SoDienThoai = Column(String(10),nullable=False)
    Email = Column(String(20), nullable=False)
    diem15p=relationship('Diem15p',backref='hocsinh',lazy=True)
    diem1tiet=relationship('Diem1Tiet',backref='hocsinh',lazy=True)
    diemhocky=relationship('DiemHocKy',backref='hocsinh',lazy=True)

    def __str__(self):
        return self.HoTen

class NamHoc(db.Model):
    MaNamHoc = Column(Integer, primary_key=True, autoincrement=True)
    TenNamHoc = Column(String(20), nullable=False)

    hockys = relationship('HocKy',backref='namhoc', lazy=True)

    def __str__(self):
        return self.TenNamHoc


class HocKy(db.Model):
    __tablename__ = 'HOCKY'
    MaHocKy = Column(Integer, primary_key=True, autoincrement=True)
    TenHocKy = Column(String(20), nullable=False)
    MaNamHoc = Column(Integer, ForeignKey(NamHoc.MaNamHoc) ,nullable=False)
    diems_15p = relationship('Diem15p', backref='hocky', lazy=True)
    diems_1tiet = relationship('Diem1Tiet', backref='hocky', lazy=True)
    diems_hocky = relationship('DiemHocKy', backref='hocky', lazy=True)


    def __str__(self):
        return self.TenHocKy

class Diem15p(db.Model):
    __tablename__ = 'DIEM15P'
    MaDiem15p = Column(Integer, primary_key=True, autoincrement=True)
    MaHocSinh = Column(Integer, ForeignKey(HocSinh.MaHocSinh), nullable=False)
    MaMonHoc = Column(Integer, ForeignKey(MonHoc.MaMonHoc), nullable=False)
    SoDiem15p = Column(Double, nullable=False)
    MaHocKy = Column(Integer, ForeignKey(HocKy.MaHocKy), nullable=False)
    MaNamHoc = Column(Integer, ForeignKey(NamHoc.MaNamHoc), nullable=False)

    def __str__(self):
        return self.MaDiem15p

class Diem1Tiet(db.Model):
    __tablename__ = 'DIEM1TIET'
    MaDiem1Tiet = Column(Integer, primary_key=True, autoincrement=True)
    MaHocSinh = Column(Integer, ForeignKey(HocSinh.MaHocSinh), nullable=False)
    MaMonHoc = Column(Integer, ForeignKey(MonHoc.MaMonHoc), nullable=False)
    SoDiem1Tiet = Column(Double, nullable=False)
    MaHocKy = Column(Integer, ForeignKey(HocKy.MaHocKy), nullable=False)
    MaNamHoc = Column(Integer, ForeignKey(NamHoc.MaNamHoc), nullable=False)

    def __str__(self):
        return self.MaDiem1Tiet

class DiemHocKy(db.Model):
    __tablename__ = 'DIEMHOCKY'
    MaDiemHocKy = Column(Integer, primary_key=True, autoincrement=True)
    MaHocSinh = Column(Integer, ForeignKey(HocSinh.MaHocSinh), nullable=False)
    MaMonHoc = Column(Integer, ForeignKey(MonHoc.MaMonHoc), nullable=False)
    SoDiemHocKy = Column(Double, nullable=False)
    MaHocKy = Column(Integer, ForeignKey(HocKy.MaHocKy), nullable=False)
    MaNamHoc = Column(Integer, ForeignKey(NamHoc.MaNamHoc), nullable=False)

    def __str__(self):
        return self.MaDiemHocKy

ChiTietLopGV = db.Table('ChiTietLopGV',
                         Column('MaLop', Integer, ForeignKey(Lop.MaLop), nullable=False, primary_key=True),
                         Column('MaGV', Integer, ForeignKey(GiaoVien.MaNhanVien), nullable=False, primary_key=True),
                         UniqueConstraint('MaLop', 'MaGV', name='uix_lop_gv')  # Đảm bảo mỗi giáo viên chỉ dạy một lớp duy nhất
)

ChiTietLopHS = db.Table('ChiTietLopHS',
                         Column('MaLop', Integer, ForeignKey(Lop.MaLop), nullable=False, primary_key=True),
                         Column('MaHocSinh', Integer, ForeignKey(HocSinh.MaHocSinh), nullable=False, primary_key=True),
                         UniqueConstraint('MaLop', 'MaHocSinh', name='uix_lop_hs')  # Đảm bảo học sinh chỉ có mặt trong lớp một lần
)

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)