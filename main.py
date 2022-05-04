from flask import Flask, render_template, flash, redirect, session, request, url_for
from flask_session import Session
from database_services import db_login, db_create_user, db_delete_user
from app import app, db
from app.routes import *

#SESSION_TYPE = 'filesystem'
#Session(app)

db.create_all()

'''
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
'''

if __name__ == '__main__':
    app.secret_key = 'super secret key'
    app.debug = True
    app.run(debug = True)
    