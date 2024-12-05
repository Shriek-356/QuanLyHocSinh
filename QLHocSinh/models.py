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
    TenDangNhap = Column(String(50),unique=True, nullable=False)
    MatKhau = Column(String(50), nullable=False)
    NgayTao = Column(DateTime, default=datetime.now)
    CCCD = Column(String(12), nullable=False)
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
    MaTaiKhoan = Column(Integer, ForeignKey(TaiKhoan.MaTaiKhoan,ondelete="CASCADE"), nullable=False)
    TenNhanVien = Column(String(50), nullable=False)
    GioiTinh = Column(Enum(GioiTinh), nullable=False)

    def __str__(self):
        return self.TenNhanVien

class NhanVienTruong(db.Model):
    __tablename__ = 'NHANVIENTRUONG'
    MaNhanVien = Column(Integer, primary_key=True, autoincrement=True)
    MaTaiKhoan = Column(Integer, ForeignKey(TaiKhoan.MaTaiKhoan, ondelete="CASCADE"), nullable=False)
    TenNhanVien = Column(String(50), nullable=False)

    def __str__(self):
        return self.TenNhanVien



class MonHoc(db.Model):
    __tablename__ = 'MONHOC'
    MaMonHoc = Column(Integer, primary_key=True, autoincrement=True)
    TenMonHoc = Column(String(50), nullable=False)
    ThoiLuongHoc = Column(Integer, nullable=False)

    diem15p = relationship('Diem15p', backref='monhoc', lazy=True)
    diem1tiet = relationship('Diem1Tiet', backref='monhoc', lazy=True)
    diemhocky = relationship('DiemHocKy', backref='monhoc', lazy=True)

    def __str__(self):
        return self.TenMonHoc

class KhoiLop(db.Model):
    __tablename__ = 'KHOILOP'

    MaKhoi = Column(Integer, primary_key=True, autoincrement=True)
    TenKhoi = Column(String(50), nullable=False)  # Ví dụ: "Khối 10", "Khối 11", "Khối 12"
    SoLopToiThieu = Column(Integer, nullable=False, default=1)  # Mỗi khối có ít nhất 1 lớp
    SoLopHienTai = Column(Integer, nullable=False, default=0)  # Đếm số lớp đã có trong khối


class Lop(db.Model):
    __tablename__ = 'LOP'
    MaLop = Column(Integer, primary_key=True, autoincrement=True)
    MaKhoi = Column(Integer, ForeignKey(KhoiLop.MaKhoi, ondelete="CASCADE"), nullable=False)  # Mỗi lớp thuộc một khối
    TenLop = Column(String(50),nullable=False)
    SiSo = Column(Integer, nullable=False, default=0)
    SiSoToiDa = Column(Integer, nullable=False, default=40)

    KhoiLop = relationship('KhoiLop', backref='lops', lazy=True)  # Quan hệ với khối lớp

    def __str__(self):
        return self.TenLop



class GiaoVien(db.Model):
    __tablename__ = 'GIAOVIEN'
    MaNhanVien = Column(Integer, primary_key=True, autoincrement=True)
    MaTaiKhoan = Column(Integer, ForeignKey(TaiKhoan.MaTaiKhoan, ondelete="CASCADE"), nullable=False)
    TenNhanVien = Column(String(50), nullable=False)
    DiaChi = Column(String(255))
    SoDienThoai = Column(String(10),nullable=False)

    def __str__(self):
        return self.TenGV


class HocSinh(db.Model):
    __tablename__ = 'HOCSINH'
    MaHocSinh = Column(Integer, primary_key=True, autoincrement=True)
    HoTen = Column(String(50), nullable=False)
    GioiTinh = Column(Enum(GioiTinh), nullable=False)
    NgaySinh = Column(DateTime, default=datetime.now)
    DiaChi = Column(String(50),nullable=False)
    SoDienThoai = Column(String(10),nullable=False)
    Email = Column(String(50), nullable=False)
    diem15p=relationship('Diem15p',backref='hocsinh',lazy=True)
    diem1tiet=relationship('Diem1Tiet',backref='hocsinh',lazy=True)
    diemhocky=relationship('DiemHocKy',backref='hocsinh',lazy=True)

    def __str__(self):
        return self.HoTen

class NamHoc(db.Model):
    MaNamHoc = Column(Integer, primary_key=True, autoincrement=True)
    TenNamHoc = Column(String(50), nullable=False)

    hockys = relationship('HocKy',backref='namhoc', lazy=True)

    def __str__(self):
        return self.TenNamHoc


class HocKy(db.Model):
    __tablename__ = 'HOCKY'
    MaHocKy = Column(Integer, primary_key=True, autoincrement=True)
    TenHocKy = Column(String(50), nullable=False)
    MaNamHoc = Column(Integer, ForeignKey(NamHoc.MaNamHoc) ,nullable=False)
    diems_15p = relationship('Diem15p', backref='hocky', lazy=True)
    diems_1tiet = relationship('Diem1Tiet', backref='hocky', lazy=True)
    diems_hocky = relationship('DiemHocKy', backref='hocky', lazy=True)

    def __str__(self):
        return self.TenHocKy

class Diem15p(db.Model):
    __tablename__ = 'DIEM15P'
    MaDiem15p = Column(Integer, primary_key=True, autoincrement=True)
    MaHocSinh = Column(Integer, ForeignKey(HocSinh.MaHocSinh,ondelete="CASCADE"), nullable=False)
    MaMonHoc = Column(Integer, ForeignKey(MonHoc.MaMonHoc,ondelete="CASCADE"), nullable=False)
    SoDiem15p = Column(Double, nullable=False)
    MaHocKy = Column(Integer, ForeignKey(HocKy.MaHocKy), nullable=False)
    MaNamHoc = Column(Integer, ForeignKey(NamHoc.MaNamHoc), nullable=False)

    def __str__(self):
        return self.MaDiem15p

class Diem1Tiet(db.Model):
    __tablename__ = 'DIEM1TIET'
    MaDiem1Tiet = Column(Integer, primary_key=True, autoincrement=True)
    MaHocSinh = Column(Integer, ForeignKey(HocSinh.MaHocSinh,ondelete="CASCADE"), nullable=False)
    MaMonHoc = Column(Integer, ForeignKey(MonHoc.MaMonHoc,ondelete="CASCADE"), nullable=False)
    SoDiem1Tiet = Column(Double, nullable=False)
    MaHocKy = Column(Integer, ForeignKey(HocKy.MaHocKy), nullable=False)
    MaNamHoc = Column(Integer, ForeignKey(NamHoc.MaNamHoc), nullable=False)

    def __str__(self):
        return self.MaDiem1Tiet

class DiemHocKy(db.Model):
    __tablename__ = 'DIEMHOCKY'
    MaDiemHocKy = Column(Integer, primary_key=True, autoincrement=True)
    MaHocSinh = Column(Integer, ForeignKey(HocSinh.MaHocSinh,ondelete="CASCADE"), nullable=False)
    MaMonHoc = Column(Integer, ForeignKey(MonHoc.MaMonHoc,ondelete="CASCADE"), nullable=False)
    SoDiemHocKy = Column(Double, nullable=False)
    MaHocKy = Column(Integer, ForeignKey(HocKy.MaHocKy), nullable=False)
    MaNamHoc = Column(Integer, ForeignKey(NamHoc.MaNamHoc), nullable=False)

    def __str__(self):
        return self.MaDiemHocKy



ChiTietLopGV = db.Table('ChiTietLopGV',
                         Column('MaLop', Integer, ForeignKey(Lop.MaLop,ondelete="CASCADE"), nullable=False, primary_key=True),
                         Column('MaGV', Integer, ForeignKey(GiaoVien.MaNhanVien,ondelete="CASCADE"), nullable=False, primary_key=True),
                         Column('MaNamHoc', Integer, ForeignKey(NamHoc.MaNamHoc), nullable=False),
                         Column('MaMonHoc', Integer, ForeignKey(MonHoc.MaMonHoc,ondelete="CASCADE"), nullable=False,primary_key=True),
)

ChiTietLopHS = db.Table('ChiTietLopHS',
                         Column('MaLop', Integer, ForeignKey(Lop.MaLop), nullable=False, primary_key=True),
                         Column('MaHocSinh', Integer, ForeignKey(HocSinh.MaHocSinh), nullable=False, primary_key=True),
                         Column('MaNamHoc', Integer, ForeignKey(NamHoc.MaNamHoc), nullable=False),
                         UniqueConstraint('MaLop', 'MaHocSinh', name='uix_lop_hs')
)

ChiTietMonHocGV = db.Table('ChiTietMonHocGV',
    Column('MaNhanVien', Integer, ForeignKey(GiaoVien.MaNhanVien,ondelete="CASCADE"), primary_key=True),
    Column('MaMonHoc', Integer, ForeignKey(MonHoc.MaMonHoc,ondelete="CASCADE"), primary_key=True),
    UniqueConstraint('MaNhanVien', 'MaMonHoc', name='uix_gv_mh')
)


class CauHinhLopHoc(db.Model):
    __tablename__ = 'CAUHINHLOPHOC'

    MaCauHinh = Column(Integer, primary_key=True, autoincrement=True)
    SiSoToiDa = Column(Integer, nullable=False, default=40)
    DoTuoiToiThieu = Column(Integer, nullable=False, default=15)
    DoTuoiToiDa = Column(Integer, nullable=False, default=20)
    NgayCapNhat = Column(DateTime, default=datetime.now, onupdate=datetime.now)

