from pydoc import describe
from flask import request, render_template, redirect, flash
from flask_login import current_user, login_user, logout_user
from sqlalchemy import null
from app import app, db
from app.forms import LoginForm, RegisterForm, AddItemForm
from app.models import User, Item

@app.route('/')
def home():
    return render_template('home.html')

# 404 error page
def not_found(e):
    return render_template('404.html'), 404

app.register_error_handler(404, not_found)

@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        name = form.username.data
        email = form.email.data
        password = form.password.data

        user = User(name = name, email = email)
        user.set_password(password)
        db.session.add(user)
        db.session.commit()
        print(f"Created user {name} with email {email}")
        login_user(user, remember=True)
        return redirect('/')

    return render_template('register.html', form=form)


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():

        user = User.query.filter_by(name=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('Invalid username or password.')
            return redirect('/login')
        
        if login_user(user, remember=form.remember_me.data):
            return redirect('/')
        else:
            pass
    return render_template('login.html', form=form)

@app.route('/logout')
def logout():
    logout_user()
    return redirect('/')

@app.route('/user/<username>')
def user(username):
    user = User.query.filter_by(name=username).first_or_404()
    return render_template('user.html', user=user)

@app.route('/account')
def account():
    if current_user.is_anonymous:
        return redirect('/login')
    return render_template('account.html', user=current_user, edit=True)

@app.route('/account/delete', methods=['GET', 'POST'])
def delete():
    if current_user.is_anonymous:
        return redirect('/login')
    if request.method == 'GET':
        return render_template('account_delete.html')
    else:
        if current_user.is_authenticated:
            db.session.delete(current_user)
            db.session.commit()
        return redirect('/')

# for seller use to add item
# still missing something like redirect to seller's product display or something after 
@app.route('/product', methods=['GET', 'POST'])
def selling():
    form = AddItemForm()
    if form.validate_on_submit():
        name = form.name.data
        price = form.price.data
        description = form.description.data
 ## Update more product's information such as image,barcode,etc later 

        item = Item(name = name, price = price, description = description)
        db.session.add(item)
        db.session.commit()
        return redirect('/account')

    return render_template('product.html', form=form)

@app.route('/account/seller', methods=['GET', 'POST'])
def seller():
    if current_user.is_anonymous:
        return redirect('/login')
    if request.method == 'GET':
        return render_template('seller_confirm.html', user=current_user)

    #### My idea is to add one column role for user
    #### Only user has role "Seller" can go to the add_item form
    #### I havent figure out since I tried to add role column and update column's data but nothing change
'''
    else:
        if current_user.is_authenticated:
            user = User.query.get(id)
            user.role = "Seller"
            db.session.commit()
        return redirect('/')
    '''

# display products. Havent worked yet
@app.route('/market')
def market():
   item = Item.query.all()
   return render_template('market.html', item = item)

    