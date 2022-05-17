from jinja2 import pass_context
from configparser import ConfigParser
import configparser
import os
from flask import Flask, flash as _flash
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, current_user

config = ConfigParser()
config.read('config.ini')
config = config['app']

# root project dir
basedir = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))

app = Flask(__name__, template_folder='../templates', static_folder='../static')

app.config.from_mapping(
    DEBUG=config.getboolean('debug', True),
    SECRET_KEY=config.get('secret_key', 'secret key'),
    # Don't change the name of database.db. Instead, try closing python and deleting the file.
    SQLALCHEMY_DATABASE_URI='sqlite:///' + os.path.join(basedir, config.get('db', 'database.db')),
    SQLALCHEMY_TRACK_MODIFICATIONS=False
)

lang = ConfigParser(default_section = "en")
lang.read('lang.ini',encoding = "utf-8")

# Get localized string
def getloc(key):
    if current_user.is_anonymous:
        return lang.get("en", key, fallback = key)
    else:
        return lang.get(current_user.lang, key, fallback = key)

# Flash localized message
def flash(message, category='message'):
    return _flash(getloc(message), category=category)

db = SQLAlchemy(app)
            
logins = LoginManager(app)
logins.login_view = '/login'
logins.login_message = lang.get("en", 'Required_login')
logins.login_message_category = 'error'

# Filter for localization
@app.template_filter()
@pass_context
def loc(context, key):
    return getloc(key)