#du lieu hoc sinh
hoc_sinh_data = [
    {'HoTen': 'Nguyễn Văn A', 'GioiTinh': 'NAM', 'NgaySinh': datetime(2009, 5, 15), 'DiaChi': 'Hà Nội', 'SoDienThoai': '0912345678', 'Email': 'nguyenvana@gmail.com'},
    {'HoTen': 'Trần Thị B', 'GioiTinh': 'NU', 'NgaySinh': datetime(2009, 3, 25), 'DiaChi': 'Hồ Chí Minh', 'SoDienThoai': '0912345679', 'Email': 'tranthib@yahoo.com'},
    {'HoTen': 'Phạm Minh C', 'GioiTinh': 'NAM', 'NgaySinh': datetime(2009, 8, 10), 'DiaChi': 'Đà Nẵng', 'SoDienThoai': '0912345680', 'Email': 'phamminhc@gmail.com'},
    {'HoTen': 'Lê Thanh D', 'GioiTinh': 'NAM', 'NgaySinh': datetime(2009, 12, 20), 'DiaChi': 'Cần Thơ', 'SoDienThoai': '0912345681', 'Email': 'lethanhd@gmail.com'},
    {'HoTen': 'Đặng Hải E', 'GioiTinh': 'NAM', 'NgaySinh': datetime(2009, 7, 18), 'DiaChi': 'Nha Trang', 'SoDienThoai': '0912345682', 'Email': 'danghaie@gmail.com'},
    {'HoTen': 'Võ Hoàng F', 'GioiTinh': 'NU', 'NgaySinh': datetime(2009, 9, 5), 'DiaChi': 'Hà Nội', 'SoDienThoai': '0912345683', 'Email': 'vohoangf@yahoo.com'},
    {'HoTen': 'Hồ Bảo G', 'GioiTinh': 'NAM', 'NgaySinh': datetime(2009, 11, 22), 'DiaChi': 'Bình Dương', 'SoDienThoai': '0912345684', 'Email': 'hobaog@gmail.com'},
    {'HoTen': 'Ngô Thanh H', 'GioiTinh': 'NU', 'NgaySinh': datetime(2009, 1, 12), 'DiaChi': 'Phan Thiết', 'SoDienThoai': '0912345685', 'Email': 'ngothanhh@gmail.com'},
    {'HoTen': 'Bùi Văn I', 'GioiTinh': 'NAM', 'NgaySinh': datetime(2009, 4, 3), 'DiaChi': 'Vũng Tàu', 'SoDienThoai': '0912345686', 'Email': 'buiivt@gmail.com'},
    {'HoTen': 'Mai Minh K', 'GioiTinh': 'NU', 'NgaySinh': datetime(2009, 6, 28), 'DiaChi': 'Quảng Ninh', 'SoDienThoai': '0912345687', 'Email': 'maiminhk@yahoo.com'},
    {'HoTen': 'Cao Quang L', 'GioiTinh': 'NAM', 'NgaySinh': datetime(2008, 2, 12), 'DiaChi': 'Hải Phòng', 'SoDienThoai': '0912345688', 'Email': 'caoquangl@gmail.com'},
    {'HoTen': 'Phan Thanh M', 'GioiTinh': 'NAM', 'NgaySinh': datetime(2008, 10, 5), 'DiaChi': 'Bắc Giang', 'SoDienThoai': '0912345689', 'Email': 'phanthanhm@yahoo.com'},
    {'HoTen': 'Trương Quỳnh N', 'GioiTinh': 'NU', 'NgaySinh': datetime(2008, 9, 8), 'DiaChi': 'Cà Mau', 'SoDienThoai': '0912345690', 'Email': 'truongquynhn@gmail.com'},
    {'HoTen': 'Nguyễn Thị O', 'GioiTinh': 'NU', 'NgaySinh': datetime(2008, 7, 16), 'DiaChi': 'Quảng Nam', 'SoDienThoai': '0912345691', 'Email': 'nguyenthi.o@gmail.com'},
    {'HoTen': 'Lý Bảo P', 'GioiTinh': 'NAM', 'NgaySinh': datetime(2008, 11, 22), 'DiaChi': 'Long An', 'SoDienThoai': '0912345692', 'Email': 'lybaop@gmail.com'},
    {'HoTen': 'Lê Minh Q', 'GioiTinh': 'NAM', 'NgaySinh': datetime(2007, 4, 15), 'DiaChi': 'Vinh', 'SoDienThoai': '0912345693', 'Email': 'leminhq@yahoo.com'},
    {'HoTen': 'Trần Mai R', 'GioiTinh': 'NU', 'NgaySinh': datetime(2007, 12, 28), 'DiaChi': 'Hà Giang', 'SoDienThoai': '0912345694', 'Email': 'tranmair@gmail.com'},
    {'HoTen': 'Nguyễn Anh S', 'GioiTinh': 'NAM', 'NgaySinh': datetime(2007, 1, 5), 'DiaChi': 'Bến Tre', 'SoDienThoai': '0912345695', 'Email': 'nguyenanhs@gmail.com'},
    {'HoTen': 'Đoàn Bảo T', 'GioiTinh': 'NAM', 'NgaySinh': datetime(2007, 10, 25), 'DiaChi': 'Lâm Đồng', 'SoDienThoai': '0912345696', 'Email': 'doanbaot@gmail.com'},
    {'HoTen': 'Hoàng Thanh U', 'GioiTinh': 'NU', 'NgaySinh': datetime(2007, 6, 30), 'DiaChi': 'Sơn La', 'SoDienThoai': '0912345697', 'Email': 'hoangthanu@gmail.com'}
]

#Du lieu cua giao vien
giao_vien_data = [
    {'TenGV': 'Nguyễn Văn A', 'DiaChi': 'Hà Nội', 'SoDienThoai': '0912345678', 'MaMonHoc': 1, 'MaTaiKhoan': 9},
    {'TenGV': 'Trần Thị B', 'DiaChi': 'Hồ Chí Minh', 'SoDienThoai': '0912345679', 'MaMonHoc': 2, 'MaTaiKhoan': 10},
    {'TenGV': 'Phạm Minh C', 'DiaChi': 'Đà Nẵng', 'SoDienThoai': '0912345680', 'MaMonHoc': 3, 'MaTaiKhoan': 11},
    {'TenGV': 'Lê Thanh D', 'DiaChi': 'Cần Thơ', 'SoDienThoai': '0912345681', 'MaMonHoc': 4, 'MaTaiKhoan': 12},
    {'TenGV': 'Đặng Hải E', 'DiaChi': 'Nha Trang', 'SoDienThoai': '0912345682', 'MaMonHoc': 5, 'MaTaiKhoan': 13},
    {'TenGV': 'Võ Hoàng F', 'DiaChi': 'Hà Nội', 'SoDienThoai': '0912345683', 'MaMonHoc': 6, 'MaTaiKhoan': 14},
]

#Du lieu cua chi tiet mon hoc giao vien

mon_hoc_GV_data = [
    {'MaGiaoVien':1,'MaMonHoc':1},
    {'MaGiaoVien':1,'MaMonHoc':3},
    {'MaGiaoVien':2,'MaMonHoc':2},
    {'MaGiaoVien':3,'MaMonHoc':1},
    {'MaGiaoVien':3,'MaMonHoc':2},
    {'MaGiaoVien':3,'MaMonHoc':3},
    {'MaGiaoVien':4,'MaMonHoc':2},
    {'MaGiaoVien':4,'MaMonHoc':1},
    {'MaGiaoVien':5,'MaMonHoc':2},
    {'MaGiaoVien':5,'MaMonHoc':1},
    {'MaGiaoVien':6,'MaMonHoc':2},
]

#Du lieu cua chi tiet lop giao vien
lop_GV_data =[
    {'MaLop':1,'MaGV':1},
    {'MaLop':1,'MaGV':4},
    {'MaLop':1,'MaGV':3},
    {'MaLop':2,'MaGV':5},
    {'MaLop':2,'MaGV':2},
    {'MaLop':2,'MaGV':3},
    {'MaLop':3,'MaGV':1},
    {'MaLop':3,'MaGV':6},
    {'MaLop':3,'MaGV':3},
    {'MaLop':4,'MaGV':1},
    {'MaLop':4,'MaGV':6},
    {'MaLop':4,'MaGV':1},
]

#Du lieu lop
lop_data = [
    {'TenLop': 'Lớp 10A1', 'MaKhoi': 1, 'SiSo': 5},
    {'TenLop': 'Lớp 10A2', 'MaKhoi': 1, 'SiSo': 5},
    {'TenLop': 'Lớp 11A1', 'MaKhoi': 2, 'SiSo': 5},
    {'TenLop': 'Lớp 12A2', 'MaKhoi': 3, 'SiSo': 5},
]

#Dữ liệu môn
mon_hoc_data = [
            {'TenMonHoc': 'Toán', 'ThoiLuongHoc': 45},
            {'TenMonHoc': 'Văn', 'ThoiLuongHoc': 45},
            {'TenMonHoc': 'Anh', 'ThoiLuongHoc': 45},
]

#Dữ liệu về năm học
nam_hoc_data = [
            {'TenNamHoc':'2023-2024'}
]

#Dữ liệu về học kì
hoc_ki_data=[
            {'TenHocKy':'Học Kì 1','MaNamHoc':1},
            {'TenHocKy': 'Học Kì 2', 'MaNamHoc': 1}
]

#Dữ liệu chi tiết lớp học sinh

lop_HS_data=[
    {'MaLop':1,'MaHocSinh':1},
    {'MaLop':1,'MaHocSinh':2},
    {'MaLop':1,'MaHocSinh':3},
    {'MaLop':1,'MaHocSinh':4},
    {'MaLop':1,'MaHocSinh':5},
    {'MaLop':2,'MaHocSinh':6},
    {'MaLop':2,'MaHocSinh':7},
    {'MaLop':2,'MaHocSinh':8},
    {'MaLop':2,'MaHocSinh':9},
    {'MaLop':2,'MaHocSinh':10},
    {'MaLop':3,'MaHocSinh':11},
    {'MaLop':3,'MaHocSinh':12},
    {'MaLop':3,'MaHocSinh':13},
    {'MaLop':3,'MaHocSinh':14},
    {'MaLop':3,'MaHocSinh':15},
    {'MaLop':4,'MaHocSinh':16},
    {'MaLop':4,'MaHocSinh':17},
    {'MaLop':4,'MaHocSinh':18},
    {'MaLop':4,'MaHocSinh':19},
    {'MaLop':4,'MaHocSinh':20},
]

