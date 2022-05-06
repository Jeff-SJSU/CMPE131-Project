from flask import Flask, render_template, flash, redirect, session, request, url_for
from flask_session import Session
from app import app, db
from app.routes import *

#SESSION_TYPE = 'filesystem'
#Session(app)

db.create_all()


if __name__ == '__main__':
    app.secret_key = 'super secret key'
    app.debug = True
    app.run(debug = True)
    