from flask import Flask
from .main.utils import UsersHandler
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


def create_app():
    app = Flask(__name__)
    app.secret_key = 'o9rew908qre3qr3$TEw3qejrewqopreREWQr'

    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///questions.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    db.init_app(app)

    from .main import main as main_blueprint
    app.register_blueprint(main_blueprint)
    return app