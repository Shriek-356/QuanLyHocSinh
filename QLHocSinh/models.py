from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Double
from QLHocSinh import db
from QLHocSinh import app
from datetime import datetime
from sqlalchemy.orm import relationship
from enum import Enum as PyEnum
from sqlalchemy import Enum

class GioiTinh(PyEnum):
    NAM = "Nam"
    NU = "Nữ"
    KHAC = "Khác"

class TaiKhoan(db.Model):
    __tablename__ = 'TAIKHOAN'

    MaTaiKhoan = Column(Integer, primary_key=True, autoincrement=True)
    TenDangNhap = Column(String(20), nullable=False)
    MatKhau = Column(String(20), nullable=False)
    NgayTao = Column(DateTime, default=datetime.now)
    CCCD = Column(String(9), nullable=False)
    NgaySinh = Column(DateTime, default=datetime.now)
    LoaiTaiKhoan = Column(String(15))

    admin = relationship('Admin',backref='taikhoan', lazy=True)
    nhanvientruong = relationship('NhanVienTruong',backref='taikhoan', lazy=True)

    def __str__(self):
        return self.TenDangNhap


class Admin (db.Model):
    __tablename__ = 'ADMIN'
    MaNhanVien = Column(Integer, primary_key=True, autoincrement=True)
    MaTaiKhoan = Column(Integer, ForeignKey(TaiKhoan.MaTaiKhoan), nullable=False)
    TenNhanVien = Column(String(20), nullable=False)

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
    MaGiaoVien = Column(Integer, primary_key=True, autoincrement=True)
    MaMonHoc = Column(Integer, ForeignKey(MonHoc.MaMonHoc) ,nullable=False)
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

    def __str__(self):
        return self.TenHocKy

class Diem(db.Model):
    __tablename__ = 'DIEM'
    MaDiem = Column(Integer, primary_key=True, autoincrement=True)
    MaHocKy = Column(Integer, ForeignKey(HocKy.MaHocKy), nullable=False)
    MaNamHoc =Column(Integer,ForeignKey(NamHoc.MaNamHoc) ,nullable=False)
    Diem15pCot1 = Column(Double, nullable=False)
    Diem15pCot2 = Column(Double, nullable=True)
    Diem15pCot3 = Column(Double, nullable=True)
    Diem15pCot4 = Column(Double, nullable=True)
    Diem15pCot5 = Column(Double, nullable=True)
    Diem1TietCot1 = Column(Double, nullable=False)
    Diem1TietCot2 = Column(Double, nullable=True)
    Diem1TietCot3 = Column(Double, nullable=True)
    DiemCuoiKy = Column(Double, nullable=False)


ChiTietLopGV = db.Table('ChiTietLopGV',
                          Column('MaLop',Integer,ForeignKey(Lop.MaLop),nullable=False,primary_key=True),
                          Column('MaGV',Integer,ForeignKey(GiaoVien.MaGiaoVien),nullable=False,primary_key=True),
)

ChiTietLopHS = db.Table('ChiTietLopHS',
                          Column('MaLop',Integer,ForeignKey(Lop.MaLop),nullable=False,primary_key=True),
                          Column('MaHocSinh',Integer,ForeignKey(HocSinh.MaHocSinh),nullable=False,primary_key=True),
)

ChiTietDiem = db.Table('ChiTietDiem',
                          Column('MaDiem',Integer,ForeignKey(Diem.MaDiem),nullable=False,primary_key=True),
                          Column('MaHocSinh',Integer,ForeignKey(HocSinh.MaHocSinh),nullable=False,primary_key=True),
                          Column('MaMonHoc',Integer,ForeignKey(MonHoc.MaMonHoc),nullable=False,primary_key=True)
)



if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)