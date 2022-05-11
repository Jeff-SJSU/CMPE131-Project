import os
import secrets
from PIL import Image
from flask import request, render_template, redirect, flash, url_for
from flask_login import current_user, login_user, logout_user
from werkzeug.utils import secure_filename
from app import app, db
from app.forms import LoginForm, RegisterForm, AccountForm, AddItemForm, ListForm
from app.models import User, Item, List


@app.route('/')
def home():
    items = Item.query.all()
    return render_template('home.html', items=items)

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


@app.route('/login', strict_slashes=False, methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():

        user = User.query.filter_by(name=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('Invalid username or password.', 'error')
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

def update_img(form_img):
    random_hex = secrets.token_hex(8)
    img_name, img_ext = os.path.splitext(form_img.filename)
    image_filename = random_hex + img_ext
    basedir = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))
    img_path = os.path.join(basedir, 'static/images/', image_filename)
    
    resize = (200, 200)
    i = Image.open(form_img)
    i.thumbnail(resize)
    i.save(img_path)

    return image_filename

def update_item_img(form_img):
    random_hex = secrets.token_hex(8)
    img_name, img_ext = os.path.splitext(form_img.filename)
    image_filename = random_hex + img_ext
    basedir = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))
    img_path = os.path.join(basedir, 'static/images/products/', image_filename)
    
    resize = (400, 400)
    i = Image.open(form_img)
    i.thumbnail(resize)
    i.save(img_path)

    return image_filename

@app.route('/account', methods=['GET', 'POST'])
def account():
    if current_user.is_anonymous:
        return redirect('/login')
    form = AccountForm()
    if form.validate_on_submit():
        if form.img.data:
            img_file = update_img(form.img.data)
            current_user.img = img_file
        current_user.name = form.username.data
        current_user.email = form.email.data
        current_user.seller = form.role.data
        db.session.commit()
        flash('Your account information has been updated.', 'success')
        return redirect('/account')
    elif request.method == 'GET':
        form.username.data = current_user.name
        form.email.data = current_user.email
        form.role.data = current_user.seller
    return render_template('account.html', user=current_user, edit=True, form=form)

@app.route('/account/avatar/remove')
def remove_avatar():
    if current_user.is_anonymous:
        return redirect('/login')
    current_user.img = 'default.jpg'
    db.session.commit()
    return redirect('/account')

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

@app.route('/product/<int:id>')
def product(id):
    item = Item.query.get_or_404(id)
    return render_template('product.html', item=item)

# for seller use to add item
# still missing something like redirect to seller's product display or something after 
@app.route('/product', methods=['GET', 'POST'])
def selling():
    if current_user.is_anonymous:
        return redirect('/login')
    elif not current_user.seller:
        return redirect('/account')
    form = AddItemForm()
    if form.validate_on_submit():
        img = update_img(form.img.data)
        name = form.name.data
        price = form.price.data
        description = form.description.data
        
            
 ## Update more product's information such as image,barcode,etc later 

        item = Item(name = name, price = price, img = img, description = description)
        db.session.add(item)
        db.session.commit()
        return redirect(f'/product/{item.id}')

    return render_template('add_product.html', form=form)

@app.route('/cart')
def cart():
    return render_template('cart.html')

@app.route('/cart/add/<int:id>')
def add_to_cart(id):
    if current_user.is_anonymous:
        return redirect('/login')
    item = Item.query.get_or_404(id)
    current_user.cart.append(item)
    db.session.commit()
    return redirect('/cart')

@app.route('/cart/remove/<int:id>')
def remove_from_cart(id):
    if current_user.is_anonymous:
        return redirect('/login')
    item = Item.query.get_or_404(id)
    current_user.cart.remove(item)
    db.session.commit()
    return redirect('/cart')

@app.route('/cart/remove/all')
def clear_cart():
    if current_user.is_anonymous:
        return redirect('/login')
    current_user.cart = []
    db.session.commit()
    return redirect('/')

@app.route('/cart/checkout', methods=['POST'])
def checkout():
    if current_user.is_anonymous:
        return redirect('/login')
    current_user.cart = []
    db.session.commit()
    return redirect('/')

@app.route('/lists', methods = ['POST', 'GET'])
def lists():
    if current_user.is_anonymous:
        return redirect('/login')
    form = ListForm()
    if form.validate_on_submit():
        name = form.name.data
        list = List(name = name, user = current_user)
        db.session.add(list)
        db.session.commit()
    lists = List.query.filter_by(user_id = current_user.id).all()
    return render_template('lists.html', lists = lists, form = form)

@app.route('/lists/delete/<int:id>', methods=['GET'])
def delete_list(id):
    if current_user.is_anonymous:
        return redirect('/login')
    list = List.query.get_or_404(id)
    db.session.delete(list)
    db.session.commit()
    return redirect('/lists')
