from flask import request, render_template
from app import app, db
from app.models import User

@app.route('/')
def home():
    return render_template('home.html')


@app.route('/register', methods=['GET', 'POST'])
def register():
    #   Method = POST
    email = None
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        password = request.form['password']

        # TODO: Password hash
        user = User(name = name, email = email, password_hash = password)
        db.session.add(user)
        db.session.commit()
        print(f"Created user {name} with email {email}")
        return render_template('home.html', email=name, message=f"User registration success")

    #   Method = GET
    return render_template('./register.html')