#Dữ liệu về điểm 15p
diem_15p_data = [
    {'MaHocSinh': 1, 'MaMonHoc': 1, 'SoDiem15p': 8.5, 'MaHocKy': 1, 'MaNamHoc': 1},
    {'MaHocSinh': 1, 'MaMonHoc': 1, 'SoDiem15p': 7, 'MaHocKy': 2, 'MaNamHoc': 1},
    {'MaHocSinh': 1, 'MaMonHoc': 2, 'SoDiem15p': 5, 'MaHocKy': 1, 'MaNamHoc': 1},
    {'MaHocSinh': 1, 'MaMonHoc': 2, 'SoDiem15p': 8.5, 'MaHocKy': 2, 'MaNamHoc': 1},
    {'MaHocSinh': 1, 'MaMonHoc': 3, 'SoDiem15p': 6, 'MaHocKy': 1, 'MaNamHoc': 1},
    {'MaHocSinh': 1, 'MaMonHoc': 3, 'SoDiem15p': 9, 'MaHocKy': 2, 'MaNamHoc': 1},

    {'MaHocSinh': 2, 'MaMonHoc': 1, 'SoDiem15p': 7.5, 'MaHocKy': 1, 'MaNamHoc': 1},
    {'MaHocSinh': 2, 'MaMonHoc': 1, 'SoDiem15p': 6.5, 'MaHocKy': 2, 'MaNamHoc': 1},
    {'MaHocSinh': 2, 'MaMonHoc': 2, 'SoDiem15p': 8.0, 'MaHocKy': 1, 'MaNamHoc': 1},
    {'MaHocSinh': 2, 'MaMonHoc': 2, 'SoDiem15p': 7.5, 'MaHocKy': 2, 'MaNamHoc': 1},
    {'MaHocSinh': 2, 'MaMonHoc': 3, 'SoDiem15p': 5.5, 'MaHocKy': 1, 'MaNamHoc': 1},
    {'MaHocSinh': 2, 'MaMonHoc': 3, 'SoDiem15p': 8.0, 'MaHocKy': 2, 'MaNamHoc': 1},

    {'MaHocSinh': 3, 'MaMonHoc': 1, 'SoDiem15p': 9.0, 'MaHocKy': 1, 'MaNamHoc': 1},
    {'MaHocSinh': 3, 'MaMonHoc': 1, 'SoDiem15p': 8.5, 'MaHocKy': 2, 'MaNamHoc': 1},
    {'MaHocSinh': 3, 'MaMonHoc': 2, 'SoDiem15p': 7.0, 'MaHocKy': 1, 'MaNamHoc': 1},
    {'MaHocSinh': 3, 'MaMonHoc': 2, 'SoDiem15p': 8.0, 'MaHocKy': 2, 'MaNamHoc': 1},
    {'MaHocSinh': 3, 'MaMonHoc': 3, 'SoDiem15p': 6.0, 'MaHocKy': 1, 'MaNamHoc': 1},
    {'MaHocSinh': 3, 'MaMonHoc': 3, 'SoDiem15p': 7.5, 'MaHocKy': 2, 'MaNamHoc': 1},

    {'MaHocSinh': 4, 'MaMonHoc': 1, 'SoDiem15p': 6.5, 'MaHocKy': 1, 'MaNamHoc': 1},
    {'MaHocSinh': 4, 'MaMonHoc': 1, 'SoDiem15p': 6.0, 'MaHocKy': 2, 'MaNamHoc': 1},
    {'MaHocSinh': 4, 'MaMonHoc': 2, 'SoDiem15p': 8.5, 'MaHocKy': 1, 'MaNamHoc': 1},
    {'MaHocSinh': 4, 'MaMonHoc': 2, 'SoDiem15p': 7.0, 'MaHocKy': 2, 'MaNamHoc': 1},
    {'MaHocSinh': 4, 'MaMonHoc': 3, 'SoDiem15p': 7.0, 'MaHocKy': 1, 'MaNamHoc': 1},
    {'MaHocSinh': 4, 'MaMonHoc': 3, 'SoDiem15p': 6.5, 'MaHocKy': 2, 'MaNamHoc': 1},

    {'MaHocSinh': 5, 'MaMonHoc': 1, 'SoDiem15p': 7.0, 'MaHocKy': 1, 'MaNamHoc': 1},
    {'MaHocSinh': 5, 'MaMonHoc': 1, 'SoDiem15p': 7.5, 'MaHocKy': 2, 'MaNamHoc': 1},
    {'MaHocSinh': 5, 'MaMonHoc': 2, 'SoDiem15p': 8.0, 'MaHocKy': 1, 'MaNamHoc': 1},
    {'MaHocSinh': 5, 'MaMonHoc': 2, 'SoDiem15p': 9.0, 'MaHocKy': 2, 'MaNamHoc': 1},
    {'MaHocSinh': 5, 'MaMonHoc': 3, 'SoDiem15p': 6.5, 'MaHocKy': 1, 'MaNamHoc': 1},
    {'MaHocSinh': 5, 'MaMonHoc': 3, 'SoDiem15p': 7.0, 'MaHocKy': 2, 'MaNamHoc': 1},

    {'MaHocSinh': 6, 'MaMonHoc': 1, 'SoDiem15p': 6.5, 'MaHocKy': 1, 'MaNamHoc': 1},
    {'MaHocSinh': 6, 'MaMonHoc': 1, 'SoDiem15p': 6.0, 'MaHocKy': 2, 'MaNamHoc': 1},
    {'MaHocSinh': 6, 'MaMonHoc': 2, 'SoDiem15p': 7.0, 'MaHocKy': 1, 'MaNamHoc': 1},
    {'MaHocSinh': 6, 'MaMonHoc': 2, 'SoDiem15p': 8.0, 'MaHocKy': 2, 'MaNamHoc': 1},
    {'MaHocSinh': 6, 'MaMonHoc': 3, 'SoDiem15p': 8.5, 'MaHocKy': 1, 'MaNamHoc': 1},
    {'MaHocSinh': 6, 'MaMonHoc': 3, 'SoDiem15p': 9.0, 'MaHocKy': 2, 'MaNamHoc': 1},

    {'MaHocSinh': 7, 'MaMonHoc': 1, 'SoDiem15p': 8.0, 'MaHocKy': 1, 'MaNamHoc': 1},
    {'MaHocSinh': 7, 'MaMonHoc': 1, 'SoDiem15p': 7.5, 'MaHocKy': 2, 'MaNamHoc': 1},
    {'MaHocSinh': 7, 'MaMonHoc': 2, 'SoDiem15p': 7.5, 'MaHocKy': 1, 'MaNamHoc': 1},
    {'MaHocSinh': 7, 'MaMonHoc': 2, 'SoDiem15p': 8.0, 'MaHocKy': 2, 'MaNamHoc': 1},
    {'MaHocSinh': 7, 'MaMonHoc': 3, 'SoDiem15p': 6.5, 'MaHocKy': 1, 'MaNamHoc': 1},
    {'MaHocSinh': 7, 'MaMonHoc': 3, 'SoDiem15p': 7.0, 'MaHocKy': 2, 'MaNamHoc': 1},

    {'MaHocSinh': 8, 'MaMonHoc': 1, 'SoDiem15p': 9.0, 'MaHocKy': 1, 'MaNamHoc': 1},
    {'MaHocSinh': 8, 'MaMonHoc': 1, 'SoDiem15p': 8.0, 'MaHocKy': 2, 'MaNamHoc': 1},
    {'MaHocSinh': 8, 'MaMonHoc': 2, 'SoDiem15p': 6.5, 'MaHocKy': 1, 'MaNamHoc': 1},
    {'MaHocSinh': 8, 'MaMonHoc': 2, 'SoDiem15p': 7.5, 'MaHocKy': 2, 'MaNamHoc': 1},
    {'MaHocSinh': 8, 'MaMonHoc': 3, 'SoDiem15p': 8.0, 'MaHocKy': 1, 'MaNamHoc': 1},
    {'MaHocSinh': 8, 'MaMonHoc': 3, 'SoDiem15p': 9.0, 'MaHocKy': 2, 'MaNamHoc': 1},

    {'MaHocSinh': 9, 'MaMonHoc': 1, 'SoDiem15p': 5.0, 'MaHocKy': 1, 'MaNamHoc': 1},
    {'MaHocSinh': 9, 'MaMonHoc': 1, 'SoDiem15p': 7.0, 'MaHocKy': 2, 'MaNamHoc': 1},
    {'MaHocSinh': 9, 'MaMonHoc': 2, 'SoDiem15p': 3.5, 'MaHocKy': 1, 'MaNamHoc': 1},
    {'MaHocSinh': 9, 'MaMonHoc': 2, 'SoDiem15p': 3.5, 'MaHocKy': 2, 'MaNamHoc': 1},
    {'MaHocSinh': 9, 'MaMonHoc': 3, 'SoDiem15p': 5.0, 'MaHocKy': 1, 'MaNamHoc': 1},
    {'MaHocSinh': 9, 'MaMonHoc': 3, 'SoDiem15p': 6.0, 'MaHocKy': 2, 'MaNamHoc': 1},

    {'MaHocSinh': 10, 'MaMonHoc': 1, 'SoDiem15p': 9.0, 'MaHocKy': 1, 'MaNamHoc': 1},
    {'MaHocSinh': 10, 'MaMonHoc': 1, 'SoDiem15p': 8.0, 'MaHocKy': 2, 'MaNamHoc': 1},
    {'MaHocSinh': 10, 'MaMonHoc': 2, 'SoDiem15p': 6.5, 'MaHocKy': 1, 'MaNamHoc': 1},
    {'MaHocSinh': 10, 'MaMonHoc': 2, 'SoDiem15p': 7.5, 'MaHocKy': 2, 'MaNamHoc': 1},
    {'MaHocSinh': 10, 'MaMonHoc': 3, 'SoDiem15p': 8.0, 'MaHocKy': 1, 'MaNamHoc': 1},
    {'MaHocSinh': 10, 'MaMonHoc': 3, 'SoDiem15p': 9.0, 'MaHocKy': 2, 'MaNamHoc': 1},

    {'MaHocSinh': 11, 'MaMonHoc': 1, 'SoDiem15p': 4.0, 'MaHocKy': 1, 'MaNamHoc': 1},
    {'MaHocSinh': 11, 'MaMonHoc': 1, 'SoDiem15p': 3.0, 'MaHocKy': 2, 'MaNamHoc': 1},
    {'MaHocSinh': 11, 'MaMonHoc': 2, 'SoDiem15p': 6.5, 'MaHocKy': 1, 'MaNamHoc': 1},
    {'MaHocSinh': 11, 'MaMonHoc': 2, 'SoDiem15p': 9.5, 'MaHocKy': 2, 'MaNamHoc': 1},
    {'MaHocSinh': 11, 'MaMonHoc': 3, 'SoDiem15p': 2.0, 'MaHocKy': 1, 'MaNamHoc': 1},
    {'MaHocSinh': 11, 'MaMonHoc': 3, 'SoDiem15p': 6.0, 'MaHocKy': 2, 'MaNamHoc': 1},

    {'MaHocSinh': 12, 'MaMonHoc': 1, 'SoDiem15p': 7.0, 'MaHocKy': 1, 'MaNamHoc': 1},
    {'MaHocSinh': 12, 'MaMonHoc': 1, 'SoDiem15p': 5.0, 'MaHocKy': 2, 'MaNamHoc': 1},
    {'MaHocSinh': 12, 'MaMonHoc': 2, 'SoDiem15p': 4.5, 'MaHocKy': 1, 'MaNamHoc': 1},
    {'MaHocSinh': 12, 'MaMonHoc': 2, 'SoDiem15p': 3.5, 'MaHocKy': 2, 'MaNamHoc': 1},
    {'MaHocSinh': 12, 'MaMonHoc': 3, 'SoDiem15p': 6.0, 'MaHocKy': 1, 'MaNamHoc': 1},
    {'MaHocSinh': 12, 'MaMonHoc': 3, 'SoDiem15p': 3.0, 'MaHocKy': 2, 'MaNamHoc': 1},

    {'MaHocSinh': 13, 'MaMonHoc': 1, 'SoDiem15p': 9.0, 'MaHocKy': 1, 'MaNamHoc': 1},
    {'MaHocSinh': 13, 'MaMonHoc': 1, 'SoDiem15p': 1.0, 'MaHocKy': 2, 'MaNamHoc': 1},
    {'MaHocSinh': 13, 'MaMonHoc': 2, 'SoDiem15p': 6.5, 'MaHocKy': 1, 'MaNamHoc': 1},
    {'MaHocSinh': 13, 'MaMonHoc': 2, 'SoDiem15p': 2.5, 'MaHocKy': 2, 'MaNamHoc': 1},
    {'MaHocSinh': 13, 'MaMonHoc': 3, 'SoDiem15p': 3.0, 'MaHocKy': 1, 'MaNamHoc': 1},
    {'MaHocSinh': 13, 'MaMonHoc': 3, 'SoDiem15p': 4.0, 'MaHocKy': 2, 'MaNamHoc': 1},

    {'MaHocSinh': 14, 'MaMonHoc': 1, 'SoDiem15p': 6.0, 'MaHocKy': 1, 'MaNamHoc': 1},
    {'MaHocSinh': 14, 'MaMonHoc': 1, 'SoDiem15p': 6.0, 'MaHocKy': 2, 'MaNamHoc': 1},
    {'MaHocSinh': 14, 'MaMonHoc': 2, 'SoDiem15p': 7.5, 'MaHocKy': 1, 'MaNamHoc': 1},
    {'MaHocSinh': 14, 'MaMonHoc': 2, 'SoDiem15p': 7.5, 'MaHocKy': 2, 'MaNamHoc': 1},
    {'MaHocSinh': 14, 'MaMonHoc': 3, 'SoDiem15p': 8.0, 'MaHocKy': 1, 'MaNamHoc': 1},
    {'MaHocSinh': 14, 'MaMonHoc': 3, 'SoDiem15p': 2.0, 'MaHocKy': 2, 'MaNamHoc': 1},

    {'MaHocSinh': 15, 'MaMonHoc': 1, 'SoDiem15p': 6.0, 'MaHocKy': 1, 'MaNamHoc': 1},
    {'MaHocSinh': 15, 'MaMonHoc': 1, 'SoDiem15p': 6.0, 'MaHocKy': 2, 'MaNamHoc': 1},
    {'MaHocSinh': 15, 'MaMonHoc': 2, 'SoDiem15p': 7.5, 'MaHocKy': 1, 'MaNamHoc': 1},
    {'MaHocSinh': 15, 'MaMonHoc': 2, 'SoDiem15p': 7.5, 'MaHocKy': 2, 'MaNamHoc': 1},
    {'MaHocSinh': 15, 'MaMonHoc': 3, 'SoDiem15p': 8.0, 'MaHocKy': 1, 'MaNamHoc': 1},
    {'MaHocSinh': 15, 'MaMonHoc': 3, 'SoDiem15p': 2.0, 'MaHocKy': 2, 'MaNamHoc': 1},

    {'MaHocSinh': 16, 'MaMonHoc': 1, 'SoDiem15p': 6.0, 'MaHocKy': 1, 'MaNamHoc': 1},
    {'MaHocSinh': 16, 'MaMonHoc': 1, 'SoDiem15p': 9.0, 'MaHocKy': 2, 'MaNamHoc': 1},
    {'MaHocSinh': 16, 'MaMonHoc': 2, 'SoDiem15p': 7.5, 'MaHocKy': 1, 'MaNamHoc': 1},
    {'MaHocSinh': 16, 'MaMonHoc': 2, 'SoDiem15p': 6.5, 'MaHocKy': 2, 'MaNamHoc': 1},
    {'MaHocSinh': 16, 'MaMonHoc': 3, 'SoDiem15p': 5.0, 'MaHocKy': 1, 'MaNamHoc': 1},
    {'MaHocSinh': 16, 'MaMonHoc': 3, 'SoDiem15p': 2.0, 'MaHocKy': 2, 'MaNamHoc': 1},

    {'MaHocSinh': 17, 'MaMonHoc': 1, 'SoDiem15p': 8.0, 'MaHocKy': 1, 'MaNamHoc': 1},
    {'MaHocSinh': 17, 'MaMonHoc': 1, 'SoDiem15p': 6.0, 'MaHocKy': 2, 'MaNamHoc': 1},
    {'MaHocSinh': 17, 'MaMonHoc': 2, 'SoDiem15p': 4.5, 'MaHocKy': 1, 'MaNamHoc': 1},
    {'MaHocSinh': 17, 'MaMonHoc': 2, 'SoDiem15p': 7.5, 'MaHocKy': 2, 'MaNamHoc': 1},
    {'MaHocSinh': 17, 'MaMonHoc': 3, 'SoDiem15p': 9.0, 'MaHocKy': 1, 'MaNamHoc': 1},
    {'MaHocSinh': 17, 'MaMonHoc': 3, 'SoDiem15p': 2.0, 'MaHocKy': 2, 'MaNamHoc': 1},

    {'MaHocSinh': 18, 'MaMonHoc': 1, 'SoDiem15p': 6.0, 'MaHocKy': 1, 'MaNamHoc': 1},
    {'MaHocSinh': 18, 'MaMonHoc': 1, 'SoDiem15p': 6.0, 'MaHocKy': 2, 'MaNamHoc': 1},
    {'MaHocSinh': 18, 'MaMonHoc': 2, 'SoDiem15p': 7.5, 'MaHocKy': 1, 'MaNamHoc': 1},
    {'MaHocSinh': 18, 'MaMonHoc': 2, 'SoDiem15p': 7.5, 'MaHocKy': 2, 'MaNamHoc': 1},
    {'MaHocSinh': 18, 'MaMonHoc': 3, 'SoDiem15p': 8.0, 'MaHocKy': 1, 'MaNamHoc': 1},
    {'MaHocSinh': 18, 'MaMonHoc': 3, 'SoDiem15p': 2.0, 'MaHocKy': 2, 'MaNamHoc': 1},

    {'MaHocSinh': 19, 'MaMonHoc': 1, 'SoDiem15p': 9.0, 'MaHocKy': 1, 'MaNamHoc': 1},
    {'MaHocSinh': 19, 'MaMonHoc': 1, 'SoDiem15p': 6.0, 'MaHocKy': 2, 'MaNamHoc': 1},
    {'MaHocSinh': 19, 'MaMonHoc': 2, 'SoDiem15p': 5.5, 'MaHocKy': 1, 'MaNamHoc': 1},
    {'MaHocSinh': 19, 'MaMonHoc': 2, 'SoDiem15p': 7.5, 'MaHocKy': 2, 'MaNamHoc': 1},
    {'MaHocSinh': 19, 'MaMonHoc': 3, 'SoDiem15p': 3.0, 'MaHocKy': 1, 'MaNamHoc': 1},
    {'MaHocSinh': 19, 'MaMonHoc': 3, 'SoDiem15p': 7.0, 'MaHocKy': 2, 'MaNamHoc': 1},

    {'MaHocSinh': 20, 'MaMonHoc': 1, 'SoDiem15p': 6.0, 'MaHocKy': 1, 'MaNamHoc': 1},
    {'MaHocSinh': 20, 'MaMonHoc': 1, 'SoDiem15p': 8.0, 'MaHocKy': 2, 'MaNamHoc': 1},
    {'MaHocSinh': 20, 'MaMonHoc': 2, 'SoDiem15p': 5.5, 'MaHocKy': 1, 'MaNamHoc': 1},
    {'MaHocSinh': 20, 'MaMonHoc': 2, 'SoDiem15p': 7.5, 'MaHocKy': 2, 'MaNamHoc': 1},
    {'MaHocSinh': 20, 'MaMonHoc': 3, 'SoDiem15p': 9.0, 'MaHocKy': 1, 'MaNamHoc': 1},
    {'MaHocSinh': 20, 'MaMonHoc': 3, 'SoDiem15p': 4.0, 'MaHocKy': 2, 'MaNamHoc': 1},
]

