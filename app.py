from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_bcrypt import Bcrypt
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView
from Model.model import *

db = SQLAlchemy()
bcrypt = Bcrypt()
login_manager = LoginManager()
login_manager.login_view = 'auth.login'
admin = Admin()

def create_app():
    app = Flask(__name__)
    db.init_app(app)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///schools.sqlite3'
    app.secret_key = 'something secret'
    login_manager.init_app(app)

    from auth import auth as auth_blueprint
    app.register_blueprint(auth_blueprint)

    from main import main as main_blueprint
    app.register_blueprint(main_blueprint)


    admin.add_view(ModelView(Teacher, db.session))
    admin.add_view(ModelView(Student, db.session))
    admin.add_view(ModelView(Room, db.session))
    admin.add_view(ModelView(Assignment, db.session))

    return app






