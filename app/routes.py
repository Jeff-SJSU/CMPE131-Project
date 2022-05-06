from flask import request, render_template, redirect, flash
from flask_login import current_user, login_user, logout_user
from app import app, db
from app.forms import LoginForm, RegisterForm
from app.models import User

@app.route('/')
def home():
    return render_template('home.html')


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