diem_1_tiet_data = [
    {'MaHocSinh': 1, 'MaMonHoc': 1, 'SoDiem1Tiet': 6.5, 'MaHocKy': 1, 'MaNamHoc': 1},
    {'MaHocSinh': 1, 'MaMonHoc': 1, 'SoDiem1Tiet': 7, 'MaHocKy': 2, 'MaNamHoc': 1},
    {'MaHocSinh': 1, 'MaMonHoc': 2, 'SoDiem1Tiet': 7, 'MaHocKy': 1, 'MaNamHoc': 1},
    {'MaHocSinh': 1, 'MaMonHoc': 2, 'SoDiem1Tiet': 5.5, 'MaHocKy': 2, 'MaNamHoc': 1},
    {'MaHocSinh': 1, 'MaMonHoc': 3, 'SoDiem1Tiet': 3, 'MaHocKy': 1, 'MaNamHoc': 1},
    {'MaHocSinh': 1, 'MaMonHoc': 3, 'SoDiem1Tiet': 9, 'MaHocKy': 2, 'MaNamHoc': 1},

    {'MaHocSinh': 2, 'MaMonHoc': 1, 'SoDiem1Tiet': 6.5, 'MaHocKy': 1, 'MaNamHoc': 1},
    {'MaHocSinh': 2, 'MaMonHoc': 1, 'SoDiem1Tiet': 6.5, 'MaHocKy': 2, 'MaNamHoc': 1},
    {'MaHocSinh': 2, 'MaMonHoc': 2, 'SoDiem1Tiet': 8.0, 'MaHocKy': 1, 'MaNamHoc': 1},
    {'MaHocSinh': 2, 'MaMonHoc': 2, 'SoDiem1Tiet': 9.5, 'MaHocKy': 2, 'MaNamHoc': 1},
    {'MaHocSinh': 2, 'MaMonHoc': 3, 'SoDiem1Tiet': 1.5, 'MaHocKy': 1, 'MaNamHoc': 1},
    {'MaHocSinh': 2, 'MaMonHoc': 3, 'SoDiem1Tiet': 8.0, 'MaHocKy': 2, 'MaNamHoc': 1},

    {'MaHocSinh': 3, 'MaMonHoc': 1, 'SoDiem1Tiet': 9.0, 'MaHocKy': 1, 'MaNamHoc': 1},
    {'MaHocSinh': 3, 'MaMonHoc': 1, 'SoDiem1Tiet': 5.5, 'MaHocKy': 2, 'MaNamHoc': 1},
    {'MaHocSinh': 3, 'MaMonHoc': 2, 'SoDiem1Tiet': 7.0, 'MaHocKy': 1, 'MaNamHoc': 1},
    {'MaHocSinh': 3, 'MaMonHoc': 2, 'SoDiem1Tiet': 8.0, 'MaHocKy': 2, 'MaNamHoc': 1},
    {'MaHocSinh': 3, 'MaMonHoc': 3, 'SoDiem1Tiet': 6.0, 'MaHocKy': 1, 'MaNamHoc': 1},
    {'MaHocSinh': 3, 'MaMonHoc': 3, 'SoDiem1Tiet': 8.5, 'MaHocKy': 2, 'MaNamHoc': 1},

    {'MaHocSinh': 4, 'MaMonHoc': 1, 'SoDiem1Tiet': 9.5, 'MaHocKy': 1, 'MaNamHoc': 1},
    {'MaHocSinh': 4, 'MaMonHoc': 1, 'SoDiem1Tiet': 6.0, 'MaHocKy': 2, 'MaNamHoc': 1},
    {'MaHocSinh': 4, 'MaMonHoc': 2, 'SoDiem1Tiet': 8.5, 'MaHocKy': 1, 'MaNamHoc': 1},
    {'MaHocSinh': 4, 'MaMonHoc': 2, 'SoDiem1Tiet': 7.0, 'MaHocKy': 2, 'MaNamHoc': 1},
    {'MaHocSinh': 4, 'MaMonHoc': 3, 'SoDiem1Tiet': 5.0, 'MaHocKy': 1, 'MaNamHoc': 1},
    {'MaHocSinh': 4, 'MaMonHoc': 3, 'SoDiem1Tiet': 6.5, 'MaHocKy': 2, 'MaNamHoc': 1},

    {'MaHocSinh': 5, 'MaMonHoc': 1, 'SoDiem1Tiet': 5.0, 'MaHocKy': 1, 'MaNamHoc': 1},
    {'MaHocSinh': 5, 'MaMonHoc': 1, 'SoDiem1Tiet': 7.5, 'MaHocKy': 2, 'MaNamHoc': 1},
    {'MaHocSinh': 5, 'MaMonHoc': 2, 'SoDiem1Tiet': 5.0, 'MaHocKy': 1, 'MaNamHoc': 1},
    {'MaHocSinh': 5, 'MaMonHoc': 2, 'SoDiem1Tiet': 9.0, 'MaHocKy': 2, 'MaNamHoc': 1},
    {'MaHocSinh': 5, 'MaMonHoc': 3, 'SoDiem1Tiet': 6.5, 'MaHocKy': 1, 'MaNamHoc': 1},
    {'MaHocSinh': 5, 'MaMonHoc': 3, 'SoDiem1Tiet': 6.0, 'MaHocKy': 2, 'MaNamHoc': 1},

    {'MaHocSinh': 6, 'MaMonHoc': 1, 'SoDiem1Tiet': 6.5, 'MaHocKy': 1, 'MaNamHoc': 1},
    {'MaHocSinh': 6, 'MaMonHoc': 1, 'SoDiem1Tiet': 6.0, 'MaHocKy': 2, 'MaNamHoc': 1},
    {'MaHocSinh': 6, 'MaMonHoc': 2, 'SoDiem1Tiet': 7.0, 'MaHocKy': 1, 'MaNamHoc': 1},
    {'MaHocSinh': 6, 'MaMonHoc': 2, 'SoDiem1Tiet': 8.0, 'MaHocKy': 2, 'MaNamHoc': 1},
    {'MaHocSinh': 6, 'MaMonHoc': 3, 'SoDiem1Tiet': 8.5, 'MaHocKy': 1, 'MaNamHoc': 1},
    {'MaHocSinh': 6, 'MaMonHoc': 3, 'SoDiem1Tiet': 5.0, 'MaHocKy': 2, 'MaNamHoc': 1},

    {'MaHocSinh': 7, 'MaMonHoc': 1, 'SoDiem1Tiet': 8.0, 'MaHocKy': 1, 'MaNamHoc': 1},
    {'MaHocSinh': 7, 'MaMonHoc': 1, 'SoDiem1Tiet': 9.5, 'MaHocKy': 2, 'MaNamHoc': 1},
    {'MaHocSinh': 7, 'MaMonHoc': 2, 'SoDiem1Tiet': 7.5, 'MaHocKy': 1, 'MaNamHoc': 1},
    {'MaHocSinh': 7, 'MaMonHoc': 2, 'SoDiem1Tiet': 8.0, 'MaHocKy': 2, 'MaNamHoc': 1},
    {'MaHocSinh': 7, 'MaMonHoc': 3, 'SoDiem1Tiet': 9.5, 'MaHocKy': 1, 'MaNamHoc': 1},
    {'MaHocSinh': 7, 'MaMonHoc': 3, 'SoDiem1Tiet': 7.0, 'MaHocKy': 2, 'MaNamHoc': 1},

    {'MaHocSinh': 8, 'MaMonHoc': 1, 'SoDiem1Tiet': 9.0, 'MaHocKy': 1, 'MaNamHoc': 1},
    {'MaHocSinh': 8, 'MaMonHoc': 1, 'SoDiem1Tiet': 8.0, 'MaHocKy': 2, 'MaNamHoc': 1},
    {'MaHocSinh': 8, 'MaMonHoc': 2, 'SoDiem1Tiet': 6.5, 'MaHocKy': 1, 'MaNamHoc': 1},
    {'MaHocSinh': 8, 'MaMonHoc': 2, 'SoDiem1Tiet': 7.5, 'MaHocKy': 2, 'MaNamHoc': 1},
    {'MaHocSinh': 8, 'MaMonHoc': 3, 'SoDiem1Tiet': 6.0, 'MaHocKy': 1, 'MaNamHoc': 1},
    {'MaHocSinh': 8, 'MaMonHoc': 3, 'SoDiem1Tiet': 9.0, 'MaHocKy': 2, 'MaNamHoc': 1},

    {'MaHocSinh': 9, 'MaMonHoc': 1, 'SoDiem1Tiet': 5.0, 'MaHocKy': 1, 'MaNamHoc': 1},
    {'MaHocSinh': 9, 'MaMonHoc': 1, 'SoDiem1Tiet': 7.0, 'MaHocKy': 2, 'MaNamHoc': 1},
    {'MaHocSinh': 9, 'MaMonHoc': 2, 'SoDiem1Tiet': 8.5, 'MaHocKy': 1, 'MaNamHoc': 1},
    {'MaHocSinh': 9, 'MaMonHoc': 2, 'SoDiem1Tiet': 3.5, 'MaHocKy': 2, 'MaNamHoc': 1},
    {'MaHocSinh': 9, 'MaMonHoc': 3, 'SoDiem1Tiet': 5.0, 'MaHocKy': 1, 'MaNamHoc': 1},
    {'MaHocSinh': 9, 'MaMonHoc': 3, 'SoDiem1Tiet': 6.0, 'MaHocKy': 2, 'MaNamHoc': 1},

    {'MaHocSinh': 10, 'MaMonHoc': 1, 'SoDiem1Tiet': 9.0, 'MaHocKy': 1, 'MaNamHoc': 1},
    {'MaHocSinh': 10, 'MaMonHoc': 1, 'SoDiem1Tiet': 8.0, 'MaHocKy': 2, 'MaNamHoc': 1},
    {'MaHocSinh': 10, 'MaMonHoc': 2, 'SoDiem1Tiet': 6.5, 'MaHocKy': 1, 'MaNamHoc': 1},
    {'MaHocSinh': 10, 'MaMonHoc': 2, 'SoDiem1Tiet': 7.5, 'MaHocKy': 2, 'MaNamHoc': 1},
    {'MaHocSinh': 10, 'MaMonHoc': 3, 'SoDiem1Tiet': 4.0, 'MaHocKy': 1, 'MaNamHoc': 1},
    {'MaHocSinh': 10, 'MaMonHoc': 3, 'SoDiem1Tiet': 9.0, 'MaHocKy': 2, 'MaNamHoc': 1},

    {'MaHocSinh': 11, 'MaMonHoc': 1, 'SoDiem1Tiet': 4.0, 'MaHocKy': 1, 'MaNamHoc': 1},
    {'MaHocSinh': 11, 'MaMonHoc': 1, 'SoDiem1Tiet': 3.0, 'MaHocKy': 2, 'MaNamHoc': 1},
    {'MaHocSinh': 11, 'MaMonHoc': 2, 'SoDiem1Tiet': 6.5, 'MaHocKy': 1, 'MaNamHoc': 1},
    {'MaHocSinh': 11, 'MaMonHoc': 2, 'SoDiem1Tiet': 9.5, 'MaHocKy': 2, 'MaNamHoc': 1},
    {'MaHocSinh': 11, 'MaMonHoc': 3, 'SoDiem1Tiet': 5.0, 'MaHocKy': 1, 'MaNamHoc': 1},
    {'MaHocSinh': 11, 'MaMonHoc': 3, 'SoDiem1Tiet': 6.0, 'MaHocKy': 2, 'MaNamHoc': 1},

    {'MaHocSinh': 12, 'MaMonHoc': 1, 'SoDiem1Tiet': 7.0, 'MaHocKy': 1, 'MaNamHoc': 1},
    {'MaHocSinh': 12, 'MaMonHoc': 1, 'SoDiem1Tiet': 5.0, 'MaHocKy': 2, 'MaNamHoc': 1},
    {'MaHocSinh': 12, 'MaMonHoc': 2, 'SoDiem1Tiet': 4.5, 'MaHocKy': 1, 'MaNamHoc': 1},
    {'MaHocSinh': 12, 'MaMonHoc': 2, 'SoDiem1Tiet': 3.5, 'MaHocKy': 2, 'MaNamHoc': 1},
    {'MaHocSinh': 12, 'MaMonHoc': 3, 'SoDiem1Tiet': 6.0, 'MaHocKy': 1, 'MaNamHoc': 1},
    {'MaHocSinh': 12, 'MaMonHoc': 3, 'SoDiem1Tiet': 3.0, 'MaHocKy': 2, 'MaNamHoc': 1},

    {'MaHocSinh': 13, 'MaMonHoc': 1, 'SoDiem1Tiet': 9.0, 'MaHocKy': 1, 'MaNamHoc': 1},
    {'MaHocSinh': 13, 'MaMonHoc': 1, 'SoDiem1Tiet': 3.0, 'MaHocKy': 2, 'MaNamHoc': 1},
    {'MaHocSinh': 13, 'MaMonHoc': 2, 'SoDiem1Tiet': 6.5, 'MaHocKy': 1, 'MaNamHoc': 1},
    {'MaHocSinh': 13, 'MaMonHoc': 2, 'SoDiem1Tiet': 4.5, 'MaHocKy': 2, 'MaNamHoc': 1},
    {'MaHocSinh': 13, 'MaMonHoc': 3, 'SoDiem1Tiet': 3.0, 'MaHocKy': 1, 'MaNamHoc': 1},
    {'MaHocSinh': 13, 'MaMonHoc': 3, 'SoDiem1Tiet': 7.0, 'MaHocKy': 2, 'MaNamHoc': 1},

    {'MaHocSinh': 14, 'MaMonHoc': 1, 'SoDiem1Tiet': 6.0, 'MaHocKy': 1, 'MaNamHoc': 1},
    {'MaHocSinh': 14, 'MaMonHoc': 1, 'SoDiem1Tiet': 6.0, 'MaHocKy': 2, 'MaNamHoc': 1},
    {'MaHocSinh': 14, 'MaMonHoc': 2, 'SoDiem1Tiet': 3.5, 'MaHocKy': 1, 'MaNamHoc': 1},
    {'MaHocSinh': 14, 'MaMonHoc': 2, 'SoDiem1Tiet': 7.5, 'MaHocKy': 2, 'MaNamHoc': 1},
    {'MaHocSinh': 14, 'MaMonHoc': 3, 'SoDiem1Tiet': 8.0, 'MaHocKy': 1, 'MaNamHoc': 1},
    {'MaHocSinh': 14, 'MaMonHoc': 3, 'SoDiem1Tiet': 2.0, 'MaHocKy': 2, 'MaNamHoc': 1},

    {'MaHocSinh': 15, 'MaMonHoc': 1, 'SoDiem1Tiet': 6.0, 'MaHocKy': 1, 'MaNamHoc': 1},
    {'MaHocSinh': 15, 'MaMonHoc': 1, 'SoDiem1Tiet': 6.0, 'MaHocKy': 2, 'MaNamHoc': 1},
    {'MaHocSinh': 15, 'MaMonHoc': 2, 'SoDiem1Tiet': 7.5, 'MaHocKy': 1, 'MaNamHoc': 1},
    {'MaHocSinh': 15, 'MaMonHoc': 2, 'SoDiem1Tiet': 6.5, 'MaHocKy': 2, 'MaNamHoc': 1},
    {'MaHocSinh': 15, 'MaMonHoc': 3, 'SoDiem1Tiet': 3.0, 'MaHocKy': 1, 'MaNamHoc': 1},
    {'MaHocSinh': 15, 'MaMonHoc': 3, 'SoDiem1Tiet': 2.0, 'MaHocKy': 2, 'MaNamHoc': 1},

    {'MaHocSinh': 16, 'MaMonHoc': 1, 'SoDiem1Tiet': 6.0, 'MaHocKy': 1, 'MaNamHoc': 1},
    {'MaHocSinh': 16, 'MaMonHoc': 1, 'SoDiem1Tiet': 9.0, 'MaHocKy': 2, 'MaNamHoc': 1},
    {'MaHocSinh': 16, 'MaMonHoc': 2, 'SoDiem1Tiet': 7.5, 'MaHocKy': 1, 'MaNamHoc': 1},
    {'MaHocSinh': 16, 'MaMonHoc': 2, 'SoDiem1Tiet': 6.5, 'MaHocKy': 2, 'MaNamHoc': 1},
    {'MaHocSinh': 16, 'MaMonHoc': 3, 'SoDiem1Tiet': 5.0, 'MaHocKy': 1, 'MaNamHoc': 1},
    {'MaHocSinh': 16, 'MaMonHoc': 3, 'SoDiem1Tiet': 4.0, 'MaHocKy': 2, 'MaNamHoc': 1},

    {'MaHocSinh': 17, 'MaMonHoc': 1, 'SoDiem1Tiet': 8.0, 'MaHocKy': 1, 'MaNamHoc': 1},
    {'MaHocSinh': 17, 'MaMonHoc': 1, 'SoDiem1Tiet': 6.0, 'MaHocKy': 2, 'MaNamHoc': 1},
    {'MaHocSinh': 17, 'MaMonHoc': 2, 'SoDiem1Tiet': 4.5, 'MaHocKy': 1, 'MaNamHoc': 1},
    {'MaHocSinh': 17, 'MaMonHoc': 2, 'SoDiem1Tiet': 7.5, 'MaHocKy': 2, 'MaNamHoc': 1},
    {'MaHocSinh': 17, 'MaMonHoc': 3, 'SoDiem1Tiet': 6.0, 'MaHocKy': 1, 'MaNamHoc': 1},
    {'MaHocSinh': 17, 'MaMonHoc': 3, 'SoDiem1Tiet': 2.0, 'MaHocKy': 2, 'MaNamHoc': 1},

    {'MaHocSinh': 18, 'MaMonHoc': 1, 'SoDiem1Tiet': 6.0, 'MaHocKy': 1, 'MaNamHoc': 1},
    {'MaHocSinh': 18, 'MaMonHoc': 1, 'SoDiem1Tiet': 9.0, 'MaHocKy': 2, 'MaNamHoc': 1},
    {'MaHocSinh': 18, 'MaMonHoc': 2, 'SoDiem1Tiet': 7.5, 'MaHocKy': 1, 'MaNamHoc': 1},
    {'MaHocSinh': 18, 'MaMonHoc': 2, 'SoDiem1Tiet': 9.5, 'MaHocKy': 2, 'MaNamHoc': 1},
    {'MaHocSinh': 18, 'MaMonHoc': 3, 'SoDiem1Tiet': 8.0, 'MaHocKy': 1, 'MaNamHoc': 1},
    {'MaHocSinh': 18, 'MaMonHoc': 3, 'SoDiem1Tiet': 2.0, 'MaHocKy': 2, 'MaNamHoc': 1},

    {'MaHocSinh': 19, 'MaMonHoc': 1, 'SoDiem1Tiet': 9.0, 'MaHocKy': 1, 'MaNamHoc': 1},
    {'MaHocSinh': 19, 'MaMonHoc': 1, 'SoDiem1Tiet': 6.0, 'MaHocKy': 2, 'MaNamHoc': 1},
    {'MaHocSinh': 19, 'MaMonHoc': 2, 'SoDiem1Tiet': 5.5, 'MaHocKy': 1, 'MaNamHoc': 1},
    {'MaHocSinh': 19, 'MaMonHoc': 2, 'SoDiem1Tiet': 7.5, 'MaHocKy': 2, 'MaNamHoc': 1},
    {'MaHocSinh': 19, 'MaMonHoc': 3, 'SoDiem1Tiet': 4.0, 'MaHocKy': 1, 'MaNamHoc': 1},
    {'MaHocSinh': 19, 'MaMonHoc': 3, 'SoDiem1Tiet': 7.0, 'MaHocKy': 2, 'MaNamHoc': 1},

    {'MaHocSinh': 20, 'MaMonHoc': 1, 'SoDiem1Tiet': 6.0, 'MaHocKy': 1, 'MaNamHoc': 1},
    {'MaHocSinh': 20, 'MaMonHoc': 1, 'SoDiem1Tiet': 8.0, 'MaHocKy': 2, 'MaNamHoc': 1},
    {'MaHocSinh': 20, 'MaMonHoc': 2, 'SoDiem1Tiet': 7.5, 'MaHocKy': 1, 'MaNamHoc': 1},
    {'MaHocSinh': 20, 'MaMonHoc': 2, 'SoDiem1Tiet': 7.5, 'MaHocKy': 2, 'MaNamHoc': 1},
    {'MaHocSinh': 20, 'MaMonHoc': 3, 'SoDiem1Tiet': 9.0, 'MaHocKy': 1, 'MaNamHoc': 1},
    {'MaHocSinh': 20, 'MaMonHoc': 3, 'SoDiem1Tiet': 6.0, 'MaHocKy': 2, 'MaNamHoc': 1},
]

