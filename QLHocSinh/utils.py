from QLHocSinh.models import TaiKhoan


def check_login(username, password):

    return TaiKhoan.query.filter(TaiKhoan.TenDangNhap.__eq__(username.strip()) and TaiKhoan.MatKhau.__eq__(password)).first()