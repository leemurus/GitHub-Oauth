from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_migrate import Migrate
from flask_socketio import SocketIO

from config import Config

# Create app and set configs
app = Flask(__name__, static_url_path='/static')
app.config.from_object(Config)
sio = SocketIO(app, async_mode='threading')

# Login manager
login = LoginManager(app)
login.login_view = 'authorization'

# Database
db = SQLAlchemy(app)
migrate = Migrate(app, db)

from app import api, models, views
