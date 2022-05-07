from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, DecimalField
from wtforms.fields.simple import FileField
from wtforms.validators import DataRequired
from flask_wtf.file import FileField, FileAllowed

class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Sign In')

class RegisterForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Create Account')

class AddItemForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired()])
    price = DecimalField('Price', validators=[DataRequired()])
    img = FileField('Picture', validators=[FileAllowed(['jpg','png'])])
    description = StringField('Description ', validators=[DataRequired()])

class AccountForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired()])
    submit = SubmitField('Update')
    img = FileField('Profile Picture', validators=[FileAllowed(['jpg','png'])])
    role = BooleanField('Become a seller')
