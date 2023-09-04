from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from inkdone.config import Config


db = SQLAlchemy()
migrate = Migrate()

bcrypt = Bcrypt()

login_manager = LoginManager()
login_manager.session_protection = "strong"
login_manager.login_view = "users.login"
login_manager.login_message_category = "🚫"


def create_app(config_class=Config):
    app = Flask(__name__)
    app.app_context().push()
    app.config.from_object(Config)

    db.init_app(app)
    migrate.init_app(app, db)
    bcrypt.init_app(app)
    login_manager.init_app(app)

    from inkdone.users.routes import users
    from inkdone.core.routes import core
    from inkdone.errors.handlers import errors

    app.register_blueprint(users)
    app.register_blueprint(core)
    app.register_blueprint(errors)

    return app