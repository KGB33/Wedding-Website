import os

from flask import Flask

from .extensions import login_manager, mongo
from .config import TestingConfig

__name__ = "weddingwebsite"


def create_app(config=TestingConfig):
    """ Flask application factory """

    # Setup Flask and load app.config
    app = Flask(__name__)
    app.config.from_object(config)

    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    @app.route("/test")
    def test():
        return "This is the test Page"

    # Register Blueprints
    register_blueprints(app)

    # init Extensions
    login_manager.init_app(app)
    login_manager.login_view = "auth.login"

    mongo.init_app(app)

    @login_manager.user_loader
    def load_user(user_id):
        from weddingwebsite.models import Guest
        from flask_pymongo import ObjectId

        guest = mongo.db.guests.find_one({"_id": ObjectId(user_id)})
        if guest is None:
            return None
        return Guest(**guest)

    return app


def register_blueprints(app):
    # Register Blueprints
    from . import views
    from weddingwebsite import admin
    from weddingwebsite import auth
    from weddingwebsite.lfgs import bp as lfgs_bp

    app.register_blueprint(views.views)
    app.register_blueprint(auth.auth)
    app.register_blueprint(admin.admin)
    app.register_blueprint(lfgs_bp)
