from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager

import os
from dotenv import load_dotenv

db = SQLAlchemy()

def create_app():
    app = Flask(__name__)

    load_dotenv()

    app.config['SECRET_KEY'] = os.environ["SECRET_KEY"]
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite'

    db.init_app(app)

    from . import models

    with app.app_context():
        db.create_all()

    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)

    from .models import User

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

    from .auth import auth as auth_blueprint
    app.register_blueprint(auth_blueprint)

    from .post import post as post_blueprint
    app.register_blueprint(post_blueprint)

    from .help import help as help_blueprint
    app.register_blueprint(help_blueprint)

    from .admin import admin as admin_blueprint
    app.register_blueprint(admin_blueprint)

    from .main import main as main_blueprint
    app.register_blueprint(main_blueprint)

    return app