
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
app = Flask(__name__)

migrate = Migrate()

app.secret_key='asdkjasjkdkj1ujikw8e91289dujasdmnaskjdas'
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:123456789@localhost/qlsvdb?charset=utf8mb4'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
app.config['PAGE_SIZE'] =4
db = SQLAlchemy(app=app)

migrate.init_app(app, db)

login = LoginManager(app=app)