diem_hoc_ky_data = [
    {'MaHocSinh': 1, 'MaMonHoc': 1, 'SoDiemHocKy': 8.5, 'MaHocKy': 1, 'MaNamHoc': 1},
    {'MaHocSinh': 1, 'MaMonHoc': 1, 'SoDiemHocKy': 7.5, 'MaHocKy': 2, 'MaNamHoc': 1},
    {'MaHocSinh': 1, 'MaMonHoc': 2, 'SoDiemHocKy': 5.5, 'MaHocKy': 1, 'MaNamHoc': 1},
    {'MaHocSinh': 1, 'MaMonHoc': 2, 'SoDiemHocKy': 8.5, 'MaHocKy': 2, 'MaNamHoc': 1},
    {'MaHocSinh': 1, 'MaMonHoc': 3, 'SoDiemHocKy': 7, 'MaHocKy': 1, 'MaNamHoc': 1},
    {'MaHocSinh': 1, 'MaMonHoc': 3, 'SoDiemHocKy': 9, 'MaHocKy': 2, 'MaNamHoc': 1},

    {'MaHocSinh': 2, 'MaMonHoc': 1, 'SoDiemHocKy': 7.5, 'MaHocKy': 1, 'MaNamHoc': 1},
    {'MaHocSinh': 2, 'MaMonHoc': 1, 'SoDiemHocKy': 6.5, 'MaHocKy': 2, 'MaNamHoc': 1},
    {'MaHocSinh': 2, 'MaMonHoc': 2, 'SoDiemHocKy': 6.0, 'MaHocKy': 1, 'MaNamHoc': 1},
    {'MaHocSinh': 2, 'MaMonHoc': 2, 'SoDiemHocKy': 6.5, 'MaHocKy': 2, 'MaNamHoc': 1},
    {'MaHocSinh': 2, 'MaMonHoc': 3, 'SoDiemHocKy': 9.5, 'MaHocKy': 1, 'MaNamHoc': 1},
    {'MaHocSinh': 2, 'MaMonHoc': 3, 'SoDiemHocKy': 8.0, 'MaHocKy': 2, 'MaNamHoc': 1},

    {'MaHocSinh': 3, 'MaMonHoc': 1, 'SoDiemHocKy': 9.0, 'MaHocKy': 1, 'MaNamHoc': 1},
    {'MaHocSinh': 3, 'MaMonHoc': 1, 'SoDiemHocKy': 8.5, 'MaHocKy': 2, 'MaNamHoc': 1},
    {'MaHocSinh': 3, 'MaMonHoc': 2, 'SoDiemHocKy': 5.0, 'MaHocKy': 1, 'MaNamHoc': 1},
    {'MaHocSinh': 3, 'MaMonHoc': 2, 'SoDiemHocKy': 8.0, 'MaHocKy': 2, 'MaNamHoc': 1},
    {'MaHocSinh': 3, 'MaMonHoc': 3, 'SoDiemHocKy': 5.0, 'MaHocKy': 1, 'MaNamHoc': 1},
    {'MaHocSinh': 3, 'MaMonHoc': 3, 'SoDiemHocKy': 7.5, 'MaHocKy': 2, 'MaNamHoc': 1},

    {'MaHocSinh': 4, 'MaMonHoc': 1, 'SoDiemHocKy': 6.5, 'MaHocKy': 1, 'MaNamHoc': 1},
    {'MaHocSinh': 4, 'MaMonHoc': 1, 'SoDiemHocKy': 8.0, 'MaHocKy': 2, 'MaNamHoc': 1},
    {'MaHocSinh': 4, 'MaMonHoc': 2, 'SoDiemHocKy': 6.5, 'MaHocKy': 1, 'MaNamHoc': 1},
    {'MaHocSinh': 4, 'MaMonHoc': 2, 'SoDiemHocKy': 7.0, 'MaHocKy': 2, 'MaNamHoc': 1},
    {'MaHocSinh': 4, 'MaMonHoc': 3, 'SoDiemHocKy': 7.0, 'MaHocKy': 1, 'MaNamHoc': 1},
    {'MaHocSinh': 4, 'MaMonHoc': 3, 'SoDiemHocKy': 6.5, 'MaHocKy': 2, 'MaNamHoc': 1},

    {'MaHocSinh': 5, 'MaMonHoc': 1, 'SoDiemHocKy': 7.0, 'MaHocKy': 1, 'MaNamHoc': 1},
    {'MaHocSinh': 5, 'MaMonHoc': 1, 'SoDiemHocKy': 4.5, 'MaHocKy': 2, 'MaNamHoc': 1},
    {'MaHocSinh': 5, 'MaMonHoc': 2, 'SoDiemHocKy': 8.0, 'MaHocKy': 1, 'MaNamHoc': 1},
    {'MaHocSinh': 5, 'MaMonHoc': 2, 'SoDiemHocKy': 9.0, 'MaHocKy': 2, 'MaNamHoc': 1},
    {'MaHocSinh': 5, 'MaMonHoc': 3, 'SoDiemHocKy': 6.5, 'MaHocKy': 1, 'MaNamHoc': 1},
    {'MaHocSinh': 5, 'MaMonHoc': 3, 'SoDiemHocKy': 9.0, 'MaHocKy': 2, 'MaNamHoc': 1},

    {'MaHocSinh': 6, 'MaMonHoc': 1, 'SoDiemHocKy': 6.5, 'MaHocKy': 1, 'MaNamHoc': 1},
    {'MaHocSinh': 6, 'MaMonHoc': 1, 'SoDiemHocKy': 3.0, 'MaHocKy': 2, 'MaNamHoc': 1},
    {'MaHocSinh': 6, 'MaMonHoc': 2, 'SoDiemHocKy': 7.0, 'MaHocKy': 1, 'MaNamHoc': 1},
    {'MaHocSinh': 6, 'MaMonHoc': 2, 'SoDiemHocKy': 8.0, 'MaHocKy': 2, 'MaNamHoc': 1},
    {'MaHocSinh': 6, 'MaMonHoc': 3, 'SoDiemHocKy': 8.5, 'MaHocKy': 1, 'MaNamHoc': 1},
    {'MaHocSinh': 6, 'MaMonHoc': 3, 'SoDiemHocKy': 5.0, 'MaHocKy': 2, 'MaNamHoc': 1},

    {'MaHocSinh': 7, 'MaMonHoc': 1, 'SoDiemHocKy': 8.0, 'MaHocKy': 1, 'MaNamHoc': 1},
    {'MaHocSinh': 7, 'MaMonHoc': 1, 'SoDiemHocKy': 7.5, 'MaHocKy': 2, 'MaNamHoc': 1},
    {'MaHocSinh': 7, 'MaMonHoc': 2, 'SoDiemHocKy': 6.5, 'MaHocKy': 1, 'MaNamHoc': 1},
    {'MaHocSinh': 7, 'MaMonHoc': 2, 'SoDiemHocKy': 6.0, 'MaHocKy': 2, 'MaNamHoc': 1},
    {'MaHocSinh': 7, 'MaMonHoc': 3, 'SoDiemHocKy': 6.5, 'MaHocKy': 1, 'MaNamHoc': 1},
    {'MaHocSinh': 7, 'MaMonHoc': 3, 'SoDiemHocKy': 7.0, 'MaHocKy': 2, 'MaNamHoc': 1},

    {'MaHocSinh': 8, 'MaMonHoc': 1, 'SoDiemHocKy': 9.0, 'MaHocKy': 1, 'MaNamHoc': 1},
    {'MaHocSinh': 8, 'MaMonHoc': 1, 'SoDiemHocKy': 8.0, 'MaHocKy': 2, 'MaNamHoc': 1},
    {'MaHocSinh': 8, 'MaMonHoc': 2, 'SoDiemHocKy': 6.5, 'MaHocKy': 1, 'MaNamHoc': 1},
    {'MaHocSinh': 8, 'MaMonHoc': 2, 'SoDiemHocKy': 7.5, 'MaHocKy': 2, 'MaNamHoc': 1},
    {'MaHocSinh': 8, 'MaMonHoc': 3, 'SoDiemHocKy': 8.0, 'MaHocKy': 1, 'MaNamHoc': 1},
    {'MaHocSinh': 8, 'MaMonHoc': 3, 'SoDiemHocKy': 9.0, 'MaHocKy': 2, 'MaNamHoc': 1},

    {'MaHocSinh': 9, 'MaMonHoc': 1, 'SoDiemHocKy': 5.0, 'MaHocKy': 1, 'MaNamHoc': 1},
    {'MaHocSinh': 9, 'MaMonHoc': 1, 'SoDiemHocKy': 7.0, 'MaHocKy': 2, 'MaNamHoc': 1},
    {'MaHocSinh': 9, 'MaMonHoc': 2, 'SoDiemHocKy': 3.5, 'MaHocKy': 1, 'MaNamHoc': 1},
    {'MaHocSinh': 9, 'MaMonHoc': 2, 'SoDiemHocKy': 3.5, 'MaHocKy': 2, 'MaNamHoc': 1},
    {'MaHocSinh': 9, 'MaMonHoc': 3, 'SoDiemHocKy': 5.0, 'MaHocKy': 1, 'MaNamHoc': 1},
    {'MaHocSinh': 9, 'MaMonHoc': 3, 'SoDiemHocKy': 6.0, 'MaHocKy': 2, 'MaNamHoc': 1},

    {'MaHocSinh': 10, 'MaMonHoc': 1, 'SoDiemHocKy': 9.0, 'MaHocKy': 1, 'MaNamHoc': 1},
    {'MaHocSinh': 10, 'MaMonHoc': 1, 'SoDiemHocKy': 8.0, 'MaHocKy': 2, 'MaNamHoc': 1},
    {'MaHocSinh': 10, 'MaMonHoc': 2, 'SoDiemHocKy': 6.5, 'MaHocKy': 1, 'MaNamHoc': 1},
    {'MaHocSinh': 10, 'MaMonHoc': 2, 'SoDiemHocKy': 7.5, 'MaHocKy': 2, 'MaNamHoc': 1},
    {'MaHocSinh': 10, 'MaMonHoc': 3, 'SoDiemHocKy': 8.0, 'MaHocKy': 1, 'MaNamHoc': 1},
    {'MaHocSinh': 10, 'MaMonHoc': 3, 'SoDiemHocKy': 9.0, 'MaHocKy': 2, 'MaNamHoc': 1},

    {'MaHocSinh': 11, 'MaMonHoc': 1, 'SoDiemHocKy': 4.0, 'MaHocKy': 1, 'MaNamHoc': 1},
    {'MaHocSinh': 11, 'MaMonHoc': 1, 'SoDiemHocKy': 3.0, 'MaHocKy': 2, 'MaNamHoc': 1},
    {'MaHocSinh': 11, 'MaMonHoc': 2, 'SoDiemHocKy': 6.5, 'MaHocKy': 1, 'MaNamHoc': 1},
    {'MaHocSinh': 11, 'MaMonHoc': 2, 'SoDiemHocKy': 9.5, 'MaHocKy': 2, 'MaNamHoc': 1},
    {'MaHocSinh': 11, 'MaMonHoc': 3, 'SoDiemHocKy': 2.0, 'MaHocKy': 1, 'MaNamHoc': 1},
    {'MaHocSinh': 11, 'MaMonHoc': 3, 'SoDiemHocKy': 6.0, 'MaHocKy': 2, 'MaNamHoc': 1},

    {'MaHocSinh': 12, 'MaMonHoc': 1, 'SoDiemHocKy': 7.0, 'MaHocKy': 1, 'MaNamHoc': 1},
    {'MaHocSinh': 12, 'MaMonHoc': 1, 'SoDiemHocKy': 5.0, 'MaHocKy': 2, 'MaNamHoc': 1},
    {'MaHocSinh': 12, 'MaMonHoc': 2, 'SoDiemHocKy': 4.5, 'MaHocKy': 1, 'MaNamHoc': 1},
    {'MaHocSinh': 12, 'MaMonHoc': 2, 'SoDiemHocKy': 3.5, 'MaHocKy': 2, 'MaNamHoc': 1},
    {'MaHocSinh': 12, 'MaMonHoc': 3, 'SoDiemHocKy': 6.0, 'MaHocKy': 1, 'MaNamHoc': 1},
    {'MaHocSinh': 12, 'MaMonHoc': 3, 'SoDiemHocKy': 3.0, 'MaHocKy': 2, 'MaNamHoc': 1},

    {'MaHocSinh': 13, 'MaMonHoc': 1, 'SoDiemHocKy': 9.0, 'MaHocKy': 1, 'MaNamHoc': 1},
    {'MaHocSinh': 13, 'MaMonHoc': 1, 'SoDiemHocKy': 4.0, 'MaHocKy': 2, 'MaNamHoc': 1},
    {'MaHocSinh': 13, 'MaMonHoc': 2, 'SoDiemHocKy': 6.5, 'MaHocKy': 1, 'MaNamHoc': 1},
    {'MaHocSinh': 13, 'MaMonHoc': 2, 'SoDiemHocKy': 2.5, 'MaHocKy': 2, 'MaNamHoc': 1},
    {'MaHocSinh': 13, 'MaMonHoc': 3, 'SoDiemHocKy': 3.0, 'MaHocKy': 1, 'MaNamHoc': 1},
    {'MaHocSinh': 13, 'MaMonHoc': 3, 'SoDiemHocKy': 4.0, 'MaHocKy': 2, 'MaNamHoc': 1},

    {'MaHocSinh': 14, 'MaMonHoc': 1, 'SoDiemHocKy': 8.0, 'MaHocKy': 1, 'MaNamHoc': 1},
    {'MaHocSinh': 14, 'MaMonHoc': 1, 'SoDiemHocKy': 6.0, 'MaHocKy': 2, 'MaNamHoc': 1},
    {'MaHocSinh': 14, 'MaMonHoc': 2, 'SoDiemHocKy': 7.5, 'MaHocKy': 1, 'MaNamHoc': 1},
    {'MaHocSinh': 14, 'MaMonHoc': 2, 'SoDiemHocKy': 5.5, 'MaHocKy': 2, 'MaNamHoc': 1},
    {'MaHocSinh': 14, 'MaMonHoc': 3, 'SoDiemHocKy': 8.0, 'MaHocKy': 1, 'MaNamHoc': 1},
    {'MaHocSinh': 14, 'MaMonHoc': 3, 'SoDiemHocKy': 5.0, 'MaHocKy': 2, 'MaNamHoc': 1},

    {'MaHocSinh': 15, 'MaMonHoc': 1, 'SoDiemHocKy': 6.0, 'MaHocKy': 1, 'MaNamHoc': 1},
    {'MaHocSinh': 15, 'MaMonHoc': 1, 'SoDiemHocKy': 6.0, 'MaHocKy': 2, 'MaNamHoc': 1},
    {'MaHocSinh': 15, 'MaMonHoc': 2, 'SoDiemHocKy': 7.5, 'MaHocKy': 1, 'MaNamHoc': 1},
    {'MaHocSinh': 15, 'MaMonHoc': 2, 'SoDiemHocKy': 7.5, 'MaHocKy': 2, 'MaNamHoc': 1},
    {'MaHocSinh': 15, 'MaMonHoc': 3, 'SoDiemHocKy': 8.0, 'MaHocKy': 1, 'MaNamHoc': 1},
    {'MaHocSinh': 15, 'MaMonHoc': 3, 'SoDiemHocKy': 2.0, 'MaHocKy': 2, 'MaNamHoc': 1},

    {'MaHocSinh': 16, 'MaMonHoc': 1, 'SoDiemHocKy': 6.0, 'MaHocKy': 1, 'MaNamHoc': 1},
    {'MaHocSinh': 16, 'MaMonHoc': 1, 'SoDiemHocKy': 9.0, 'MaHocKy': 2, 'MaNamHoc': 1},
    {'MaHocSinh': 16, 'MaMonHoc': 2, 'SoDiemHocKy': 7.5, 'MaHocKy': 1, 'MaNamHoc': 1},
    {'MaHocSinh': 16, 'MaMonHoc': 2, 'SoDiemHocKy': 6.5, 'MaHocKy': 2, 'MaNamHoc': 1},
    {'MaHocSinh': 16, 'MaMonHoc': 3, 'SoDiemHocKy': 5.0, 'MaHocKy': 1, 'MaNamHoc': 1},
    {'MaHocSinh': 16, 'MaMonHoc': 3, 'SoDiemHocKy': 2.0, 'MaHocKy': 2, 'MaNamHoc': 1},

    {'MaHocSinh': 17, 'MaMonHoc': 1, 'SoDiemHocKy': 8.0, 'MaHocKy': 1, 'MaNamHoc': 1},
    {'MaHocSinh': 17, 'MaMonHoc': 1, 'SoDiemHocKy': 6.0, 'MaHocKy': 2, 'MaNamHoc': 1},
    {'MaHocSinh': 17, 'MaMonHoc': 2, 'SoDiemHocKy': 4.5, 'MaHocKy': 1, 'MaNamHoc': 1},
    {'MaHocSinh': 17, 'MaMonHoc': 2, 'SoDiemHocKy': 7.5, 'MaHocKy': 2, 'MaNamHoc': 1},
    {'MaHocSinh': 17, 'MaMonHoc': 3, 'SoDiemHocKy': 9.0, 'MaHocKy': 1, 'MaNamHoc': 1},
    {'MaHocSinh': 17, 'MaMonHoc': 3, 'SoDiemHocKy': 2.0, 'MaHocKy': 2, 'MaNamHoc': 1},

    {'MaHocSinh': 18, 'MaMonHoc': 1, 'SoDiemHocKy': 6.0, 'MaHocKy': 1, 'MaNamHoc': 1},
    {'MaHocSinh': 18, 'MaMonHoc': 1, 'SoDiemHocKy': 6.0, 'MaHocKy': 2, 'MaNamHoc': 1},
    {'MaHocSinh': 18, 'MaMonHoc': 2, 'SoDiemHocKy': 7.5, 'MaHocKy': 1, 'MaNamHoc': 1},
    {'MaHocSinh': 18, 'MaMonHoc': 2, 'SoDiemHocKy': 7.5, 'MaHocKy': 2, 'MaNamHoc': 1},
    {'MaHocSinh': 18, 'MaMonHoc': 3, 'SoDiemHocKy': 8.0, 'MaHocKy': 1, 'MaNamHoc': 1},
    {'MaHocSinh': 18, 'MaMonHoc': 3, 'SoDiemHocKy': 2.0, 'MaHocKy': 2, 'MaNamHoc': 1},

    {'MaHocSinh': 19, 'MaMonHoc': 1, 'SoDiemHocKy': 9.0, 'MaHocKy': 1, 'MaNamHoc': 1},
    {'MaHocSinh': 19, 'MaMonHoc': 1, 'SoDiemHocKy': 6.0, 'MaHocKy': 2, 'MaNamHoc': 1},
    {'MaHocSinh': 19, 'MaMonHoc': 2, 'SoDiemHocKy': 5.5, 'MaHocKy': 1, 'MaNamHoc': 1},
    {'MaHocSinh': 19, 'MaMonHoc': 2, 'SoDiemHocKy': 7.5, 'MaHocKy': 2, 'MaNamHoc': 1},
    {'MaHocSinh': 19, 'MaMonHoc': 3, 'SoDiemHocKy': 3.0, 'MaHocKy': 1, 'MaNamHoc': 1},
    {'MaHocSinh': 19, 'MaMonHoc': 3, 'SoDiemHocKy': 7.0, 'MaHocKy': 2, 'MaNamHoc': 1},

    {'MaHocSinh': 20, 'MaMonHoc': 1, 'SoDiemHocKy': 6.0, 'MaHocKy': 1, 'MaNamHoc': 1},
    {'MaHocSinh': 20, 'MaMonHoc': 1, 'SoDiemHocKy': 8.0, 'MaHocKy': 2, 'MaNamHoc': 1},
    {'MaHocSinh': 20, 'MaMonHoc': 2, 'SoDiemHocKy': 5.5, 'MaHocKy': 1, 'MaNamHoc': 1},
    {'MaHocSinh': 20, 'MaMonHoc': 2, 'SoDiemHocKy': 7.5, 'MaHocKy': 2, 'MaNamHoc': 1},
    {'MaHocSinh': 20, 'MaMonHoc': 3, 'SoDiemHocKy': 9.0, 'MaHocKy': 1, 'MaNamHoc': 1},
    {'MaHocSinh': 20, 'MaMonHoc': 3, 'SoDiemHocKy': 4.0, 'MaHocKy': 2, 'MaNamHoc': 1},
]

if __name__ == '__main__':
    with app.app_context():
        db.create_all()

        # Chạy ứng dụng Flask
        app.run(debug=True)
