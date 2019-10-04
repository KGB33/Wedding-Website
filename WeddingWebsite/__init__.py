import os

from flask import Flask

from WeddingWebsite.extensions import login_manager, mongo
from WeddingWebsite.secrets import DB_HOST, DB_NAME, FLASK_SECRET_KEY


def create_app(config):
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
        from WeddingWebsite.models import Guest
        from flask_pymongo import ObjectId

        guest = mongo.db.guests.find_one({"_id": ObjectId(user_id)})
        if guest is None:
            return None
        return Guest(**guest)

    return app


def register_blueprints(app):
    # Register Blueprints
    from . import views
    from WeddingWebsite import admin
    from WeddingWebsite import auth

    app.register_blueprint(views.views)
    app.register_blueprint(auth.auth)
    app.register_blueprint(admin.admin)
