from app import db, login
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(128), index=True, unique=True)
    password_hash = db.Column(db.String(128))
    img = db.Column(db.String(30), nullable=False, default='default.jpg')
    

    @staticmethod
    @login.user_loader
    def get_user(id):
        return User.query.get(id)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        return f'<User {self.name}>'


class Item(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(30), nullable= False, unique=True)
    price = db.Column(db.Integer(), nullable= False)
    description = db.Column(db.String(128),  nullable= False, unique=True)
    img = db.Column(db.String(30), nullable=False, default='default.jpg')

    def __repr__(self):
        return f'Item {self.name}'

