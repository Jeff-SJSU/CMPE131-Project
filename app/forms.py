from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, DecimalField, DateField
from wtforms.validators import DataRequired, Optional, NumberRange, InputRequired
from flask_wtf.file import FileField, FileAllowed

# TODO: Change DataRequired -> InputRequired for all fields

#Login Form
class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Sign In')
#Register Form
class RegisterForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Create Account')
#AddItemForm
class AddItemForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired()])
    price = DecimalField('Price', validators=[DataRequired()])
    img = FileField('Item Picture', validators=[FileAllowed(['jpg','png'])])
    description = StringField('Description ', validators=[DataRequired()])

#EditItemForm
class EditItemForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired()])
    price = DecimalField('Price', validators=[DataRequired()])
    discount_price = DecimalField('Discount Price', validators=[Optional()])
    img = FileField('Item Picture', validators=[FileAllowed(['jpg','png'])])
    description = StringField('Description ', validators=[DataRequired()])
    end_sale= DateField('Sale ends on', format='%Y-%m-%d', validators=[Optional()])
#Account Form
class AccountForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired()])
    submit = SubmitField('Update')
    img = FileField('Profile Picture', validators=[FileAllowed(['jpg','png'])])
    role = BooleanField('Become a seller')
    lang = StringField('Language',validators=[DataRequired()])
#List Form
class ListForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired()])

#Review Form
class ReviewForm(FlaskForm):
    rating = DecimalField('Rating', validators=[InputRequired(), NumberRange(min=0, max=5)])
    review = StringField('Review', validators=[DataRequired()])

