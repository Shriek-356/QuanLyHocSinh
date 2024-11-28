from django.shortcuts import redirect

from QLHocSinh import app
from flask import render_template, request
from QLHocSinh.admin import *
from QLHocSinh import utils
@app.route('/')
def welcome():
    return render_template('index.html')

def home():
    return render_template('home.html')
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method.__eq__('POST'):
        username = request.form['username']
        password = request.form['password']
        user = utils.check_login(username, password)
        if user:
            return redirect(url_for('home'))

    return render_template('login.html')


if __name__ == '__main__':
    app.run(debug=True)