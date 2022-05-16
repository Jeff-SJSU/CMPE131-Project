
from datetime import datetime, date
from operator import itemgetter
import os
import secrets
from PIL import Image
from flask import request, render_template, redirect, flash, url_for
from flask_login import current_user, login_user, logout_user, login_required
from werkzeug.utils import secure_filename
from app import app, db, config
from app.forms import *
from app.models import User, Item, List, Review
from app.util import seller_required


@app.route('/')
def home():
    items = Item.query.all()
    return render_template('home.html', items=items)

# 404 error page
def not_found(e):
    return render_template('404.html'), 404

app.register_error_handler(404, not_found)

########## ACCOUNTS ##########

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
            return redirect(request.args.get('next', default='/'))
        else:
            pass
    return render_template('login.html', form=form)

@app.route('/logout')
def logout():
    logout_user()
    return redirect(request.referrer or '/')

@app.route('/user/<username>')
def user(username):
    user = User.query.filter_by(name=username).first_or_404()
    items = Item.query.filter_by(uploader=user.id).all()
    test_rating = 3.8
    return render_template('user.html', user=user, items=items, test_rating = test_rating)

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
@login_required
def account():
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
@login_required
def remove_avatar():
    current_user.img = 'default.jpg'
    db.session.commit()
    return redirect('/account')

@app.route('/account/delete', methods=['GET', 'POST'])
@login_required
def delete():
    if request.method == 'GET':
        return render_template('account_delete.html')
    else:
        if current_user.is_authenticated:
            db.session.delete(current_user)
            db.session.commit()
        return redirect('/')

########## PRODUCTS ##########

@app.route('/product/<int:id>')
def product(id):
    form = ReviewForm()
    reviews = Review.query.filter_by(item_id=id).all()
    item = Item.query.get_or_404(id)
    user = User.query.get_or_404(item.uploader)
    remaining = None
    if item.end_sale != None:
        # Compute time remaining
        now = datetime.today()
        remaining = item.end_sale - datetime.today()
        
        # If sale has ended, reset price
        if item.end_sale < now:
            item.discount_price = item.price
    
    return render_template('product.html', item=item, uploader=user, form=form, reviews=reviews, remaining=remaining)

# for seller use to add item
@app.route('/product', methods=['GET', 'POST'])
@seller_required
def selling():
    form = AddItemForm()
    if form.validate_on_submit():
        if form.img.data == None:
            img = 'default.jpg'
        else:
            img = update_img(form.img.data, 'products', size=600)
        name = form.name.data
        price = form.price.data
        description = form.description.data
        uploader = current_user.id
        
        item = Item(name = name, price = price, img = img, description = description, uploader = uploader)
        db.session.add(item)
        db.session.commit()
        return redirect(f'/product/{item.id}')

    return render_template('add_product.html', form=form)

# For seller to edit their item
@app.route('/product/<int:id>/edit', methods=['GET', 'POST'])
@seller_required
def edit_item(id):
    item = Item.query.get_or_404(id)
    form = EditItemForm()

    if not item.uploader == current_user.id:
        return redirect(f'/product/{id}')

    if form.validate_on_submit():
        if form.img.data != None:
            item.img = update_img(form.img.data, 'products', size=600)
        item.name = form.name.data
        item.price = form.price.data
        item.description = form.description.data
        item.discount_price = form.discount_price.data
        item.end_sale = form.end_sale.data
        db.session.commit()
        return redirect(f'/product/{item.id}')

    return render_template('edit_product.html', form=form, item=item)

@app.route('/product/<int:id>/delete', methods=['GET', 'POST'])
@seller_required
def delete_listing(id):
    item = Item.query.get_or_404(id)
    if request.method == 'GET':
        return render_template('delete_product.html', item = item)
    else:
        db.session.delete(item)
        db.session.commit()
        return redirect('/')

########## REVIEWS ##########

@app.route('/product/<int:id>/review', methods=['POST'])
@login_required
def review_product(id):
    form = ReviewForm()
    item = Item.query.get_or_404(id)
    if form.validate_on_submit():
        # Check if user has already reviewed this item
        if not config.getboolean('multiple_reviews'):
            reviewed = Review.query.filter_by(user_id = current_user.id, item_id = item.id).first()
            if reviewed != None:
                flash('You already left a review for this product!', 'error')
                return redirect(f'/product/{item.id}')
        
        rating = float(form.rating.data)
        review = Review(content=form.review.data, rating=int(rating), item_id=item.id, user_id=current_user.id)
        item.rating += (rating - item.rating) / (len(item.reviews) + 1)
        db.session.add(review)
        db.session.commit()
        return redirect(f'/product/{item.id}')
    return redirect(f'/product/{item.id}')

@app.route('/review/<int:id>/delete', methods=['GET'])
@login_required
def delete_review(id):
    review = Review.query.get_or_404(id)
    if current_user.id == review.user_id:
        item = review.item
        n = max(len(item.reviews) - 1, 1)
        item.rating = ((item.rating * (n + 1)) - review.rating) / n
        db.session.delete(review)
        db.session.commit()
    return redirect(f'/product/{review.item_id}')


########## CARTS ##########

@app.route('/cart')
def cart():
    return render_template('cart.html')

@app.route('/cart/add/<int:id>')
@login_required
def add_to_cart(id):
    item = Item.query.get_or_404(id)
    current_user.cart.append(item)
    db.session.commit()
    return redirect('/cart')

@app.route('/cart/remove/<int:id>')
@login_required
def remove_from_cart(id):
    item = Item.query.get_or_404(id)
    current_user.cart.remove(item)
    db.session.commit()
    return redirect('/cart')

@app.route('/cart/remove/all')
@login_required
def clear_cart():
    current_user.cart = []
    db.session.commit()
    return redirect('/')

@app.route('/cart/checkout', methods=['POST'])
@login_required
def checkout():
    current_user.cart = []
    db.session.commit()
    return redirect('/')

########## LISTS ##########

@app.route('/lists', methods = ['POST', 'GET'])
@login_required
def lists():
    form = ListForm()
    if form.validate_on_submit():
        name = form.name.data
        list = List(name = name, user_id = current_user.id)
        db.session.add(list)
        db.session.commit()
        return redirect('/lists')
    lists = List.query.filter_by(user_id = current_user.id).all()
    return render_template('lists.html', lists = lists, form = form)


@app.route('/lists/<int:id>', methods=['GET'])
@login_required
def view_list(id):
    list = List.query.get_or_404(id)
    return render_template('list.html', list=list)

@app.route('/lists/<int:id>/delete', methods=['GET'])
@login_required
def delete_list(id):
    list = List.query.get_or_404(id)
    db.session.delete(list)
    db.session.commit()
    return redirect('/lists')

@app.route('/lists/<int:list_id>/add/<int:id>')
@login_required
def add_to_list(list_id, id):
    list = List.query.get_or_404(list_id)
    item = Item.query.get_or_404(id)
    list.items.append(item)
    db.session.commit()
    return redirect(f'/lists/{list_id}')

@app.route('/lists/<int:list_id>/remove/<int:id>')
@login_required
def remove_from_list(list_id, id):
    list = List.query.get_or_404(list_id)
    item = Item.query.get_or_404(id)
    list.items.remove(item)
    db.session.commit()
    return redirect(f'/lists/{list_id}')

@app.route('/lists/<int:id>/remove/all')
@login_required
def clear_list(id):
    list = List.query.get_or_404(id)
    list.items = []
    db.session.commit()
    return redirect(f'/lists/{id}')

@app.route('/wishlist')
@login_required
def wishlist():
    return redirect(f'/lists/{current_user.lists[0].id}')

