from configparser import ConfigParser
import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager

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

db = SQLAlchemy(app)
login = LoginManager(app)
