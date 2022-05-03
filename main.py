from flask import Flask, render_template, flash, redirect, session, request, url_for
from flask_session import Session
from database_services import db_login, db_create_user, db_delete_user
app = Flask(__name__, template_folder='.')
SESSION_TYPE = 'filesystem'
app.config.from_object(__name__)
Session(app)

@app.route('/')
def home():
    email = None
    if session.get('email', None) != None:
        email = session.get('email')    
    return render_template('home.html', email=email)

@app.route('/login/', methods=['GET', 'POST'])
def login():
    #   Method = POST
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        if db_login(email, password) == True:
            session['email'] = email
            return redirect(url_for('home'))
        else:
            return redirect(url_for('home'))

    #   Method = GET
    return render_template('./login.html')

@app.route('/logout')
def logout():
    session['email'] = None
    return redirect(url_for('home'))

@app.route('/create_account', methods=['GET', 'POST'])
def create_account():
    #   Method = POST
    email = None
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        password = request.form['password']

        if db_create_user(name, email, password) == True:
            session['email'] = email
            print("Create success")
            # message = "User {email} registration success"
            # return redirect(url_for('home'))
            return render_template('home.html',email=name, message=f"User {email} registration success")
        else:
            session['email'] = None
            print("Create failed")
            # message = "ERROR: User creation failed"
            # return redirect(url_for('home'))
            return render_template('home.html', email=None, message="ERROR: User creation failed")

    #   Method = GET
    return render_template('./create_account.html')

@app.route('/delete_account', methods=['GET', 'POST'])
def delete_account():
    #   Check if user is logged in
    message = None
    if request.method == 'POST':
        if session['email'] != None:
            db_delete_user(session['email'])
            message = f"User {session['email']} deleted"
            session['email'] = None
            return render_template('home.html', email=None, message=message)

    return render_template('delete_account.html', email=session['email'])
    
if __name__ == '__main__':
    app.secret_key = 'super secret key'
    app.debug = True
    app.run(debug = True)