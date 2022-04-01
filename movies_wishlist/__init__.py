from flask import Flask
from .extensions import db, bcrypt, login_manager


def create_app(config_object="movies_wishlist.config.DevelopmentConfig"):
    app = Flask(__name__, instance_relative_config=False)
    app.config.from_object(config_object)
    register_extensions(app)
    register_blueprint(app)
    return app


def register_extensions(app):
    db.init_app(app)
    bcrypt.init_app(app)
    login_manager.init_app(app)


def register_blueprint(app):
    from .main.routes import main
    from .user.routes import user
    app.register_blueprint(main)
    app.register_blueprint(user)
