from QLHocSinh import app
from flask import render_template
from QLHocSinh.admin import *
@app.route('/')
def home():
    return render_template('index.html')


if __name__ == '__main__':
    app.run(debug=True)