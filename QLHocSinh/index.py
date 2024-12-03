from QLHocSinh import app
from flask import render_template, request, url_for,redirect
from QLHocSinh.admin import *
from QLHocSinh import utils,login
from flask_login import login_user, logout_user
from QLHocSinh.models import *
from QLHocSinh.utils import laythongtinnhanvien


@app.route('/')
def welcome():
    return render_template('index.html')


@app.route('/home')
def home():
    userif=laythongtinnhanvien(current_user.MaTaiKhoan,current_user.LoaiTaiKhoan)

    return render_template('home.html',VaiTro=VaiTro,userif=userif)

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
            msg="Tai khoan hoac mat khau khong dung"

    return render_template('login.html', msg=msg)

@app.route('/logout')
def signout():
    logout_user()
    return redirect(url_for('login'))

@app.route('/admin-login', methods=['POST'])
def login_admin():
    username = request.form['username']
    password = request.form['password']
    user = utils.check_login(username, password , role=VaiTro.ADMIN)
    if user:
        login_user(user)
        return redirect(url_for('admin.index'))
@app.route('/test1')
def test1():
    return render_template('test1.html')

@app.route('/test2')
def test2():
    return render_template('test2.html')



if __name__ == '__main__':
    app.run(debug=True)