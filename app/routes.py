from operator import itemgetter
import os
import secrets
from PIL import Image
from flask import request, render_template, redirect, flash, url_for
from flask_login import current_user, login_user, logout_user
from werkzeug.utils import secure_filename
from app import app, db
from app.forms import LoginForm, RegisterForm, AccountForm, AddItemForm, ListForm, EditItemForm
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
        wishlist = List(name='Wishlist', user_id=user.id, wishlist=True)
        db.session.add(wishlist)
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
    items = Item.query.filter_by(uploader = current_user.id).all()
    return render_template('user.html', user=user, items = items)

def update_img(form_img, dir='avatars', size=200):
    random_hex = secrets.token_hex(8)
    img_name, img_ext = os.path.splitext(form_img.filename)
    image_filename = random_hex + img_ext
    basedir = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))
    img_path = os.path.join(basedir, 'static/images/', dir, image_filename)
    
    resize = (200, 200)
    i = Image.open(form_img)
    i.thumbnail(resize)
    i.save(img_path)

    return image_filename

@app.route('/account', methods=['GET', 'POST'])
def account():
    if current_user.is_anonymous:
        return redirect('/login')
    form = AccountForm()
    items = Item.query.filter_by(uploader = current_user.id).all()
    if form.validate_on_submit():
        if form.img.data:
            img_file = update_img(form.img.data, 'avatars')
            current_user.img = img_file
        valid_username = User.query.filter_by(name=form.username.data).first()
        valid_email = User.query.filter_by(email=form.email.data).first()
        itself_name = current_user.name == form.username.data
        itself_email = current_user.email == form.email.data
        if (valid_username is None or itself_name) and (valid_email is None or itself_email):
            current_user.name = form.username.data
            current_user.email = form.email.data
            flash('Your account information has been updated.', 'success')
        else:
            flash('This user name or email is already taken!', 'error')
        current_user.seller = form.role.data
        db.session.commit()
        
        return redirect('/account')
    elif request.method == 'GET':
        form.username.data = current_user.name
        form.email.data = current_user.email
        form.role.data = current_user.seller
    return render_template('account.html', user=current_user, edit=True, form=form, items = items)

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
        img = update_img(form.img.data, 'products', size=600)
        name = form.name.data
        price = form.price.data
        description = form.description.data
        uploader = current_user.id
        
 ## Update more product's information such as image,barcode,etc later 

        item = Item(name = name, price = price, img = img, description = description, uploader = uploader)
        db.session.add(item)
        db.session.commit()
        return redirect(f'/product/{item.id}')

    return render_template('add_product.html', form=form)

# For seller to edit their item
@app.route('/product/<int:id>/edit', methods=['GET', 'POST'])
def edit_item(id):
    if current_user.is_anonymous:
        return redirect('/login')
    elif not current_user.seller:
        return redirect('/account')

    form = EditItemForm()
    item = Item.query.get_or_404(id)
    if form.validate_on_submit():
        item.img = update_img(form.img.data, 'products', size=600)
        item.name = form.name.data
        item.price = form.price.data
        item.description = form.description.data
        item.uploader = current_user.id
        db.session.commit()
                
        start_sale_date = form.start_sale.data
        end_sale_date = form.end_sale.data
        return redirect(f'/product/{item.id}')

    return render_template('edit_product.html', form=form, item=item)

@app.route('/product/<int:id>/delete', methods=['GET', 'POST'])
def delete_listing(id):
    item = Item.query.get_or_404(id)
    if request.method == 'GET':
        return render_template('delete_product.html', item = item)
    else:
        db.session.delete(item)
        db.session.commit()
        return redirect('/')

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


@app.route('/lists/<int:id>', methods=['GET'])
def view_list(id):
    if current_user.is_anonymous:
        return redirect('/login')
    list = List.query.get_or_404(id)
    return render_template('list.html', list=list)

@app.route('/lists/<int:id>/delete', methods=['GET'])
def delete_list(id):
    if current_user.is_anonymous:
        return redirect('/login')
    list = List.query.get_or_404(id)
    db.session.delete(list)
    db.session.commit()
    return redirect('/lists')

@app.route('/lists/<int:list_id>/add/<int:id>')
def add_to_list(list_id, id):
    if current_user.is_anonymous:
        return redirect('/login')
    list = List.query.get_or_404(list_id)
    item = Item.query.get_or_404(id)
    list.items.append(item)
    db.session.commit()
    return redirect(f'/lists/{list_id}')

@app.route('/lists/<int:list_id>/remove/<int:id>')
def remove_from_list(list_id, id):
    if current_user.is_anonymous:
        return redirect('/login')
    list = List.query.get_or_404(list_id)
    item = Item.query.get_or_404(id)
    list.items.remove(item)
    db.session.commit()
    return redirect(f'/lists/{list_id}')

@app.route('/lists/<int:id>/remove/all')
def clear_list(id):
    if current_user.is_anonymous:
        return redirect('/login')
    list = List.query.get_or_404(id)
    list.items = []
    db.session.commit()
    return redirect(f'/lists/{list_id}')

@app.route('/wishlist')
def wishlist():
    if current_user.is_anonymous:
        return redirect('/login')
    return redirect(f'/lists/{current_user.lists[0].id}')

