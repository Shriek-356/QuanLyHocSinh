"""Add ThoiLuongHoc column to MonHoc

Revision ID: 938747f5231a
Revises: 
Create Date: 2024-11-28 01:29:52.362400

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = '938747f5231a'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('admin')
    op.drop_table('chitietdiem')
    op.drop_table('taikhoan')
    op.drop_table('giaovien')
    op.drop_table('chitietlophs')
    op.drop_table('nhanvientruong')
    op.drop_table('lop')
    op.drop_table('hocsinh')
    op.drop_table('chitietlopgv')
    op.drop_table('diem')
    op.drop_table('hocky')
    op.drop_table('nam_hoc')
    op.drop_table('monhoc')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('monhoc',
    sa.Column('MaMonHoc', mysql.INTEGER(), autoincrement=True, nullable=False),
    sa.Column('TenMonHoc', mysql.VARCHAR(collation='utf8mb4_unicode_ci', length=20), nullable=False),
    sa.PrimaryKeyConstraint('MaMonHoc'),
    mysql_collate='utf8mb4_unicode_ci',
    mysql_default_charset='utf8mb4',
    mysql_engine='InnoDB'
    )
    op.create_table('nam_hoc',
    sa.Column('MaNamHoc', mysql.INTEGER(), autoincrement=True, nullable=False),
    sa.Column('TenNamHoc', mysql.VARCHAR(collation='utf8mb4_unicode_ci', length=20), nullable=False),
    sa.PrimaryKeyConstraint('MaNamHoc'),
    mysql_collate='utf8mb4_unicode_ci',
    mysql_default_charset='utf8mb4',
    mysql_engine='InnoDB'
    )
    op.create_table('hocky',
    sa.Column('MaHocKy', mysql.INTEGER(), autoincrement=True, nullable=False),
    sa.Column('TenHocKy', mysql.VARCHAR(collation='utf8mb4_unicode_ci', length=20), nullable=False),
    sa.Column('MaNamHoc', mysql.INTEGER(), autoincrement=False, nullable=False),
    sa.ForeignKeyConstraint(['MaNamHoc'], ['nam_hoc.MaNamHoc'], name='hocky_ibfk_1'),
    sa.PrimaryKeyConstraint('MaHocKy'),
    mysql_collate='utf8mb4_unicode_ci',
    mysql_default_charset='utf8mb4',
    mysql_engine='InnoDB'
    )
    op.create_table('diem',
    sa.Column('MaDiem', mysql.INTEGER(), autoincrement=True, nullable=False),
    sa.Column('MaHocKy', mysql.INTEGER(), autoincrement=False, nullable=False),
    sa.Column('MaNamHoc', mysql.INTEGER(), autoincrement=False, nullable=False),
    sa.Column('Diem15pCot1', mysql.DOUBLE(asdecimal=True), nullable=False),
    sa.Column('Diem15pCot2', mysql.DOUBLE(asdecimal=True), nullable=True),
    sa.Column('Diem15pCot3', mysql.DOUBLE(asdecimal=True), nullable=True),
    sa.Column('Diem15pCot4', mysql.DOUBLE(asdecimal=True), nullable=True),
    sa.Column('Diem15pCot5', mysql.DOUBLE(asdecimal=True), nullable=True),
    sa.Column('Diem1TietCot1', mysql.DOUBLE(asdecimal=True), nullable=False),
    sa.Column('Diem1TietCot2', mysql.DOUBLE(asdecimal=True), nullable=True),
    sa.Column('Diem1TietCot3', mysql.DOUBLE(asdecimal=True), nullable=True),
    sa.Column('DiemCuoiKy', mysql.DOUBLE(asdecimal=True), nullable=False),
    sa.ForeignKeyConstraint(['MaHocKy'], ['hocky.MaHocKy'], name='diem_ibfk_1'),
    sa.ForeignKeyConstraint(['MaNamHoc'], ['nam_hoc.MaNamHoc'], name='diem_ibfk_2'),
    sa.PrimaryKeyConstraint('MaDiem'),
    mysql_collate='utf8mb4_unicode_ci',
    mysql_default_charset='utf8mb4',
    mysql_engine='InnoDB'
    )
    op.create_table('chitietlopgv',
    sa.Column('MaLop', mysql.INTEGER(), autoincrement=False, nullable=False),
    sa.Column('MaGV', mysql.INTEGER(), autoincrement=False, nullable=False),
    sa.ForeignKeyConstraint(['MaGV'], ['giaovien.MaGiaoVien'], name='chitietlopgv_ibfk_2'),
    sa.ForeignKeyConstraint(['MaLop'], ['lop.MaLop'], name='chitietlopgv_ibfk_1'),
    sa.PrimaryKeyConstraint('MaLop', 'MaGV'),
    mysql_collate='utf8mb4_unicode_ci',
    mysql_default_charset='utf8mb4',
    mysql_engine='InnoDB'
    )
    op.create_table('hocsinh',
    sa.Column('MaHocSinh', mysql.INTEGER(), autoincrement=True, nullable=False),
    sa.Column('HoTen', mysql.VARCHAR(collation='utf8mb4_unicode_ci', length=20), nullable=False),
    sa.Column('GioiTinh', mysql.ENUM('NAM', 'NU', 'KHAC'), nullable=False),
    sa.Column('NgaySinh', mysql.DATETIME(), nullable=True),
    sa.Column('DiaChi', mysql.VARCHAR(collation='utf8mb4_unicode_ci', length=50), nullable=False),
    sa.Column('SoDienThoai', mysql.VARCHAR(collation='utf8mb4_unicode_ci', length=10), nullable=False),
    sa.Column('Email', mysql.VARCHAR(collation='utf8mb4_unicode_ci', length=20), nullable=False),
    sa.PrimaryKeyConstraint('MaHocSinh'),
    mysql_collate='utf8mb4_unicode_ci',
    mysql_default_charset='utf8mb4',
    mysql_engine='InnoDB'
    )
    op.create_table('lop',
    sa.Column('MaLop', mysql.INTEGER(), autoincrement=True, nullable=False),
    sa.Column('TenLop', mysql.VARCHAR(collation='utf8mb4_unicode_ci', length=20), nullable=False),
    sa.Column('SoHocSinh', mysql.INTEGER(), autoincrement=False, nullable=False),
    sa.PrimaryKeyConstraint('MaLop'),
    mysql_collate='utf8mb4_unicode_ci',
    mysql_default_charset='utf8mb4',
    mysql_engine='InnoDB'
    )
    op.create_table('nhanvientruong',
    sa.Column('MaNhanVien', mysql.INTEGER(), autoincrement=True, nullable=False),
    sa.Column('MaTaiKhoan', mysql.INTEGER(), autoincrement=False, nullable=False),
    sa.Column('TenNhanVien', mysql.VARCHAR(collation='utf8mb4_unicode_ci', length=20), nullable=False),
    sa.ForeignKeyConstraint(['MaTaiKhoan'], ['taikhoan.MaTaiKhoan'], name='nhanvientruong_ibfk_1'),
    sa.PrimaryKeyConstraint('MaNhanVien'),
    mysql_collate='utf8mb4_unicode_ci',
    mysql_default_charset='utf8mb4',
    mysql_engine='InnoDB'
    )
    op.create_table('chitietlophs',
    sa.Column('MaLop', mysql.INTEGER(), autoincrement=False, nullable=False),
    sa.Column('MaHocSinh', mysql.INTEGER(), autoincrement=False, nullable=False),
    sa.ForeignKeyConstraint(['MaHocSinh'], ['hocsinh.MaHocSinh'], name='chitietlophs_ibfk_2'),
    sa.ForeignKeyConstraint(['MaLop'], ['lop.MaLop'], name='chitietlophs_ibfk_1'),
    sa.PrimaryKeyConstraint('MaLop', 'MaHocSinh'),
    mysql_collate='utf8mb4_unicode_ci',
    mysql_default_charset='utf8mb4',
    mysql_engine='InnoDB'
    )
    op.create_table('giaovien',
    sa.Column('MaGiaoVien', mysql.INTEGER(), autoincrement=True, nullable=False),
    sa.Column('MaMonHoc', mysql.INTEGER(), autoincrement=False, nullable=False),
    sa.Column('TenGV', mysql.VARCHAR(collation='utf8mb4_unicode_ci', length=20), nullable=False),
    sa.Column('DiaChi', mysql.VARCHAR(collation='utf8mb4_unicode_ci', length=50), nullable=True),
    sa.Column('SoDienThoai', mysql.VARCHAR(collation='utf8mb4_unicode_ci', length=10), nullable=False),
    sa.ForeignKeyConstraint(['MaMonHoc'], ['monhoc.MaMonHoc'], name='giaovien_ibfk_1'),
    sa.PrimaryKeyConstraint('MaGiaoVien'),
    mysql_collate='utf8mb4_unicode_ci',
    mysql_default_charset='utf8mb4',
    mysql_engine='InnoDB'
    )
    op.create_table('taikhoan',
    sa.Column('MaTaiKhoan', mysql.INTEGER(), autoincrement=True, nullable=False),
    sa.Column('TenDangNhap', mysql.VARCHAR(collation='utf8mb4_unicode_ci', length=20), nullable=False),
    sa.Column('MatKhau', mysql.VARCHAR(collation='utf8mb4_unicode_ci', length=20), nullable=False),
    sa.Column('NgayTao', mysql.DATETIME(), nullable=True),
    sa.Column('CCCD', mysql.VARCHAR(collation='utf8mb4_unicode_ci', length=9), nullable=False),
    sa.Column('NgaySinh', mysql.DATETIME(), nullable=True),
    sa.Column('LoaiTaiKhoan', mysql.VARCHAR(collation='utf8mb4_unicode_ci', length=15), nullable=True),
    sa.PrimaryKeyConstraint('MaTaiKhoan'),
    mysql_collate='utf8mb4_unicode_ci',
    mysql_default_charset='utf8mb4',
    mysql_engine='InnoDB'
    )
    op.create_table('chitietdiem',
    sa.Column('MaDiem', mysql.INTEGER(), autoincrement=False, nullable=False),
    sa.Column('MaHocSinh', mysql.INTEGER(), autoincrement=False, nullable=False),
    sa.Column('MaMonHoc', mysql.INTEGER(), autoincrement=False, nullable=False),
    sa.ForeignKeyConstraint(['MaDiem'], ['diem.MaDiem'], name='chitietdiem_ibfk_1'),
    sa.ForeignKeyConstraint(['MaHocSinh'], ['hocsinh.MaHocSinh'], name='chitietdiem_ibfk_2'),
    sa.ForeignKeyConstraint(['MaMonHoc'], ['monhoc.MaMonHoc'], name='chitietdiem_ibfk_3'),
    sa.PrimaryKeyConstraint('MaDiem', 'MaHocSinh', 'MaMonHoc'),
    mysql_collate='utf8mb4_unicode_ci',
    mysql_default_charset='utf8mb4',
    mysql_engine='InnoDB'
    )
    op.create_table('admin',
    sa.Column('MaNhanVien', mysql.INTEGER(), autoincrement=True, nullable=False),
    sa.Column('MaTaiKhoan', mysql.INTEGER(), autoincrement=False, nullable=False),
    sa.Column('TenNhanVien', mysql.VARCHAR(collation='utf8mb4_unicode_ci', length=20), nullable=False),
    sa.ForeignKeyConstraint(['MaTaiKhoan'], ['taikhoan.MaTaiKhoan'], name='admin_ibfk_1'),
    sa.PrimaryKeyConstraint('MaNhanVien'),
    mysql_collate='utf8mb4_unicode_ci',
    mysql_default_charset='utf8mb4',
    mysql_engine='InnoDB'
    )
    # ### end Alembic commands ###