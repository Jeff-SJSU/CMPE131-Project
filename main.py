from flask import Flask, render_template, flash, redirect, session, request, url_for
from flask_session import Session
from app import app, db
from app.routes import *

#SESSION_TYPE = 'filesystem'
#Session(app)

db.create_all()


if __name__ == '__main__':
    app.run()
    