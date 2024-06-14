from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_bcrypt import Bcrypt
app = Flask(__name__)
app.config['SECRET_KEY'] = '' #insert your app key here
app.config['SQLALCHEMY_DATABASE_URI'] = ''#database URI goes here
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
#line below tells login_manager where the login page is
login_manager.login_view='login_page'
login_manager.login_message_category='info'
from todos import routes
