from app import db, logins
from flask_login import UserMixin
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash

# User's shopping cart
carts = db.Table('carts',
    db.Column('user_id', db.Integer, db.ForeignKey('user.id'), primary_key=True),
    db.Column('item_id', db.Integer, db.ForeignKey('item.id'), primary_key=True)
)

# LIsts of items
lists = db.Table('lists',
    db.Column('list_id', db.Integer, db.ForeignKey('list.id'), primary_key=True),
    db.Column('item_id', db.Integer, db.ForeignKey('item.id'), primary_key=True)
)

# User's purchased items
purchased = db.Table('purchased',
    db.Column('user_id', db.Integer, db.ForeignKey('user.id'), primary_key=True),
    db.Column('item_id', db.Integer, db.ForeignKey('item.id'))
)

# User Model
class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(128), index=True, unique=True)
    password_hash = db.Column(db.String(128))
    img = db.Column(db.String(30), nullable=False, default='default.jpg')
    seller = db.Column(db.Boolean(), default=False)
    cart = db.relationship('Item', secondary=carts,lazy='subquery')
    lists = db.relationship('List', backref='user', lazy=True)
    reviews = db.relationship('Review', backref='user', lazy=True)
    num_ratings = db.Column(db.Integer, default=0)
    rating = db.Column(db.Float, default=0.0)
    lang = db.Column(db.String(5), default = "en")
    purchase = db.relationship('Item', secondary=purchased, lazy='subquery')
    dark_theme = db.Column(db.Boolean(), default=False)

    @staticmethod
    @logins.user_loader
    def get_user(id):
        return User.query.get(id)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        return f'<User {self.name}>'

# Item Model
class Item(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(32), nullable=False)
    price = db.Column(db.Float(), nullable=False)
    description = db.Column(db.String(128),  nullable= False)
    img = db.Column(db.String(30), nullable=False, default='default.jpg')
    uploader = db.Column(db.Integer())
    reviews = db.relationship('Review', backref='item', lazy=True)
    discount_price = db.Column(db.Float(), nullable=True)
    end_sale = db.Column(db.DateTime, default=None)
    rating = db.Column(db.Float(), default=0.0)

    def __repr__(self):
        return f'<Item {self.name}>'

# List Model
class List(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(32), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    items = db.relationship('Item', secondary=lists, lazy='subquery')
    wishlist = db.Column(db.Boolean(), default=False)

# Review Model
class Review(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    item_id = db.Column(db.Integer, db.ForeignKey('item.id'), nullable=False)
    rating = db.Column(db.Integer(), nullable=False)
    content = db.Column(db.Text)
