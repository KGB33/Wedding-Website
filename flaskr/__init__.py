import os

from flask import Flask

from flaskr.extensions import login_manager, mongo
from flaskr.secrets import DB_HOST, DB_NAME, FLASK_SECRET_KEY



def create_app(test_config=None):
    """ Flask application factory """

    # Setup Flask and load app.config
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY=FLASK_SECRET_KEY,
        MONGO_URI=DB_HOST,
        USER_APP_NAME="Wedding-Website",  # Shown in and email templates and page footers
        USER_ENABLE_EMAIL=False,  # Disable email authentication
        USER_ENABLE_USERNAME=True,  # Enable username authentication
        USER_REQUIRE_RETYPE_PASSWORD=False,  # Simplify register form
    )

    if test_config is None:
        app.config.from_pyfile('config.py', silent=True)
    else:
        app.config.from_mapping(test_config)

    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    @app.route('/test')
    def test():
        return 'This is the test Page'

    # Register Blueprints
    register_blueprints(app)

    # init Extensions
    login_manager.init_app(app)
    login_manager.login_view = 'auth.login'

    mongo.init_app(app)

    @login_manager.user_loader
    def load_user(user_id):
        from flaskr.models import Guest
        from flask_pymongo import ObjectId
        guest = mongo.db.guests.find_one({'_id': ObjectId(user_id)})
        if guest is None:
            return None
        return Guest(**guest)

    return app


def register_blueprints(app):
    # Register Blueprints
    from . import main, auth, profile
    app.register_blueprint(main.bp)
    app.register_blueprint(auth.bp)
    app.register_blueprint(profile.bp)


# Create app
app = create_app()



