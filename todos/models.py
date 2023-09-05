from datetime import datetime

from todos import db, login_manager, app
from todos import bcrypt
from flask_login import UserMixin


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

class User(db.Model, UserMixin):
    id = db.Column(db.Integer(), primary_key=True, autoincrement=True)
    name = db.Column(db.String(length=1000), nullable=False)
    email = db.Column(db.String(length=10000), nullable=False)

    password_hash = db.Column(db.String(length=60), nullable=False)
    todo = db.relationship('Todos',backref = 'author',lazy = True)

    @property
    # the getter func
    def password(self):
        return self.password

    @password.setter
    def password(self, plain_text_password):
        self.password_hash = bcrypt.generate_password_hash(plain_text_password).decode('utf-8')

    def check_password_correction(self, attempted_password):
        return bcrypt.check_password_hash(self.password_hash, attempted_password)



class Todos(db.Model):
    id = db.Column(db.Integer(), primary_key=True, autoincrement=True)
    title = db.Column(db.String(length=1000), nullable=False)
    created = db.Column(db.DateTime, nullable=False,default=datetime.utcnow)
    content = db.Column(db.String(length=100000))
    user_id = db.Column(db.Integer(),db.ForeignKey('user.id'),nullable=False)
with app.app_context():
    db.create_all()

