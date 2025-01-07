from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_bcrypt import Bcrypt
from flask_login import LoginManager

""" instatiat extensions """
db = SQLAlchemy()
migrate = Migrate()
bcrypt = Bcrypt()
login_manager = LoginManager()

def app_extensions(app):
    """ initializing flask extentions wit app """
    db.init_app(app)
    migrate.init_app(app, db)
    bcrypt.init_app(app)
    login_manager.init_app(app)
    login_manager.login_view = 'auth.login'

    # provide placeholder for the user loader
    if not login_manager._user_callback:
        @login_manager.user_loader
        def load_user(user_id):
            """ placeholder user loader"""
            return None
