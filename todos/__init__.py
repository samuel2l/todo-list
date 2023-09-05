from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_bcrypt import Bcrypt
app = Flask(__name__)
app.config['SECRET_KEY'] = 'bk94334098284g6'
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:22%40mypgadmin@localhost:5432/TodoApp'
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
#line below tells login_manager where the login page is
login_manager.login_view='login_page'
login_manager.login_message_category='info'
from todos import routes
