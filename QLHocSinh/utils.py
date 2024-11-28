from QLHocSinh.models import TaiKhoan,VaiTro


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