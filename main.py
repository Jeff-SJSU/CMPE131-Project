from flask import Flask, render_template, flash, redirect, session, request, url_for
from app import app, db
from app.routes import *

db.create_all()

if __name__ == '__main__':
    app.run()
    