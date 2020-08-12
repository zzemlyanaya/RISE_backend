from flask import Flask
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy
from flask_socketio import SocketIO

from config import Config

db = SQLAlchemy()

login_manager = LoginManager()
login_manager.login_view = 'login'

socketio = SocketIO(always_connect=True)


def create_app():
    """Construct the core application."""
    app = Flask(__name__)
    db.init_app(app)
    app.config.from_object(Config)

    login_manager.init_app(app)

    socketio.init_app(app)

    with app.app_context():
        # Imports
        from . import routes, events

        return app
