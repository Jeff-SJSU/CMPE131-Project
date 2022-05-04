from flask import request, render_template, redirect
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

        # TODO: Password hash?
        user = User(name = name, email = email, password_hash = password)
        db.session.add(user)
        db.session.commit()
        print(f"Created user {name} with email {email}")
        return redirect('/')

    return render_template('register.html', form=form)
